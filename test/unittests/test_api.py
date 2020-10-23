from unittest.mock import Mock

from pytest import fixture

from User import User
from app import user_api


class TestAPI:
    @fixture
    def success_response(self, mocker):
        success_response = mocker.patch("app.user_api.success_response")
        success_response.side_effect = lambda message, data: (message, data)

    def test_probe_ok(self, success_response):
        dao_mock = Mock()
        dao_mock.get_all.return_value = 0, []

        a = user_api.probe.__wrapped__(dao=dao_mock)
        print(dao_mock.mock_calls)
        assert a == ('API Ready', {'available': 0})

    def test_read_no_filter(self, success_response):
        users = [User(name="MyName"), User(name="OtherName")]

        dao_mock = Mock()
        dao_mock.get_all.return_value = len(users), users

        a = user_api.read.__wrapped__(dao=dao_mock)

        assert dao_mock.get_all.called_with(length=20, offset=0, filters=None)
        assert a == ('List of user', {"total": len(users),
                                      "results": [dict(user)
                                                  for user
                                                  in users]})
