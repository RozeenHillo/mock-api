import requests

BASE_URL = "http://localhost:8000"


def test_health_ok():
    r = requests.get(f"{BASE_URL}/health", timeout=5)
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_valid_200():
    r = requests.get(f"{BASE_URL}/mock", params={"mode": "valid"}, timeout=5)
    assert r.status_code == 200
    assert r.json()["result"] == "success"


def test_bad_400():
    r = requests.get(f"{BASE_URL}/mock", params={"mode": "bad"}, timeout=5)
    assert r.status_code == 400
    body = r.json()
    assert body["error"] == "Bad Request"


def test_error_500():
    r = requests.get(f"{BASE_URL}/mock", params={"mode": "error"}, timeout=5)
    assert r.status_code == 500
    body = r.json()
    assert body["error"] == "Internal Server Error"
