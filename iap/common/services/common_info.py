

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


def get_tools_info(storage, tools_ids=None, lang=None):
    tools = [dict(
        id='forecast',
        name='Forecasting',
        short_name='Forecasting',
        description='This is forecasting',
        icon='logo.jpg'
    )]
    return tools


def get_projects_info(starage, projects_ids=None, lang=None):
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
