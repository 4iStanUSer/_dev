from pyramid.httpexceptions import HTTPFound
from pyramid.security import forget
from pyramid.renderers import render_to_response


def notfound_view(req):
    req.response.status = 404
    return render_to_response('templates/404.jinja2',
                              {'title': '404 Not Found'},
                              request=req)


def forbidden_view(req):
    next_url = req.route_url('common.login', _query={'next': req.url})
    return HTTPFound(location=next_url)


def login_view(request):
    next_url = request.params.get('next', request.referrer)
    if not next_url:
        next_url = request.route_url('common.index')
    message = ''
    email = ''
    data = dict(
        message=message,
        url=request.route_url('common.login'),
        next_url=next_url,
        email=email,
    )
    return render_to_response('templates/login.jinja2',
                              data,
                              request=request)


def logout_view(request):
    headers = forget(request)
    next_url = request.route_url('common.login')
    return HTTPFound(location=next_url, headers=headers)


def index_view(req):
    # user = req.user
    # if user is None:
    #    raise HTTPForbidden

    # service.recreate_db(req)
    # service.fillin_db(req)

    #user_id = 1
    #tool_name = forecast_tool_name
    # TODO(1.0) - REMOVE
    #try:
        #wb = run_time_collection.get(user_id)
    #except runTimeEx.BackupNotFound as error:
        # TODO(1.0) - Move this
    #i_access = get_access_interface(ssn=req.dbsession)
    #i_man_acc = get_manage_access_interface(ssn=req.dbsession)
    #user_roles = i_man_acc.get_user_roles(user_id)
    #user_roles_id = [x.id for x in user_roles]

    # Load into RAM
    #wb = Workbench(user_id)
    #warehouse = get_wh_interface()

    #wb.init_load(warehouse, i_access, dev_template)
    #run_time_collection.add(user_id, wb)

    # Save into storage
    #new_backup = wb.get_data_for_backup()
    #s = Storage()
    #s.save_backup(user_id, tool_name, new_backup, 'default')

    return render_to_response('iap.common:templates/index.jinja2',
                              {'title': 'Home page'},
                              request=req)


