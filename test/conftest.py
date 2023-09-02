

from infra.utils.logs_handler import LoggingSettings

# fetching desired log level
def pytest_addoption(parser):
    parser.addoption("--log_level", action="store", default="INFO", help="Set the log level for Loguru")

def pytest_sessionstart(session):
    log_level = session.config.getoption("--log_level").upper()
    logs_settings = LoggingSettings(log_level=log_level,log_path='automation_logs/')
    logs_settings.configure_logs()
