from pydantic import BaseModel, Field


class LoginForm(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class CurrentUser(BaseModel):
    id: int
    username: str
