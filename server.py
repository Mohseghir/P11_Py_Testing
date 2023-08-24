import json
from flask import Flask, render_template, request, redirect, flash, url_for

SUCCESS_MESSAGE = "Booking successful"
INSUFFICIENT_POINTS = "Insufficient points"
BOOKING_LIMIT_12_PLACES_MESSAGE = "You are not allowed to book more than 12 places!"
NEGATIVE_POINTS = "You are not allowed to introduce negative points"

def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
    except IndexError:
        error_message = "Invalid email !"  # exception pour un email invalid
        return render_template("index.html", error_message=error_message)
    else:
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    club_points = int(club["points"])
    competition_numberOfPlaces = int(competition["numberOfPlaces"])
    placesRequired = int(request.form['places'])
    error = False
    # points négatifs
    if placesRequired < 0:
        flash(NEGATIVE_POINTS)
        error = True

    if placesRequired > club_points:
        flash(INSUFFICIENT_POINTS)
        error = True

    if placesRequired > 12:
        flash(BOOKING_LIMIT_12_PLACES_MESSAGE)
        error = True

    if not error:
        club["points"] = club_points - placesRequired
        competition["numberOfPlaces"] = competition_numberOfPlaces - placesRequired
        flash(SUCCESS_MESSAGE)
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
