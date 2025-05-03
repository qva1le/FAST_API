from typing  import Annotated
from fastapi import Depends, Query
from pydantic import BaseModel

class Pagination(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(5,ge=1, lt=30)]

PaginationDep = Annotated[Pagination, Depends()]