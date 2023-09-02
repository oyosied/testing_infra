import pytest

from infra.managers.test_manager import TestManager
from infra.utils.logs_handler import LoggingSettings


# fetching desired log level
def pytest_addoption(parser):
    parser.addoption("--log_level", action="store", default="INFO", help="Set the log level for Loguru")


def pytest_sessionstart(session):
    log_level = session.config.getoption("--log_level").upper()
    logs_settings = LoggingSettings(log_level=log_level, log_path='automation_logs/')
    logs_settings.configure_logs()


@pytest.fixture(scope="function", autouse=True)
def clean_environment(test_manager: TestManager):
    test_manager.character_api.reset_characters()
    yield
    test_manager.character_api.reset_characters()


@pytest.fixture(scope="session", autouse=True)
def test_manager(request):
    test_manager: TestManager = TestManager()
    yield test_manager
