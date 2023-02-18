import random

from flask import Flask, render_template, request, redirect

from webdb import *

app = Flask(__name__)


def gets_rides():
    rides = Rides.select().where(
        (Rides.date > datetime.datetime.now().date()) |
        (Rides.date == datetime.datetime.now().date()) & (Rides.hour > datetime.datetime.now().time().strftime(
            "%H:%M:%S"))
    ).order_by(Rides.date, Rides.hour)
    return rides


RIDES = gets_rides()


@app.route("/")
def home_page():
    return render_template("home_page.html")


@app.route("/new_ride", methods=["POST"])
def create_new_ride():
    data = request.json
    name = data.get("name")
    phone = data.get("phone")
    date = data.get("date")
    departure = data.get("departure")
    seats = data.get("seats")
    price = data.get("price")
    hour = data.get("hour")
    destination = data.get("destination")
    while True:
        random_reference = random.randint(100000, 999999)
        if random_reference not in reference_list():
            break
    Rides.create(name=name, phone=phone, date=date, hour=hour, departure=departure, destination=destination,
                 several_places=seats,
                 ride_price=price, reference_num=random_reference)
    return dict(reference=random_reference)


@app.route("/new_ride", methods=["GET"])
def new_ride_page():
    return render_template("new_ride.html")


@app.route("/rides_board", methods=["GET"])
def to_existing_rides():
    return render_template("rides_board.html", rides=gets_rides())


@app.route("/rides_board", methods=["GET", "POST"])
def search_for_ride():
    global RIDES

    if request.form.get("depart_search"):
        RIDES = RIDES.where(Rides.departure == request.form.get("depart_search"))
    if request.form.get("dest_search"):
        RIDES = RIDES.where(Rides.destination == request.form.get("dest_search"))
    if request.form.get("date_search"):
        RIDES = RIDES.where(Rides.date == request.form.get("date_search"))
    if request.form.get("min_time_search") and request.form.get("max_time_search"):
        RIDES = RIDES.where(
            Rides.hour.between(request.form.get("min_time_search"), request.form.get("max_time_search")))
    if request.form.get("min_time_search"):
        RIDES = RIDES.where(request.form.get("min_time_search") < Rides.hour)
    if request.form.get("max_time_search"):
        RIDES = RIDES.where(request.form.get("max_time_search") > Rides.hour)
    return render_template("rides_board.html", rides=RIDES, cities=CITIES)


@app.route("/hello")
def back():
    return redirect("/")


@app.route("/find_ride", methods=["GET"])
def find_ride():
    return render_template("find_ride.html")


@app.route("/ride_update", methods=["POST"])
def update_ride():
    phone_number = request.form.get("uphone")
    reference_nun = request.form.get("ref_num")
    ride = Rides.get_or_none(Rides.phone == phone_number, Rides.reference_num == reference_nun)
    if ride is None:
        error = "Drive Is not exist,please check that the details are correct."
        print("Ride not found")
        return render_template('find_ride.html', error=error)
    else:
        print("exists")
        return render_template("ride_update.html", ride=ride)


@app.route("/update_ride", methods=["POST"])
def update_ride_endpoint():
    button_id = request.form.get('button_id')
    if button_id == '1':
        # Get the form data from the request
        name = request.form.get("name")
        phone = request.form.get("phone")
        date = request.form.get("date")
        hour = request.form.get("hour")
        seats = request.form.get("seats")
        price = request.form.get("price")
        departure = request.form.get("departure")
        destination = request.form.get("destination")

        # Use the ORM to update the ride in the database
        ride = Rides.get_or_none(Rides.phone == phone)
        ride.name = name
        ride.date = date
        ride.hour = hour
        ride.several_places = seats
        ride.ride_price = price
        ride.departure = departure
        ride.destination = destination
        ride.save()

        # redirect the user to the "rides board" page
        return redirect("/rides_board")
    elif button_id == '2':
        print("delete")
        reference_number = request.form.get("reference_number")
        row = Rides.delete().where(Rides.reference_num == reference_number)
        row.execute()
        print(reference_number)
        return redirect("/rides_board")
