import logging

class LevelBasedFormatter(logging.Formatter):
    """Форматирует вывод в консоль по уровню логирования."""

    def format(self, record):
        # Если Warning или выше — добавляем путь файла
        if record.levelno >= logging.WARNING:
            self._style._fmt = '{asctime} {levelname} {message} {pathname}'
        else:
            self._style._fmt = '{asctime} {levelname} {message}'

        # Если Error или выше — добавляем стек ошибки
        if record.levelno >= logging.ERROR and record.exc_info:
            self._style._fmt += ' {exc_info}'

        return super().format(record)

class LevelBasedStreamHandler(logging.StreamHandler):
    """Кастомный StreamHandler с умным форматированием."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFormatter(LevelBasedFormatter(style='{'))