from ..db.warehouse import (
    add_entity,
    get_entity_by_id,
    add_time_scale
)


class IWarehouse:

    def add_entity(ssn, path):
        return add_entity(ssn, path)

    def get_entity_by_id(ssn, entity_id):
        return get_entity_by_id(ssn, entity_id)

    def add_time_scale(ssn, name, time_line):
        add_time_scale(ssn, name, time_line)
