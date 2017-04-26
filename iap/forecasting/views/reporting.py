from iap.common import runtime_storage as rt
from iap.common.security import *
from iap.common.repository.models_managers.access_manager import build_permission_tree
from iap.forecasting.workbench.services import reporting
from iap.forecasting.services.scenario_service import get_scenarios, get_scenario_details
import json
import pyramid.httpexceptions as http_exc
from pyramid.response import Response


@forbidden_view
def get_report_options(request):
    """Get report options for user

    :param request:
    :type request:
    :return:
    :rtype:
    """
    try:
        user_id = request.user
    except KeyError:
        raise http_exc.HTTPUnauthorized()
    try:
        # project = rt.get_state(user_id)._project_id
        wb = rt.get_wb(user_id)
        session = request.dbsession
        scenarios = get_scenarios(session, user_id, None)
        for scenario in scenarios:
            scenario['details'] = get_scenario_details(session, user_id, scenario['id'])

        data = reporting.get_options_data(config=wb.data_config, scenarios=scenarios)
    except Exception:
        raise http_exc.HTTPClientError()
    else:
        return Response(json_body=json.dumps(data), content_type='application/json')


@forbidden_view
def generate_report(request):
    """Generate report and save it to specified address

    :param request: request.json_body['data']['file_name']
    :type request:
    :return:
    :rtype:
    """
    try:
        user_id = request.user
        lang = rt.language(user_id)
    except KeyError:
        raise http_exc.HTTPUnauthorized()
    try:
        project = rt.get_state(user_id)._project_id
        # TODO remove test project
        if project is None:
            project = request.json_body['data']['project']
            rt.update_state(user_id, tool_id='forecast', project_id=project)
        wb = rt.get_wb(user_id)
        session = request.dbsession
        permission_tree = build_permission_tree(session, project_name=project)
        scenarios = get_scenarios(session, user_id, None)
        for scenario in scenarios:
            scenario['details'] = get_scenario_details(session, user_id, scenario['id'])

        options = reporting.get_options_data(config=wb.data_config, scenarios=scenarios)
        data = reporting.collect_report_data(options=options, permission_tree=permission_tree,
                                             container=wb.default_container, config=wb.data_config,
                                             entities_ids=wb.selection, lang=lang)
        reporting.create_report(request.json_body['data']['file_name'], data)

    except Exception:
        raise http_exc.HTTPClientError()
    else:
        return Response(json_body=json.dumps('Success'), content_type='application/json')
