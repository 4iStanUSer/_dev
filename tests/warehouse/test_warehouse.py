from iap.common.repository.models_managers.warehouse import Warehouse

import pandas as pd
from timeit import default_timer as timer
from sqlalchemy import create_engine
import logging
import logging.config

logger = logging.getLogger(__name__)


handler = logging.handlers.RotatingFileHandler(
              'warehouse.ini', maxBytes=20, backupCount=5)
logger.addHandler(handler)
# create a file handler
info_handler = logging.FileHandler('info.log')
info_handler.setLevel(logging.INFO)

warnign_handler = logging.FileHandler('info.log')
warnign_handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
warnign_handler.setFormatter(formatter)
info_handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(info_handler)
logger.addHandler(warnign_handler)



path_db_engine = "sqlite:///C:/Users/Alex/Desktop/iap/IAP.sqlite"

path_to_files = "C:/Users/Alex/Desktop/iap/data_storage/data_lake" \
                "/JJOralCare/JJOralCare_Sales.csv"

def test_warehouse_write():

    start = timer()
    wh = Warehouse(engine=path_db_engine, ssn_factory=None)
    project_name = "oralcare"
    logger.info("")
    df = pd.read_json(path_to_files)
    wh.save_project_data(project_name, df)
    end = timer()
    elapsed_time = end - start
    print('completed singlethread insert loops in %s sec!' % (elapsed_time))


def test_warehouse_read():

    start = timer()
    project_name = "oralcare"
    wh = Warehouse(engine=path_db_engine, ssn_factory=None)
    df = wh.get_project_data(project_name)
    end = timer()
    elapsed_time = end - start
    print('completed singlethread insert loops in %s sec!' % (elapsed_time))
    print(df)


def test_warehouse_read():

    start = timer()
    project_name = "oralcare"
    wh = Warehouse(engine=path_db_engine, ssn_factory=None)
    df = wh.get_project_data(project_name)
    end = timer()
    elapsed_time = end - start
    print('completed singlethread insert loops in %s sec!' % (elapsed_time))
    print(df)




