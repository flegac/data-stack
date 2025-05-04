import sys

FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <7}</level> | "
    "<cyan>{name}:{line}</cyan> | <level>{function}</level>\n"
    # "<yellow>pid:{process.id: >6} thread:{thread.id: >6} "
    # "elapsed: {elapsed}</yellow> \n"
    "{message}"
)


class _Logger:
    @staticmethod
    def configure():
        from loguru import logger

        logger.remove()
        logger.add(
            sink=sys.stdout,
            format=FORMAT,
            colorize=True,
        )
        return logger


logger = _Logger.configure()
