from pyramid.response import Response
# import pyramid.httpexceptions as http_exc
import json
from iap.common.security import *
from iap.common.repository.models_managers.admin_manager import IManageAccess
from iap.common.repository.models_managers.access_manager import get_user_by_id


@forbidden_view
def get_users(request):
    try:
        session = request.dbsession
        imanage_access = IManageAccess(ssn=session)

        users = imanage_access.get_users()
        data = []
        for user in users:
            list_user = {'id': user.id,
                         'first_name': 'Mr. Nice',
                         'last_name': 'Mr. Nice',
                         'email': user.email,
                         'active': True}
            data.append(list_user)
    except Exception:
        raise http_exc.HTTPClientError()
    else:
        return Response(json_body=json.dumps(data), content_type='application/json')


@forbidden_view
def get_user_details(request):
    try:
        user_id = request.json_body['data']['user_id']  # user_id:number
        session = request.dbsession
        imanage_access = IManageAccess(ssn=session)

        users = imanage_access.get_users()
        roles = imanage_access.get_user_roles(user_id)

        list_role = []
        for role in roles:
            list_role.append(role.id)
        data = {}
        for user in users:
            if user.id == user_id:
                data.update({'id': user.id,
                             'first_name': 'Mr. Nice',
                             'last_name': 'Mr. Nice',
                             'email': user.email,
                             'active': True,
                             'roles': list_role,
                             'avatar': ''})
                break

    except Exception:
        raise http_exc.HTTPClientError()
    else:
        return Response(json_body=json.dumps(data), content_type='application/json')


@forbidden_view
def reset_password(request):
    try:
        user_id = request.json_body['data']['user_id']  # id: number
        session = request.dbsession
        user = get_user_by_id(session, user_id)

        user.set_password('')
    except Exception:
        raise http_exc.HTTPClientError()
    else:
        return Response(json_body=json.dumps('Success'), content_type='application/json')


@forbidden_view
def add_user(request):
    try:
        create_obj = request.json_body['data']['create_obj']  # create_obj: Object
        email = create_obj['email']
        password = create_obj['password']
        if 'roles' in create_obj:
            roles_id = create_obj['roles']
        else:
            roles_id = []

        session = request.dbsession
        imanage_access = IManageAccess(ssn=session)
        new_user = imanage_access.add_user(email, password, roles_id)

        list_role = []
        for role in new_user.roles:
            if role.id not in list_role:
                list_role.append(role.id)
        data = {'user_id': new_user.id,
                'email': new_user.email,
                'active': True,
                'roles': list_role,
                'avatar': ''}

    except Exception as e:
        if type(e).__name__ == 'AlreadyExistsError':
            raise http_exc.HTTPConflict(' '.join(e.args))
        raise http_exc.HTTPClientError()
    else:
        return Response(json_body=json.dumps(data), content_type='application/json')


@forbidden_view
def edit_user(request):
    try:
        user_id = request.json_body['data']['user_id']  # user_id: number
        changes_obj = request.json_body['data']['changes_obj']  # changes_obj: Object
        session = request.dbsession
        imanage_access = IManageAccess(ssn=session)
        user = get_user_by_id(session, user_id)

        # Change password
        if 'password' in changes_obj:
            user.set_password(changes_obj['password'])

        # Add roles
        if 'roles' in changes_obj:
            for role_id in changes_obj['roles']:
                role = imanage_access.get_role(id=role_id)
                imanage_access.add_role_to_user(user, role)

        user = get_user_by_id(session, user_id)
        list_role = []
        for role in user.roles:
            if role.id not in list_role:
                list_role.append(role.id)
        data = {'user_id': user.id,
                'email': user.email,
                'active': True,
                'roles': list_role,
                'avatar': ''}
    except Exception:
        raise http_exc.HTTPClientError()
    else:
        return Response(json_body=json.dumps(data), content_type='application/json')
