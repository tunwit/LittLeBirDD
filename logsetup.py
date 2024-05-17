import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import sys

class Log():
    def __init__(self) -> None:
        self.setup()

    def logger_filename(self):
        now = datetime.now()
        return 'littlebirdd_'+now.strftime("%Y-%m-%d")+'.log'

    def setup(self):
        logger = logging.getLogger('littlebirdd')
        logger.setLevel(logging.INFO)

        handler = TimedRotatingFileHandler(filename='log/'+self.logger_filename(),when='midnight', interval=1, backupCount=7)
        handler.rotation_filename = self.logger_filename

        formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s     %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)

        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(formatter)

        logger.addHandler(handler)
        logger.addHandler(console)

Log()