import pytest


def test_get_activities_returns_200_and_payload(client):
    # Arrange: initial activities provided by fixture

    # Act
    response = client.get('/activities')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    # Ensure at least one activity has the expected keys
    for name, info in data.items():
        assert 'participants' in info
        assert 'max_participants' in info
        break


def test_signup_adds_participant(client):
    # Arrange
    activity_name = 'Chess Club'
    email = 'newstudent@example.com'
    before = client.get('/activities').json()[activity_name]['participants']
    initial_count = len(before)

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    data = client.get('/activities').json()
    assert email in data[activity_name]['participants']
    assert len(data[activity_name]['participants']) == initial_count + 1


def test_unregister_removes_participant(client):
    # Arrange
    activity_name = 'Chess Club'
    # ensure there is a participant to remove
    signup_email = 'toremove@example.com'
    client.post(f"/activities/{activity_name}/signup", params={"email": signup_email})
    before = client.get('/activities').json()[activity_name]['participants']
    initial_count = len(before)

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": signup_email})

    # Assert
    assert response.status_code == 200
    data = client.get('/activities').json()
    assert signup_email not in data[activity_name]['participants']
    assert len(data[activity_name]['participants']) == initial_count - 1


def test_signup_nonexistent_activity_returns_404(client):
    # Arrange
    activity_name = 'Nonexistent Club'
    email = 'student@example.com'

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404


def test_unregister_nonexistent_participant_returns_404(client):
    # Arrange
    activity_name = 'Chess Club'
    email = 'notfound@example.com'

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
