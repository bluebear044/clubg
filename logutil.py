import config

from logging import handlers
import logging

def fileLog(content) :
	mylogger = logging.getLogger("CLUBG")
	mylogger.setLevel(logging.INFO)

	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

	file_handler = handlers.TimedRotatingFileHandler(filename=config.PRJ_CONFIG['path'] + 'log', when='midnight', interval=1, encoding='utf-8')
	file_handler.setFormatter(formatter)
	file_handler.suffix = "%Y%m%d"
	
	mylogger.addHandler(file_handler)
	
	mylogger.info(content) 


if __name__ == '__main__':
	fileLog("test!!")

