from pydantic import BaseModel


class MatchedPerson(BaseModel):
    """
    Base Model for the profile of a matched person.
    """

    profile: str
    photo: str
    source: str
    age: int
    first_name: str
    last_name: str
    city: str
    country: str

    def __repr__(self) -> str:

        return self.json()
