from ...repository.db.models import Pr_Tool, Project

def get_client_info(storage, user_id, lang=None):
    info = dict(
        name='CompanyASD',
        icon='logo.jpg'
    )
    return info

def _get_user_info(user_id, req):
    #
    pass


def get_user_info(storage, user_id, lang=None):
    info = dict(
        name='Nicolas'
    )
    return info


def get_languages_list(storage, selected_lang_id):
    langs = [
        dict(id='en', name='English', selected=False),
        dict(id='ru', name='Russian', selected=False)]
    found_flag = False
    for l in langs:
        if l['id'] == selected_lang_id:
            l['selected'] = True
            found_flag = True
            break
    if not found_flag:
        langs[0]['selected'] = True
    return langs


def get_tools_info(req):
    tools_info =[]
    tools = req.dbsession.query(Pr_Tool).all()
    for tool in tools:
        if tool.name == "Forecasting":
            id = 'forecast'
        tools_info.append(dict(id=id, name=tool.name, description=tool.description))
    return tools_info


def get_projects_info(req):
    """
    Get projects info from db
    ToDo - set check acccess for data
    :param req:
    :type req:
    :return:
    :rtype:
    """
    projects_info = []
    #request to db
    projects = req.dbsession.query(Project).all()
    for project in projects:
        for tool in project.pr_tools:
            if tool.id == 1:
                tool_id = 'forecast'
            else:
                tool_id = tool.id
            projects_info.append(dict(id=project.id, name=project.name,
                                      description=project.description, tool_id=tool_id))
    return projects_info


def _get_tools_info(storage, tools_ids=None, lang=None):
    """
    Old function for _get tools info

    :param storage:
    :type storage:
    :param tools_ids:
    :type tools_ids:
    :param lang:
    :type lang:
    :return:
    :rtype:
    """
    tools = [dict(
        id='forecast',
        name='Forecasting',
        short_name='Forecasting',
        description='This is forecasting',
        icon='logo.jpg'
    )]
    return tools


def _get_projects_info(starage, projects_ids=None, lang=None):
    """
    Old function for get projects info
        """
    projects = [
        dict(
            id='JJOralCare',
            tool_id='forecast',
            name='Oral Care Forecasting',
            short_name='JJOralCare',
            description='This is oral care'
        ),
        dict(
            id='JJLean',
            tool_id='forecast',
            name='Lean Forecasting',
            short_name='JJLean',
            description='This is lean'
        )
    ]
    return projects
