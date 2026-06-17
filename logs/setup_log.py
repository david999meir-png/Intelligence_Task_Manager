import logging

def setup_logger():
    return logging.basicConfig(
        level=logging.DEBUG,
        format= "%(asctime)s | %(levelname)s | %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler("logs/app.log")]
    )
