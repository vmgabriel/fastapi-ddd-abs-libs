import enum


class HistoryChangeType(enum.StrEnum):
    INSERTED = enum.auto()
    UPDATED = enum.auto()
    DELETED = enum.auto()
