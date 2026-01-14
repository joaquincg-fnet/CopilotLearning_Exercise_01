import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_cycle():
    activity = "Chess Club"
    email = "unittest_user@example.com"

    # ensure not present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # signup
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # duplicate signup should fail
    resp_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_dup.status_code == 400

    # unregister
    resp_unreg = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp_unreg.status_code == 200
    assert email not in activities[activity]["participants"]


def test_unregister_nonexistent():
    activity = "Chess Club"
    email = "not_in_list@example.com"

    # ensure not present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 404
