import pytest
import json


def test_index(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "URL Shortener" in res.get_data(as_text=True)
    post_res = client.post("/")
    assert post_res.status_code != 200
    assert "http://127.0.0.1:5000/" in post_res.get_data(as_text=True)


def test_display_short_url(client):
    res = client.get("/display/test1")
    assert res.status_code == 200
    assert "http://127.0.0.1:5000/test1" in post_res.get_data(as_text=True)
