import logging
logger = logging.getLogger(__name__)

class InfoOnlyFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno == logging.INFO


class ExcludeDjangoLogsFilter(logging.Filter):
    """ Excludes django system logs from logger """
    modules_to_exclude = (
        "daphne.server",
        "daphne.cli",
        "django",
        "django.db",
        "django.server"
    )

    def filter(self, record: logging.LogRecord) -> bool:
        """ Filters records to exclude from a logging modules with a certain names. """
        return not record.name.startswith(self.modules_to_exclude)