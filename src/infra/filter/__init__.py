from __future__ import annotations

from src.domain.models import filter

from . import postgres

filter_builder: filter.FilterBuilder = postgres.postgres_filter_builder
