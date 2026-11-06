
from fastapi import APIRouter, HTTPException, Query, status

from schemas import (
    MessageCreate,
    MessageUpdate,
    MessageResponse,
    MessageListResponse,
    MessageDeleteResponse,
)


router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


# Temporary storage
storage = {
    "next_id": 1,
    "messages": {},
}


# CREATE
@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_message(message_data: MessageCreate):

    message_id = storage["next_id"]

    new_message = {
        "id": message_id,
        "sender": message_data.sender,
        "message": message_data.message,
    }

    storage["messages"][message_id] = new_message
    storage["next_id"] += 1

    return new_message


# READ ALL
@router.get(
    "",
    response_model=MessageListResponse,
)
def get_messages(
    sender: str | None = None,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):

    messages = list(storage["messages"].values())

    if sender is not None:
        messages = [
            message
            for message in messages
            if message["sender"].lower() == sender.lower()
        ]

    total = len(messages)

    paginated_messages = messages[offset:offset + limit]

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "data": paginated_messages,
    }


# READ ONE
@router.get(
    "/{message_id}",
    response_model=MessageResponse,
)
def get_message(message_id: int):

    message = storage["messages"].get(message_id)

    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    return message


# UPDATE
@router.patch(
    "/{message_id}",
    response_model=MessageResponse,
)
def update_message(
    message_id: int,
    message_data: MessageUpdate,
):

    message = storage["messages"].get(message_id)

    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    updates = message_data.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    message.update(updates)

    return message


# DELETE
@router.delete(
    "/{message_id}",
    response_model=MessageDeleteResponse,
)
def delete_message(message_id: int):

    message = storage["messages"].pop(message_id, None)

    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    return {
        "status": "success",
        "message": "Message deleted successfully",
        "data": message,
    }
