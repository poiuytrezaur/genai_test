"""Pytest configuration for Weather App."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _pytest.config import Config


def pytest_configure(config: Config) -> None:
    """Configure pytest.

    Args:
        config: Pytest configuration object
    """
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line(
        "markers",
        "integration: mark test as an integration test",
    )
