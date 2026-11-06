
from pydantic import BaseModel, Field


# Data received when creating a message
class MessageCreate(BaseModel):
    sender: str = Field(min_length=2, max_length=50)
    message: str = Field(min_length=1, max_length=1000)


# Data received when updating a message
class MessageUpdate(BaseModel):
    sender: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
    )

    message: str | None = Field(
        default=None,
        min_length=1,
        max_length=1000,
    )


# Data returned for an individual message
class MessageResponse(BaseModel):
    id: int
    sender: str
    message: str


# Data returned when retrieving multiple messages
class MessageListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    data: list[MessageResponse]


# Data returned after deleting a message
class MessageDeleteResponse(BaseModel):
    status: str
    message: str
    data: MessageResponse
