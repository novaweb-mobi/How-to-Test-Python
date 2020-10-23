from unittest.mock import Mock

from User import User
from app import user_api


class TestAPI:
    def test_probe_ok(self, mocker):
        success_response = mocker.patch("app.user_api.success_response")
        success_response.side_effect = lambda message, data: (message, data)

        dao_mock = Mock()
        dao_mock.get_all.return_value = 0, []

        a = user_api.probe.__wrapped__(dao=dao_mock)
        print(dao_mock.mock_calls)
        assert a == ('API Ready', {'available': 0})

    def test_read(self, mocker):
        success_response = mocker.patch("app.user_api.success_response")
        success_response.side_effect = lambda message, data: (message, data)

        users = [User(name="MyName"), User(name="OtherName")]

        dao_mock = Mock()
        dao_mock.get_all.return_value = len(users), users

        a = user_api.read.__wrapped__(dao=dao_mock)

        assert a == ('List of user', {"total": len(users),
                                      "results": [dict(user)
                                                  for user
                                                  in users]})
