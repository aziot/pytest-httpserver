
from pytest_httpserver import HTTPServer
import requests


def test_request_handler_calls(httpserver: HTTPServer):
    handler_foo = httpserver.expect_request("/foo").respond_with_data("foo")
    handler_bar = httpserver.expect_request("/foo").respond_with_data("foo")

    assert handler_foo.requests_log == []
    assert handler_foo.responses_log == []

    assert requests.post(httpserver.url_for("/foo"), json={"foo": "bar"}).text == "foo"
    assert requests.post(httpserver.url_for("/foo"), json={"foo": "baz"}).text == "foo"

    assert len(handler_foo.requests_log) == 2
    assert handler_foo.requests_log[0].method == "POST"
    assert handler_foo.requests_log[1].method == "POST"
    assert handler_foo.requests_log.query("data") == [b'{"foo": "bar"}', b'{"foo": "baz"}']
    assert handler_foo.requests_log.data == handler_foo.requests_log.query("data")
    assert handler_foo.requests_log.json == [{"foo": "bar"}, {"foo": "baz"}]

    assert handler_bar.requests_log == []

    assert handler_foo.responses_log[0].status_code == 200
    assert handler_foo.responses_log[1].status_code == 200
