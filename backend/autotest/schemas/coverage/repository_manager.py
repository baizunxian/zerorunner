from pydantic import BaseModel, Field


class RepositoryListQuery(BaseModel):
    id: int = Field(None, description="id")
    name: str = Field(None, description="name")
