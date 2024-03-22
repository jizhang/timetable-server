from pydantic import BaseModel, ConfigDict, Field


class LoginForm(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class CurrentUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
