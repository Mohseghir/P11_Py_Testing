from server import SUCCESS_MESSAGE, INSUFFICIENT_POINTS, BOOKING_LIMIT_12_PLACES_MESSAGE, NEGATIVE_POINTS, \
    BOOKING_MORE_THAN_AVAILABLE, clubs, competitions
"""
scenario:
# Template index.html 
# Template Welcome.html
# Template booking.html
# Test successful booking with enough pointss
"""


def test_integration_flow(test_client):
    club_name = clubs[0]["name"]
    club_email = clubs[0]["email"]
    competition_name = competitions[0]["name"]

    # Template index.html
    response = test_client.get("/")
    data = response.data.decode()
    assert "Please enter your secretary email to continue" in data

    # Template Welcome.html
    response = test_client.post("/showSummary", data={"email": club_email})
    data = response.data.decode()
    assert "Welcome" in data

    # Template booking.html
    response = test_client.get(f"/book/{competition_name}/{club_name}")
    assert "How many places?" in response.data.decode()

    # Test successful booking with enough points
    response = test_client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": 1,
        },
    )
    data = response.data.decode()
    assert SUCCESS_MESSAGE in data

