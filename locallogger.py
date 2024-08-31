import logging

logger = logging.getLogger("GlobalLogger")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("local.log")
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Adjust level for console output
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
