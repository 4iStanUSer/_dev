from .. import exceptions as ex


def get_int_id_or_err(value, name):
    try:
        integer = int(value)
        if integer < 1:
            raise ex.WrongArgEx(name, value)
        return integer
    except TypeError:
        raise ex.EmptyInputsError(name)
    except ValueError:
        raise ex.WrongArgEx(name, value)


def get_str_or_err(value, name):
    try:
        if not isinstance(value, str) or len(value) == 0:
            raise ex.WrongArgEx(name, value)
        return value
    except TypeError:
        raise ex.EmptyInputsError(name)
    except ValueError:
        raise ex.WrongArgEx(name, value)
