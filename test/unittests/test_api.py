from unittest.mock import Mock

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
