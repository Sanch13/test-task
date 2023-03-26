from loguru import logger


logger_1 = logger.bind()
logger_1.add("./logs/firsttask.log",
             rotation="10 MB",
             format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {function}:{line} | {message}",
             compression="zip")
