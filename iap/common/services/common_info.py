

def get_client_info(storage, user_id, lang=None):
    info = dict(
        company_name='CompanyASD',
        company_logo='logo.jpg'
    )
    return info


def get_user_info(storage, user_id, lang=None):
    info = dict(
        user_name='Nicolas'
    )
    return info


def get_languages_list(storage):
    langs = [
        dict(id='en', name='English'),
        dict(id='ru', name='Russian')
    ]
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
            description='This is forecasting'
        ),
        dict(
            id='JJLean',
            tool_id='forecast',
            name='Lean Forecasting',
            short_name='JJLean',
            description='This is forecasting'
        )
    ]
    return projects
