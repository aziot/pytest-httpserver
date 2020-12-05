
from pytest_httpserver import HTTPServer
import requests


def test_request_handler_calls(httpserver: HTTPServer):
    handler_foo = httpserver.expect_request("/foo").respond_with_data("foo")
    handler_bar = httpserver.expect_request("/foo").respond_with_data("foo")

    assert handler_foo.calls == []

    assert requests.get(httpserver.url_for("/foo")).text == "foo"
    assert requests.post(httpserver.url_for("/foo")).text == "foo"

    assert len(handler_foo.calls) == 2
    assert handler_foo.calls[0][0] is handler_foo.calls[0].request
    assert handler_foo.calls[0][1] is handler_foo.calls[0].response

    assert handler_foo.calls[0].response.status_code == 200
    assert handler_foo.calls[0].response.get_data() == b"foo"
    assert handler_foo.calls[0].request.method == "GET"
    assert handler_foo.calls[1].response.status_code == 200
    assert handler_foo.calls[1].response.get_data() == b"foo"
    assert handler_foo.calls[1].request.method == "POST"

    assert handler_bar.calls == []
