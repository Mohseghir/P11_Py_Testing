from server import (SUCCESS_MESSAGE, INSUFFICIENT_POINTS, BOOKING_limit_12_PLACES_MESSAGE, clubs, competitions)

club_name = clubs[0]["name"]
club_email = clubs[0]["email"]
club_points = int(clubs[0]["points"])
competition_name = competitions[0]["name"]


# Email tests
def test_valid_email(client):
    response = client.post("/showSummary", data={"email": club_email})
    data = response.data.decode()
    assert "Welcome" in data


def test_invalid_email(client):
    response = client.post("/showSummary", data={"email": "invalid@email.com"})
    data = response.data.decode()
    assert "Invalid email !" in data


# Booking tests
def test_successful_booking_with_enough_points(client):
    # Faire une réservation avec suffisamment de points
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": 1,
        },
    )

    # Vérifier que le message de réussite est présent dans la réponse
    data = response.data.decode()
    assert SUCCESS_MESSAGE in data


def test_unsuccessful_booking_with_insufficient_points(client):
    # Tenter une réservation avec un montant de points insuffisant
    wrong_amount_of_points = club_points + 1
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions[0]["name"],
            "club": clubs[0]["name"],
            "places": wrong_amount_of_points,
        },
    )

    # Vérifier que le message d'insuffisance de points est présent dans la réponse
    data = response.data.decode()
    assert INSUFFICIENT_POINTS in data


# point refresh

def test_club_points_refresh_after_booking(client):
    booked_places = 2
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": booked_places,
        },
    )

    data = response.data.decode()
    assert data.find(f"Points available: {club_points - booked_places}")


# 12 places limit
def test_booking_12_places_or_less(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": 4,
        },
    )

    data = response.data.decode()
    assert SUCCESS_MESSAGE in data


def test_booking_limit_12_places(client):
    booked_places = 13
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": booked_places,
        },
    )

    data = response.data.decode()
    assert BOOKING_limit_12_PLACES_MESSAGE in data
