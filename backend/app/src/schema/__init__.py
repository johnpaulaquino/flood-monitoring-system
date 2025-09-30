from typing import Optional

from pydantic import BaseModel, Field


class Paginated(BaseModel):
     skip: Optional[int] = Field(default=1, ge=1)
     limit: Optional[int] = Field(default=10,ge=10)
