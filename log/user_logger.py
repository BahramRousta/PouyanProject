import logging


user_logger = logging.getLogger(__name__)
user_logger.view_name = None
user_logger.setLevel(logging.INFO)
user_filehandler = logging.FileHandler(filename='log/user.log', mode='a')
user_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
user_filehandler.setFormatter(user_formatter)
user_logger.addHandler(user_filehandler)