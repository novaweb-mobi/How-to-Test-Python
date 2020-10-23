from unittest.mock import Mock

from pytest import fixture, mark

from User import User
from app import user_api


class TestAPI:
    @fixture
    def success_response(self, mocker):
        success_response = mocker.patch("app.user_api.success_response")
        success_response.side_effect = lambda message, data: (message, data)
        return success_response

    @fixture
    def dao_mock(self):
        return Mock()

    def test_probe_ok(self, success_response, dao_mock):
        dao_mock.get_all.return_value = 0, []

        a = user_api.probe.__wrapped__(dao=dao_mock)
        print(dao_mock.mock_calls)
        assert a == ('API Ready', {'available': 0})

    def test_read_no_filter(self, success_response, dao_mock):
        users = [User(name="MyName"), User(name="OtherName")]

        dao_mock.get_all.return_value = len(users), users

        a = user_api.read.__wrapped__(dao=dao_mock)

        assert dao_mock.get_all.called_with(length=20, offset=0, filters=None)
        assert a == ('List of user', {"total": len(users),
                                      "results": [dict(user)
                                                  for user
                                                  in users]})

    @mark.parametrize("length, offset, kwargs, filters", [
        (10, 0, {"name": "MyName"}, {"name": "MyName"}),
        (70, 0, {}, None),
        (2, 0, {"name": "LIKE,My%"}, {"name": ["LIKE", "My%"]})
    ])
    def test_read_with_params(self, success_response, dao_mock,
                              length, offset, kwargs, filters):
        users = [User(name="MyName"), User(name="OtherName")]

        dao_mock.get_all.return_value = len(users), users

        a = user_api.read.__wrapped__(length=length, offset=offset,
                                      dao=dao_mock, **kwargs)

        assert dao_mock.get_all.called_with(length=length, offset=offset,
                                            filters=filters)
        assert a == ('List of user', {"total": len(users),
                                      "results": [dict(user)
                                                  for user
                                                  in users]})
