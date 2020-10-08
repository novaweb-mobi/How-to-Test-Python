from nova_api.dao.generic_sql_dao import GenericSQLDAO
from nova_api.persistence.postgresql_helper import PostgreSQLHelper

from User import User


class UserDAO(GenericSQLDAO):
    def __init__(self, **kwargs):
        super(UserDAO, self).__init__(database_type=PostgreSQLHelper,
                                      return_class=User,
                                      **kwargs)