import asyncio

import pytest
from fastapi import HTTPException

from server import app as server_app


def test_create_session_rejects_role_mismatch(world: dict) -> None:
    server_app._SESSIONS.clear()

    with pytest.raises(HTTPException) as exc_info:
        server_app.create_session(
            server_app.SessionCreate(user_id=9002, role="shopper")
        )

    assert exc_info.value.status_code == 403


def test_message_rejects_token_for_another_session(world: dict) -> None:
    server_app._SESSIONS.clear()

    first = server_app.create_session(
        server_app.SessionCreate(user_id=9002, role="merchant")
    )
    second = server_app.create_session(
        server_app.SessionCreate(user_id=9002, role="merchant")
    )

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            server_app.post_message(
                second["session_id"],
                server_app.MessageIn(message="Hello"),
                authorization=f"Bearer {first['token']}",
            )
        )

    assert exc_info.value.status_code == 403
