from typing import Annotated

from pydantic import Field

PositiveInt = Annotated[int, Field(gt=0)]
