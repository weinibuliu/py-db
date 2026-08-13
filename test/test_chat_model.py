"""Unit tests for chat ORM models and their create/update DTOs."""

import pytest
from pydantic import ValidationError
from sqlalchemy import Text

from db._db.model._chat import (
    ChatMessage,
    ChatSession,
    ChatMessageCreate,
    ChatSessionCreate,
    ChatSessionUpdate,
)
from db.common.define import ChatRole, ChatSessionStatus


def _session_data() -> dict[str, object]:
    return {
        "session_id": "session-1",
        "status": ChatSessionStatus.OK,
        "uid": "user-1",
        "title": "A chat session",
    }


def _message_data() -> dict[str, object]:
    return {
        "session_id": "session-1",
        "message_id": "message-1",
        "uid": "user-1",
        "role": "user",
        "content": "Hello",
        "model": "test-model",
        "temperature": 1,
        "top_k": 40,
        "cached_tokens": 1,
        "uncached_tokens": 2,
        "output_tokens": 5,
    }


def test_create_chat_session_uses_counter_defaults() -> None:
    session = ChatSessionCreate(**_session_data())

    assert session.message_count == 0
    assert session.total_tokens == 0
    assert session.created_by is None
    assert session.edited_by is None


def test_create_chat_session_preserves_explicit_values() -> None:
    session = ChatSessionCreate(
        **_session_data(),
        message_count=4,
        total_tokens=128,
        created_by="creator-1",
        edited_by="editor-1",
    )

    assert session.session_id == "session-1"
    assert session.status is ChatSessionStatus.OK
    assert session.uid == "user-1"
    assert session.title == "A chat session"
    assert session.message_count == 4
    assert session.total_tokens == 128
    assert session.created_by == "creator-1"
    assert session.edited_by == "creator-1"


@pytest.mark.parametrize("field", ["session_id", "status", "uid", "title"])
def test_create_chat_session_rejects_missing_required_field(field: str) -> None:
    data = _session_data()
    data.pop(field)

    with pytest.raises(ValidationError):
        ChatSessionCreate(**data)


@pytest.mark.parametrize("field", ["uid", "title"])
def test_create_chat_session_rejects_strings_over_255_characters(field: str) -> None:
    data = _session_data()
    data[field] = "x" * 256

    with pytest.raises(ValidationError):
        ChatSessionCreate(**data)


def test_update_chat_session_supports_partial_updates() -> None:
    empty_update = ChatSessionUpdate()
    update = ChatSessionUpdate(
        status=ChatSessionStatus.Archived,
        title="Archived chat",
    )

    assert empty_update.model_dump(exclude_unset=True) == {}
    assert update.model_dump(exclude_unset=True, exclude_none=True) == {
        "status": ChatSessionStatus.Archived,
        "title": "Archived chat",
    }


def test_create_chat_message_preserves_all_fields() -> None:
    message = ChatMessageCreate(
        **_message_data(),
        created_by="creator-1",
        edited_by="editor-1",
    )

    assert message.session_id == "session-1"
    assert message.message_id == "message-1"
    assert message.uid == "user-1"
    assert message.role is ChatRole.user
    assert message.content == "Hello"
    assert message.model == "test-model"
    assert message.temperature == 1
    assert message.top_k == 40
    assert message.cached_tokens == 1
    assert message.uncached_tokens == 2
    assert message.output_tokens == 5
    assert message.created_by == "creator-1"
    assert message.edited_by == "creator-1"


@pytest.mark.parametrize(
    "field",
    [
        "session_id",
        "message_id",
        "uid",
        "role",
        "content",
        "model",
        "temperature",
        "top_k",
        "cached_tokens",
        "uncached_tokens",
        "output_tokens",
    ],
)
def test_create_chat_message_rejects_missing_required_field(field: str) -> None:
    data = _message_data()
    data.pop(field)

    with pytest.raises(ValidationError):
        ChatMessageCreate(**data)


def test_create_chat_message_rejects_uid_over_255_characters() -> None:
    data = _message_data()
    data["uid"] = "x" * 256

    with pytest.raises(ValidationError):
        ChatMessageCreate(**data)


@pytest.mark.parametrize(
    ("model", "table_name", "text_column", "index_name"),
    [
        (ChatSession, "chat_session", "summary", "chat_session_uid_index"),
        (ChatMessage, "chat_message", "content", "chat_message_uid_index"),
    ],
)
def test_chat_table_mapping(
    model: type[ChatSession] | type[ChatMessage],
    table_name: str,
    text_column: str,
    index_name: str,
) -> None:
    table = model.__table__

    assert table.name == table_name
    assert isinstance(table.c[text_column].type, Text)
    assert table.c.uid.type.length == 255

    index = next(index for index in table.indexes if index.name == index_name)
    assert [column.name for column in index.columns] == ["uid"]
