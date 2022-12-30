import io
import httpx

from .models import MatchedPerson
from .exceptions import (
    SearchAPIError,
    check_for_errors, 
    check_for_errors_async,
)

from base64 import b64encode
from typing import Union


class SearchClient:
    """
    Base class for the Search4Faces API client.
    Documentation: https://search4faces.com/api.html
    """

    DEFAULT_PARAMS = {
        "jsonrpc": "2.0",
        "id": "some-id",
    }
    API_URL = 'https://search4faces.com/api/json-rpc/v1'

    def __init__(self, token: str):
        """
        Creates a new api client instance.
        Documentation: https://search4faces.com/api.html

        :param str token: The API token. Example: 'abcdef-ghiklm-nopqrs-tuvxyz-xxxxxx'
        :raises SearchAPIError: If the token is invalid
        """

        self.token = token
        self.client = httpx.Client(timeout=120)
        self.async_client = httpx.AsyncClient(timeout=120)

        response = self._make_request(method="rateLimit")
        if 'error' in response:

            raise SearchAPIError(response['error'])


    @property
    def HEADERS(self) -> dict:

        return {
            "Content-Type": "application/json-rpc", 
            "x-authorization-token": self.token,
        }


    def _retrieve_photo(self, photo_url: str) -> io.BytesIO:

        response = self.client.get(photo_url)
        return io.BytesIO(response.content)

    
    async def _retrieve_photo_async(self, photo_url: str) -> io.BytesIO:

        response = await self.async_client.get(photo_url)
        return io.BytesIO(response.content)


    @check_for_errors
    def _make_request(self, **kwargs) -> dict:

        response = self.client.post(
            self.API_URL,
            headers=self.HEADERS,
            json={
                **self.DEFAULT_PARAMS,
                **kwargs,
            },
        )
        
        return response.json()


    @check_for_errors_async
    async def _make_request_async(self, **kwargs) -> dict:
    
        response = await self.async_client.post(
            self.API_URL,
            headers=self.HEADERS,
            json={
                **self.DEFAULT_PARAMS,
                **kwargs,
            },
        )
            
        return response.json()


    async def find_similar_async(
        self, 
        image: Union[io.BytesIO, str], 
        source: str='vk_wall', 
        show_hidden: bool=True, 
        results: int=10,
    ) -> list[MatchedPerson]:
        """
        This method searches for similar faces in the database, asynchronously.
        Documentation: https://search4faces.com/api.html

        :param BytesIO | str image: The image to process (can be a url)
        :param str source:          The database to search in
        :param bool show_hidden:    Whether to show hidden profiles 
        :param int results:         How many results to return (max 500)
        :type priority:             integer or None
        :return:                    list[MatchedPerson]
        :rtype:                     list
        :raises SearchAPIError: If the API returns an error
        """
        
        if isinstance(image, str):

            image = await self._retrieve_photo_async(image)

        ascii_image = b64encode(image.read()).decode("ascii")

        response = (await self._make_request_async(
            method="detectFaces",
            params={
                'image': ascii_image,
            }, 
        ))['result']

        result = (await self._make_request_async(
            method="searchFace",
            params={
                "image": response['image'],
                "face": response['faces'][0],
                "source": source,
                "hidden": show_hidden,
                "results": results,
                "lang": "ru",
            },
        ))['result']
        
        return [
            MatchedPerson(**person) 
            for person 
            in result['profiles']
        ]


    def find_similar(
        self, 
        image: Union[io.BytesIO, str], 
        source: str='vk_wall',
        show_hidden: bool=True, 
        results: int=10,
    ) -> list[MatchedPerson]:
        """
        This method searches for similar faces in the database.
        Documentation: https://search4faces.com/api.html

        :param BytesIO | str image: The image to process (can be a url)
        :param str source: The database to search in
        :param bool show_hidden: Whether to show hidden profiles 
        :param int results: How many results to return (max 500)
        :type priority: integer or None
        :return: list[MatchedPerson]
        :rtype: list
        :raises SearchAPIError: If the API returns an error
        """

        if isinstance(image, str):

            image = self._retrieve_photo(image)

        ascii_image = b64encode(image.read()).decode("ascii")

        response = self._make_request(
            method="detectFaces",
            params={
                'image': ascii_image,
            }, 
        )['result']

        result = self._make_request(
            method="searchFace",
            params={
                "image": response['image'],
                "face": response['faces'][0],
                "source": source,
                "hidden": show_hidden,
                "results": results,
                "lang": "ru",
            },
        )['result']

        return [
            MatchedPerson(**person) 
            for person 
            in result['profiles']
        ]
