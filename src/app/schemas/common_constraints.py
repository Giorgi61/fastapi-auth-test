from typing import Annotated

from pydantic import Field

str50 = Annotated[str, Field(max_length=50)]
str200 = Annotated[str, Field(max_length=200)]

nullable_str = Annotated[str | None, Field(default=None)]

password_field = Annotated[str, Field(min_length=8,)]