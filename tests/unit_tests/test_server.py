from server import (SUCCESS_MESSAGE, INSUFFICIENT_POINTS, BOOKING_LIMIT_12_PLACES_MESSAGE,
                    NEGATIVE_POINTS, BOOKING_MORE_THAN_AVAILABLE, clubs, competitions)

club_name = clubs[0]["name"]
club_email = clubs[0]["email"]
club_points = int(clubs[0]["points"])
competition_name = competitions[0]["name"]
numberOfPlaces = competitions[0]["numberOfPlaces"]


# Email tests
def test_valid_email(test_client):
    response = test_client.post("/showSummary", data={"email": club_email})
    data = response.data.decode()
    assert "Welcome" in data


def test_invalid_email(test_client):
    response = test_client.post("/showSummary", data={"email": "invalid@email.com"})
    data = response.data.decode()
    assert "Invalid email !" in data


# Book
# affiche une page booking.html pour un club ou une compétition valide
def test_valide_club_and_competition(test_client):
    response = test_client.get(f"/book/{competition_name}/{club_name}")
    data = response.data.decode()
    assert "How many places?" in data


"""def test_invalide_club_and_competition(test_client):
    competition_name = "te"
    club_name = "te"
    response = test_client.get(f"/book/{competition_name}/{club_name}")
    data = response.data.decode()
    assert "Something went wrong-please try again" in data"""


# Booking tests
def test_successful_booking_with_enough_points(test_client):
    # Faire une réservation avec suffisamment de points
    response = test_client.post(
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


def test_unsuccessful_booking_with_insufficient_points(test_client):
    # Tenter une réservation avec un montant de points insuffisant
    wrong_amount_of_points = club_points + 1
    response = test_client.post(
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

def test_club_points_refresh_after_booking(test_client):
    booked_places = 2
    response = test_client.post(
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
def test_booking_12_places_or_less(test_client):
    response = test_client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": 4,
        },
    )

    data = response.data.decode()
    assert SUCCESS_MESSAGE in data


def test_booking_over_12_places(test_client):
    booked_places = 13
    response = test_client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": booked_places,
        },
    )

    data = response.data.decode()
    assert BOOKING_LIMIT_12_PLACES_MESSAGE in data


# negative places not allowed
def test_booking_negative_places(test_client):
    booked_places = -2
    response = test_client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": booked_places,
        },
    )

    data = response.data.decode()
    assert NEGATIVE_POINTS in data


# BOOKING_MORE_THAN_AVAILABLE

def test_booking_more_than_available(test_client):

    # Définissez un nombre de places supérieur à la capacité disponible
    places_to_book = int(numberOfPlaces) + 1

    response = test_client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": places_to_book,
        },
    )

    data = response.data.decode()
    assert BOOKING_MORE_THAN_AVAILABLE in data
