import requests

BASE_URL = "http://localhost:8000"

def test_valid():
    r = requests.get(f"{BASE_URL}/valid")
    assert r.status_code == 200
    assert r.json()["message"] == "OK - valid request"

def test_bad_request():
    r = requests.get(f"{BASE_URL}/bad-request")
    assert r.status_code == 400
    assert "Bad Request" in r.json()["error"]

def test_server_error():
    r = requests.get(f"{BASE_URL}/server-error")
    assert r.status_code == 500
    assert "Internal Server Error" in r.json()["error"]
