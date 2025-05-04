import logging

class LevelBasedFormatterHandler(logging.StreamHandler):
    def emit(self, record):
        if record.levelno >= logging.CRITICAL:
            fmt = '[CRITICAL] {asctime} | {levelname} | {message} | {pathname} | {exc_text}'
        elif record.levelno >= logging.ERROR:
            fmt = '[ERROR] {asctime} | {levelname} | {message} | {pathname} | {exc_text}'
        elif record.levelno >= logging.WARNING:
            fmt = '[WARNING] {asctime} | {levelname} | {message} | {pathname}'
        elif record.levelno >= logging.INFO:
            fmt = '[INFO] {asctime} | {levelname} | {message}'
        else:
            fmt = '[DEBUG] {asctime} | {levelname} | {message}'

        if record.exc_info:
            record.exc_text = self.formatException(record.exc_info)
        else:
            record.exc_text = ''

        formatter = logging.Formatter(fmt=fmt, style='{')
        self.setFormatter(formatter)
        super().emit(record)