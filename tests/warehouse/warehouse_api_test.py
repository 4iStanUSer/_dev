import logging
import logging.config

from iap.data_loading.loading_lib import warehouse_api


def test_create_project():

    logger = logging.getLogger(__name__)

    # create a file handler
    info_handler = logging.FileHandler('info.log')
    info_handler.setLevel(logging.INFO)

    warnign_handler = logging.FileHandler('warning.log')
    warnign_handler.setLevel(logging.WARNING)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    warnign_handler.setFormatter(formatter)
    info_handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(info_handler)
    logger.addHandler(warnign_handler)


    name = "JJOLean"

    logger.info("Started new project {0}".format(name))
    project = warehouse_api.Project(name=name)

    entity_1 = warehouse_api.Entity(path=['Canada', 'Mouthwash'])
    project.add_entity(entity=entity_1)
    logging.info("Added entity {1} to new project {0}".
                format(name, ['Canada', 'Mouthwash']))

    variable_1 = warehouse_api.Variable(name="PricePromo")
    entity_1.add_var(variable_1)


    entity_2 = warehouse_api.Entity(path = ['USA', 'Mouthwash'])

    project.add_entity(entity=entity_2)
    logger.info("Added entity {1} to new project {0}".
                format(name, ['USA', 'Mouthwash']))

    variable_2 = warehouse_api.Variable(name ="Dynamics")
    entity_2.add_var(var=variable_2)

    time_serie = warehouse_api.TimeSeries(name="annual")
    time_serie.set_by_index(start_index=0, len=10,
                            values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    variable_2.add_time_serie(time_serie=time_serie)

    try:
        time_serie = warehouse_api.TimeSeries(name=[1, 2, 3, 4, 5],
                                              values="annual")

    except TypeError:
        logger.warning("Unexpected input")
    entity_3 = warehouse_api.Entity(path =['Poland', 'Mouthwash'])
    project.add_entity(entity=entity_3)
    logger.info("Added entity {1} to new project {0}".format(name,
                                                    ['Poland', 'Mouthwash']))

    project.save()


def test_read_data_from_project():
    project = warehouse_api.Project("JJOLean")
    project.read()
    print("Project", project)
    print("Ent", project.entities)
    print("Ent USA*Mouthwash", project.entities['USA*Mouthwash'].vars)
    print("Ent USA*Mouthwash", project.entities['USA*Mouthwash'].
          vars['Dynamics'].time_series['annual'].timeserie)
    project.save()

