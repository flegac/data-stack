import sys

FORMAT = (
    "<yellow>{thread.name: <8}@{process.name: >6}</yellow> | "
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <7}</level> | "
    "<cyan>{name}:{line}</cyan> | <level>{function}</level>\n"
    # "<yellow>elapsed: {elapsed}</yellow> \n"
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
