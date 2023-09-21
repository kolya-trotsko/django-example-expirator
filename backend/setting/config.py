from pathlib import Path
import os
import logging

TG_TOKEN = ''

pegas_api_key = ''
                      
TG_CHATID_DOMAIN_END = 
TG_CHATID = 
TG_CHATID_ERROR = 
DB_PATH = os.path.join(Path(__file__).resolve().parent.parent.parent, 'db.sqlite3')
log_path = os.path.join(Path(__file__).resolve().parent, "../logs/logfile.log")


logging.basicConfig(
    level=logging.ERROR,
    filename=log_path,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)
