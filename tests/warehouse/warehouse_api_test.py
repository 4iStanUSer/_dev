from iap.common.repository.models_managers.warehouse import Warehouse
import pandas as pd
import pytest
from timeit import default_timer as timer
from iap.common.repository.interface.warehouse_api import warehouse_api, iwarehouse


def test_create_project():

    name = "JJOLean"
    project = warehouse_api.Project(name=name)

    entity_1 = warehouse_api.Entity(path = ['Canada', 'Mouthwash'])
    project.add_entity(entity=entity_1)

    variable_1 = warehouse_api.Variable(name = "PricePromo")
    entity_1.add_var(variable_1)


    entity_2 = warehouse_api.Entity(path = ['USA', 'Mouthwash'])
    project.add_entity(entity=entity_2)

    variable_2 = warehouse_api.Variable(name = "Dynamics")
    entity_2.add_var(var=variable_2)

    time_serie = warehouse_api.TimeSeries(name="annual")
    time_serie.set_by_index(start_index=0, len=10, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    variable_2.add_time_serie(time_serie=time_serie)

    entity_3 = warehouse_api.Entity(path =['Poland', 'Mouthwash'])
    project.add_entity(entity=entity_3)

    project.save()


def test_read_data_from_project():
    project = warehouse_api.Project("JJOLean")
    project.read()
    project.save()

