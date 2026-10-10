"""Process-local storage boundary for reviewable editorial content."""

from __future__ import annotations

from uuid import uuid4

from apps.api.editorial_review import EditorialContent


class EditorialContentStore:
    """Store editorial records by stable ID for the lifetime of the API process."""

    def __init__(self) -> None:
        self._items: dict[str, EditorialContent] = {}

    def create(self, content: EditorialContent) -> EditorialContent:
        if content.content_id in self._items:
            raise ValueError(f"content_id already exists: {content.content_id}")
        self._items[content.content_id] = content
        return content

    def create_id(self) -> str:
        return uuid4().hex

    def get(self, content_id: str) -> EditorialContent | None:
        return self._items.get(content_id)

    def save(self, content: EditorialContent) -> EditorialContent:
        if content.content_id not in self._items:
            raise KeyError(content.content_id)
        self._items[content.content_id] = content
        return content

    def clear(self) -> None:
        self._items.clear()


__all__ = ["EditorialContentStore"]
