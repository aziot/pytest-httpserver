
from pytest_httpserver import HTTPServer
from pytest_mock import MockerFixture
import requests


def test_mock(mocker: MockerFixture, httpserver: HTTPServer):
    handler_foo = httpserver.expect_request("/foo").respond_with_data("foo")
    m = mocker.patch.object(handler_foo, "respond", wraps=handler_foo.respond)

    assert requests.post(httpserver.url_for("/foo"), data=b"request_data").text == "foo"
    m.assert_called_once()
    print(m.call_args[0][0].data == b"request_data")
    httpserver.check_assertions()
