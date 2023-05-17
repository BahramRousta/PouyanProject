import logging


app_logger = logging.getLogger(__name__)
app_logger.view_name = None
app_logger.setLevel(logging.INFO)
app_filehandler = logging.FileHandler(filename='log/app.log', mode='a')
app_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
app_filehandler.setFormatter(app_formatter)
app_logger.addHandler(app_filehandler)