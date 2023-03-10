<div align="left">
    <h1>Search4FacesAPI <img src="https://search4faces.com/favicon.ico" width=30 height=30></h1>
    <p align="left" >
        <a href="https://pypi.org/project/Search4Faces/">
            <img src="https://img.shields.io/pypi/v/Search4Faces?style=flat-square" alt="PyPI">
        </a>
        <a href="https://pypi.org/project/Search4Faces/">
            <img src="https://img.shields.io/pypi/dm/Search4Faces?style=flat-square" alt="PyPI">
        </a>
    </p>
</div>

A simple library with async capabilities to interact with Search4Faces [API](https://search4faces.com/api.html)


## Usage

With ``SearchClient`` you can easily find social media profiles with similar faces. It is a great tool for finding duplicates, finding people, and more.

## Documentation

Official docs can be found on the [API's webpage](https://search4faces.com/api.html)

## Installation

```bash
pip install Search4Faces
```

## Requirements

 - ``Python 3.9+``
 - ``httpx``
 - ``pydantic``

## Features

 - ``Async capabilities``
 - ``Exception handling``
 - ``Pydantic return model``
 - ``LightWeight``

## Examples

```python
from Search4Faces import (
    SearchClient, 
    SearchAPIError, 
    MatchedPerson,
    sources,
)

client = SearchClient(
    token='your-token',     
    no_check=False,    # if you want to disable token check
) 

# you can use photo's url - client will fetch the image for you
photo_url = 'https://imgur.com/XYZ.jpg'
response: list[MatchedPerson] = client.find_similar(
    photo_url,
    source=sources.VK_OK_NEW_AVATAR, # you can specify the image database to search in
    show_hidden=True,                # or define if you want hidden profiles to show up
    results=25,                      # and choose how many results you want back (max 500)
)

# you can also provide a file / io.BytesIO object
response: list[MatchedPerson] = client.find_similar(
    open('photo.jpg', 'rb'),
)

# you can do some exception handling
try:

    response: list[MatchedPerson] = client.find_similar(photo_url)

except SearchAPIError as exc:

    print(exc)

# you can use some async methods
await client.find_similar_async(photo_url)
```

Developed by Nikita Minaev (c) 2023
