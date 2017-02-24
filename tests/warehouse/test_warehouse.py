from iap.common.repository.models_managers.warehouse import Warehouse
import pandas as pd
from timeit import default_timer as timer
from sqlalchemy import create_engine

path_db_engine = "sqlite:///C:/Users/Alex/Desktop/iap/IAP.sqlite"
path_to_files = "C:/Users/Alex/Desktop/iap/data_storage/data_lake" \
                "/JJOralCare/JJOralCare_Sales.csv"
path_to_files = "C:/Users/Alex/Desktop/airbnb_usa_top_cities_by_population.json"

def test_warehouse_write():

    start = timer()
    wh = Warehouse(engine=path_db_engine, ssn_factory=None)
    project_name = "oralcare"
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




