import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import sys
import os
import discord

class Log():
    def __init__(self) -> None:
        self.checkpath()
        self.setup()

    def checkpath(self):
        if not os.path.exists('log'):
            os.mkdir('log')

    def logger_filename(self):
        now = datetime.now()
        return 'littlebirdd_'+now.strftime("%Y-%m-%d")+'.log'

    def unhandle_exception(self,exc_type, exc_value, exc_traceback):
        logger = logging.getLogger('littlebirdd')
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

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

        discord.utils.setup_logging(handler=handler,level=logging.ERROR,formatter=formatter,root=False)

        sys.excepthook = self.unhandle_exception

Log()