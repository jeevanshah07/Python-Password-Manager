import logging

logs = logging.getLogger(__name__)
logs.setLevel(logging.DEBUG)

stream = logging.StreamHandler()
stream.setLevel(logging.DEBUG)
streamformat = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
stream.setFormatter(streamformat)

logs.addHandler(stream)

fileHandler = logging.FileHandler("logs/logs.log")
fileHandler.setLevel(logging.DEBUG)
fileformat = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s",datefmt="%H:%M:%S")
fileHandler.setFormatter(fileformat)

logs.addHandler(fileHandler)

logs.debug('Hello Wolrd')
