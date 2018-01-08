from flask_dev_mark import DevMark
import pytest
from flask import Flask, Response


@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/html")
    def html():
        body = '<html><head><title>test</title></head><body>hello</body></html>'
        return Response(body, 200, content_type='text/html')

    @app.route("/json")
    def json():
        body = '{"message":"hello"}'
        return Response(body, 200, content_type='application/json')

    app.wsgi_app = DevMark(app.wsgi_app, 'development')

    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_dev_mark_html(app, client):
    r = client.get("/html")
    assert r.status_code == 200
    assert r.data.decode("utf-8").count('development') > 0


def test_dev_mark_json(app, client):
    r = client.get("/json")
    assert r.status_code == 200
    assert r.data.decode("utf-8").count('development') == 0
