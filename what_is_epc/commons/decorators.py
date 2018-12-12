from functools import wraps

from flask_jwt_extended import current_user

from .exceptions import InsufficientPrivilege


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role not in roles:
                raise InsufficientPrivilege()
            return f(*args, **kwargs)
        return decorated_function
    return decorator
