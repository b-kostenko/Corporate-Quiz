from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Parameters for pagination."""

    limit: int = Field(default=10, ge=1, le=100, description="Number of items per page")
    offset: int = Field(default=0, ge=0, description="Number of items to skip")


class PaginationMeta(BaseModel):
    """Metadata for pagination response."""

    total: int = Field(description="Total number of items")
    limit: int = Field(description="Number of items per page")
    offset: int = Field(description="Number of items skipped")
    has_next: bool = Field(description="Whether there are more items")
    has_previous: bool = Field(description="Whether there are previous items")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response."""

    items: list[T] = Field(description="List of items")
    meta: PaginationMeta = Field(description="Pagination metadata")
