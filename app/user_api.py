from datetime import datetime, timedelta

import nova_api
from flask import Response
from jose import jwt
from nova_api.dao.generic_sql_dao import GenericSQLDAO
from nova_api import error_response, success_response, use_dao

from UserDAO import UserDAO
from User import User


@use_dao(UserDAO, "API Unavailable")
def probe(dao: GenericSQLDAO = None):
    total, _ = dao.get_all(length=1, offset=0, filters=None)
    return success_response(message="API Ready",
                            data={"available": total})


@use_dao(UserDAO, "Unable to list user")
def read(length: int = 20, offset: int = 0,
         dao: GenericSQLDAO = None, **kwargs):
    for key, value in kwargs.items():
        kwargs[key] = value.split(',') \
            if len(value.split(',')) > 1 \
            else value
    total, results = dao.get_all(length=length, offset=offset,
                                 filters=kwargs if len(kwargs) > 0 else None)
    return success_response(message="List of user",
                            data={"total": total, "results": [dict(result)
                                                              for result
                                                              in results]})


@use_dao(UserDAO, "Unable to retrieve user")
def read_one(id_: str, dao: GenericSQLDAO = None):
    result = dao.get(id_=id_)

    if not result:
        return success_response(status_code=404,
                                message="User not found in database",
                                data={"id_": id_})

    return success_response(message="User retrieved",
                            data={"User": dict(result)})


@use_dao(UserDAO, "Unable to create user")
def create(entity: dict, dao: GenericSQLDAO = None):
    entity_to_create = User(**entity)

    dao.create(entity=entity_to_create)

    return success_response(message="User created",
                            data={"User": dict(entity_to_create)})


@use_dao(UserDAO, "Unable to update user")
def update(id_: str, entity: dict, dao: GenericSQLDAO = None):
    entity_to_update = dao.get(id_)

    if not entity_to_update:
        return error_response(status_code=404,
                              message="User not found",
                              data={"id_": id_})

    entity_fields = dao.fields.keys()

    for key, value in entity.items():
        if key not in entity_fields:
            raise KeyError("{key} not in {entity}"
                           .format(key=key,
                                   entity=dao.return_class))

        entity_to_update.__dict__[key] = value

    dao.update(entity_to_update)

    return success_response(message="User updated",
                            data={"User": dict(entity_to_update)})


@use_dao(UserDAO, "Unable to delete user")
def delete(id_: str, dao: GenericSQLDAO):
    entity = dao.get(id_=id_)

    if not entity:
        return error_response(status_code=404,
                              message="User not found",
                              data={"id_": id_})

    dao.remove(entity)

    return success_response(message="User deleted",
                            data={"User": dict(entity)})


@use_dao(UserDAO, "Unable to Login")
def login(id_: str, name: str) -> Response:
    """Verifies the user name and generates a session token if valid

    :param id_: ID of the user trying to login
    :param name: Name inputted by user to verify
    :return: Success response with token if name is valid or Error response.
    """
    pass


def generate_token(user: User, *, iss: str = "mobi.novaweb.myloginapi",
                   exp: float = 20.0) -> str:
    """Generates a JWT token for the specified user.

    Includes sub as user id and name as user name in the claims. Default \
    lifetime is 20 minutes and default iss is "mobi.novaweb.myloginapi".

    :param user: The user to generate token to
    :param iss: The issuer of the token.
    :param exp: Lifetime of the token in minutes.
    :return: JWT encoded token signed with HSA256
    """
    if not isinstance(user, User) or not isinstance(iss, str) \
            or not isinstance(exp, float):
        raise ValueError("Invalid parameters!")

    now = datetime.utcnow()
    claims = {
        "iat": now,
        "exp": now + timedelta(minutes=exp),
        "iss": iss,
        "sub": user.id_,
        "name": user.name
    }
    print(claims)
    return jwt.encode(claims, key=nova_api.JWT_SECRET)

