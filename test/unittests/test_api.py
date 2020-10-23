from datetime import datetime
from unittest.mock import Mock

from pytest import fixture, mark

from User import User
from app import user_api

from nova_api import auth


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

    def test_generate_token(self, mocker):
        user = User(id_="00000000000000000000000000000000", name="MyName",
                    email="MyEmail@mymail.com", birthday = "10/10/1998")

        iat = mocker.patch('app.user_api.datetime')
        iat.utcnow.return_value = datetime(2018, 1, 18, 1, 30, 22, 00000)

        token = user_api.generate_token(user)

        assert token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1" \
                        "MTYyMzkwMjIsImV4cCI6IjE1MTYyNDAyMjIiLCJpc3MiOiJtb" \
                        "2JpLm5vdmF3ZWIubXlsb2dpbmFwaSIsInN1YiI6IjAwMDAwMD" \
                        "AwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwIiwibmFtZSI6Ik1" \
                        "5TmFtZSJ9.9Qb7sQ4WhoJKitKXnFo8jvdxOyLnFblk1OY-KFS" \
                        "I0Uk"

