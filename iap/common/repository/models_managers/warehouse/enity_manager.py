from iap.common.repository import exceptions as ex
from iap.common.repository.models.warehouse import Entity, Variable
from sqlalchemy.orm.exc import NoResultFound
import enum

class DataType(enum.IntEnum):
    float = 0
    int = 1
    string = 2


def get_default_value(type_index):
    if type_index == DataType.float:
        return 0.0
    if type_index == DataType.int:
        return 0
    if type_index == DataType.string:
        return ''


def cast_value(type_index, value):
    if type_index == DataType.float:
        return float(value)
    if type_index == DataType.int:
        return int(value)
    if type_index == DataType.string:
        return str(value)

def add_child(session, entity, name, meta):
    """
    Add child to entity
    :param session:
    :type session:
    :param entity_id:
    :type entity_id:
    :param name:
    :type name:
    :param meta:
    :type meta:
    :return:
    :rtype:
    """
    try:
        for child in entity.children:
            if child.name == name:
                return child
        new_child = Entity(_name=name, _dimension_name=meta[0], _layer=meta[1])
        entity.children.append(new_child)
    except NoResultFound:
        return None
    else:
        return new_child


def get_child(session, entity_id,  name):
    try:
        entity = session.Entity.filter(Entity.id == entity_id).one()
        for child in entity.children:
            if child.name == name:
                result = child
            else:
                result = None
    except NoResultFound:
        return None
    else:
        return result


def _add_node_by_path(session, entity, path, meta, depth):

    #try:
    print("Entity", entity)
    print("Path", path)
    #entity = session.query(Entity).filter(Entity.id == entity_id).one_or_none()
    node = None
    for child in entity.children:
        if child.name == path[depth]:
            node = child
            break
    if node is None:
        node = add_child(session, entity, path[depth], meta[depth])
    if depth != len(path) - 1:
        return _add_node_by_path(session, node.id, path, meta, depth + 1)
    else:
        return node
    #except AttributeError:
    #    return None
    #except NoResultFound:
    #    return None


def _find_node_by_path(session, entity_id, path, depth):
    try:
        entity = session.query(Entity).filter(Entity.id == entity_id).one()
        node = None
        for child in entity.children:
            if child.name == path[depth]:
                node = child
                break
        if node is None:
            return None
        if depth != len(path) - 1:
            return _find_node_by_path(session, node.id, path, depth + 1)
        else:
            return node
    except NoResultFound:
        return None


def _get_root(session, entity_id):
    try:
        entity = session.Entity.filter(Entity.id == entity_id).one()
        if entity.name == 'root':
            return entity
        for parent in entity.parents:
            return parent._get_root(session, parent.id)
    except NoResultFound:
        raise ex.NotFoundError('Entity', 'root', 'root', '', '_get_root')


def _get_path(session, entity_id, path):
    try:
        entity = session.Entity.filter(Entity.id == entity_id).one()
        if entity.name == 'root':
            return
        path.insert(0, entity.name)
        if entity.parent is not None:
            _get_path(session, entity.parent.id, path)
    except NoResultFound:
        return None


def _get_path_meta(session, entity_id, path_meta):
    try:
        entity = session.Entity.filter(Entity.id == entity_id).one()
        if entity.name == 'root':
            return
        path_meta.insert(0, entity.meta)
        if entity.parent is not None:
            _get_path_meta(session, entity.parent.id, path_meta)
    except NoResultFound:
        return None


def get_variables_names(session, entity_id):
    try:
        entity = session.Entity.filter(Entity.id == entity_id).one()
        return [x.name for x in entity._variables]
    except NoResultFound:
        return None

def get_variable(session, entity_id, name):
    try:
        entity = session.Entity.filter(Entity.id == entity_id).one()
        for var in entity._variables:
            if var.name == name:
                return var
        return None
    except NoResultFound:
        return None


def force_variable(session, entity_id, name, data_type, default_value=None):
    # Check if variable with the name already exists.
    try:
        entity = session.Entity.filter(Entity.id == entity_id).one()
        for var in entity._variables:
            if var.name == name:
                return var
        type_enum = DataType[data_type]
    except KeyError:
        raise ex.NotFoundError('DataType', 'DataType', data_type,
                               'Not found value in dict by key',
                               'force_variable')
    # Validate default value.
    if default_value is not None:
        try:
            cast_value(type_enum, default_value)
        except ValueError:
            raise ex.WrongValueError(default_value, type_enum,
                                     'Value not from enum',
                                     'force_variable')
    else:
        default_value = get_default_value(type_enum)
    # Create new variable.
    new_var = Variable(_name=name, _data_type=type_enum.value,
                       _default_value=default_value)
    entity._variables.append(new_var)
    return new_var


def get_var_values(self):
    pass