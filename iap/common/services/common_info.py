from iap.common.repository.models.access import Tool, Project


def get_tools_info(req, lang):
    """Get tool's and project
    :param req:
    :type req: pyramid.util.Request
    :param lang:
    :type lang:
    :return:
    :rtype:
    """
    # TODO send tool info in required lang
    tools_info = []
    keys = ['id', 'name', 'description']
    tools = req.dbsession.query(Tool.id, Tool.name, Tool.description).all()
    for tool in tools:

        tool_info = dict(zip(keys, tool))
        tools_info.append(tool_info)

    return tools_info


def get_projects_info(req, lang):
    """
    Get projects info from db
    ToDo - set check acccess for data
    :param req:
    :type req:
    :return:
    :rtype:
    """
    # TODO send tool info in required lang
    projects_info = []
    keys = ['id', 'name', 'description', 'tool_id']

    query = req.dbsession.query(Project.id, Project.name, Project.description, Tool.id)
    query = query.join(Project.pr_tools).all()

    for sub_query in query:
        project_info = dict(zip(keys, sub_query))
        projects_info.append(project_info)
    return projects_info


def get_client_info(storage, user_id, lang=None):
    info = dict(
    name='CompanyASD',
    icon='logo.jpg'
    )
    return info


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
