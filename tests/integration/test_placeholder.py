import pytest

pytestmark = pytest.mark.integration


@pytest.mark.integration
async def test_placeholder() -> None:
    assert True