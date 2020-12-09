from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from src.Booking import BookingError

from server import app, system, auth_manager

from src.Booking import Booking
from src.User import User, Patient, Provider, Admin, UserError

#Go to the home webpage:
@app.route('/')
def home():
    return render_template('home.html')

#Go to the login webpage:
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        if system.login_user(username,password):
            return redirect(url_for('home'))
        elif system.login_admin(username,password):
            return redirect(url_for('home'))
        else: 
            return render_template('login.html',message = "Wrong username or password")
    
    return render_template('login.html')

#Go to the webpage specific to logging in Administrators:
@app.route('/login_admin', methods=['POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        if system.login_admin(username,password):
            return redirect(url_for('home')) 
        else:
            return render_template('login.html')

    return render_template('login.html')

#Go to the logout webpage specific to the 
@app.route('/logout')
@login_required
def logout():
    auth_manager.logout()
    return redirect(url_for('home'))

'''
    Dedicated page for "page not found"
'''
#Display the error HTML webpage (i.e. Page not found )
@app.route('/404')
@app.errorhandler(404)
def page_not_found(e=None):
    return render_template('404.html'), 404

#Display the search_provider HTML webpage:
@app.route('/provider/search', methods=['GET', 'POST'])
@login_required
def provider_search():
    if request.method == 'POST':
        sname = request.form['name']
        stype = request.form['type']
        providers = system.get_search_provider(sname, stype, True)
        if not providers:
            return render_template('search_provider.html', providers=providers)
        return render_template('search_provider.html', providers=providers, name=sname, type=stype)
    providers = system.providers
    return render_template('search_provider.html', providers=providers)

#Display the search_centre HTML webpage:
@app.route('/centre/search', methods=['GET', 'POST'])
@login_required
def centre_search():
    if request.method == 'POST':
        search_method = request.form['search_select']
        search = request.form['search']
        centres = system.get_search_centre(search, search_method, True)
        if not centres:
            return render_template('search_centre.html', centres=None, search_method=search_method, search=search)
        return render_template('search_centre.html', centres=centres, search_method=search_method, search=search)
    centres = system.centres
    return render_template('search_centre.html', centres=centres)

#Go to the webpage specific to the provider:
@app.route('/provider/<name>', methods=['GET', 'POST'])
@login_required
def provider(name):
    provider = system.get_search_provider(name, "", False)
    if not provider:
        abort(404)
    if request.method == 'POST':
        if (request.form['user_rating'] is "" or request.form['user_rating'].isdigit() is False):
            return render_template('provider_details.html', provider=provider, message="Invalid rating")
        rating = float(request.form['user_rating'])
        if rating >= 0 and rating <= 5:
            provider.add_rating(rating)
            message="Rating Submitted"
        else:
            message="Rating Error: Out of 0..5 Range"
        return render_template('provider_details.html', provider=provider, message=message)
    return render_template('provider_details.html', provider=provider, message="")

#Go to the webpage specific to the centre:
@app.route('/centre/<name>', methods=['GET', 'POST'])
@login_required
def centre(name):
    centre = system.get_search_centre(name, "name", False)
    if not centre:
        abort(404)
    if request.method == 'POST':
        if (request.form['user_rating'] is "" or request.form['user_rating'].isdigit() is False):
            return render_template('provider_details.html', provider=provider, message="Invalid rating")
        rating = float(request.form['user_rating'])
        if rating >= 0 and rating <= 5:
            centre.add_rating(rating)
            message="Rating Submitted"
        else:
            message="Rating Error: Out of 0..5 Range"
        return render_template('centre_details.html', centre=centre, message=message)
    return render_template('centre_details.html', centre=centre, message="")

@app.route('/bookings')
@login_required
def get_book():
    bookings_list = system.get_bookings()
    bookings_list.reverse()
    if not bookings_list:
        return render_template('bookings.html', valid_book=False, bookings_list=None)
    return render_template('bookings.html', valid_book=False, bookings_list=bookings_list)

@app.route('/patient/<name>/bookings')
@login_required
def get_patient_book(name):
    if current_user.is_patient():
        abort(404)
    if not current_user.patient_perm(name):
        abort(404)
    patient = system.get_patient(name)
    bookings_list = patient.bookings
    bookings_list.reverse()
    if not bookings_list:
        return render_template('patient_bookings.html', bookings_list=None, patient=name)
    return render_template('patient_bookings.html', bookings_list=bookings_list, patient=name)

@app.route('/patient/<name>/booking/<bdate>/<btime>/view')
@login_required
def get_patient_book_detail(name, bdate, btime):
    if current_user.is_patient():
        abort(404)
    if not current_user.patient_perm(name):
        abort(404)
    patient = system.get_patient(name)
    booking = None
    for books in patient.bookings:
        if books.date == bdate and books.time == btime:
            booking = books
            return render_template('booking_note.html', booking=booking, provider=current_user.username)
    abort(404)

@app.route('/patient/<name>/booking/<bdate>/<btime>/add_prescript', methods=['POST'])
@login_required
def add_prescript(name, bdate, btime):
    if current_user.is_patient():
        abort(404)
    if not current_user.patient_perm(name):
        abort(404)
    patient = system.get_patient(name)
    booking = None
    for books in patient.bookings:
        if books.date == bdate and books.time == btime:
            booking = books
            if request.form['prescript'] != "":
                booking.prescriptions_append(current_user.username, request.form['prescript'])
                return render_template('booking_note.html', booking=booking, provider=current_user.username, message="Prescription Added")
            return render_template('booking_note.html', booking=booking, provider=current_user.username, message="Prescription Added")

@app.route('/patient/<name>/booking/<bdate>/<btime>/add_note', methods=['POST'])
@login_required
def add_note(name, bdate, btime):
    if current_user.is_patient():
        abort(404)
    if not current_user.patient_perm(name):
        abort(404)
    patient = system.get_patient(name)
    booking = None
    for books in patient.bookings:
        if books.date == bdate and books.time == btime:
            booking = books
            if request.form['note'] != "":
                booking.notes_append(current_user.username, request.form['note'])
                return render_template('booking_note.html', booking=booking, provider=current_user.username, message="Note Added")
            return render_template('booking_note.html', booking=booking, provider=current_user.username, message="")

@app.route('/<provider>/book', methods=['GET', 'POST'])
@login_required
def make_book(provider):
    patient = current_user.username
    mprovider = system.get_search_provider(provider, "", False)
    if not mprovider:
        abort(404)
    if current_user.is_provider():
        return render_template('message.html', message="A provider can't book with a provider")  
    if request.method == 'POST':
        #Get time from HTML form:
        time = request.form['btime']
 
        #Split time into minutes and hours:
        minutes = time[-2:]
        hours = time[:2]
        
        if (minutes is ""):
            minutes = "00"
        
        if (minutes[0] is "0"):
            minutes = minutes[1]
        
        if (hours is ""):
            hours = "00"
        
        if (hours[0] == "0"):
            hours = hours[1]
        
        minutes = int(minutes)
        hours = int(hours)
        
        if (minutes%30 != 0 or hours < 8 or hours > 20):
            err = "Invalid booking time {}".format(time)
            return render_template('make_booking.html', patient=patient, provider=mprovider, message=err)
    
        if mprovider.appointment_present(request.form['bdate'], request.form['btime']):
            return render_template('make_booking.html', patient=patient, provider=mprovider, message="Appointment Time Taken")

        try:    
            system.make_booking(Booking(mprovider.username, request.form['bdate'], request.form['btime'], patient, request.form['booking_msg']))
        except BookingError as err:
            return render_template('make_booking.html', patient=patient, provider=mprovider, message=str(err))
        else:
            current_user.append_bookings(Booking(mprovider.username, request.form['bdate'], request.form['btime'], patient, request.form['booking_msg']))
            mprovider.append_bookings(Booking(mprovider.username, request.form['bdate'], request.form['btime'], patient, request.form['booking_msg']))
            mprovider.add_appointment(request.form['bdate'], request.form['btime'])
            if not mprovider.patient_perm(current_user.username):
                mprovider.patient_perm_append(current_user.username)
            system.pickle_save_booking()
            system.pickle_save_providers()
            system.pickle_save_patients()
            return render_template('make_booking.html', patient=patient, provider=mprovider, message="Booking Successful")
    return render_template('make_booking.html', patient=patient, provider=mprovider, message="")

# gets profile to display to user
@app.route('/profile', methods=['GET'])
@login_required
def get_profile():
    user = current_user
    if not user:
        abort(404)
    if user.is_admin():
        return render_template('admin_profile.html')
    if not user:
        abort(404)
    return render_template('profile_page.html', user=user)

# edits profile to display to user
@app.route('/profile/edit', methods=['GET','POST'])
@login_required
def edit_profile():
    user = current_user
    if not user:
        abort(404)
    if request.method == 'POST':
        try:
            user.username = request.form['username']
            user.email = request.form['email']
            user.phone_no = request.form['phone_no']
        except UserError as err:
            return render_template('edit_profile_page.html', user=user, message=str(err))     
        if user.is_provider():
            try:
                user.provider_type = request.form['prov_type']
                user.prov_num = request.form['prov_no']
            except UserError as err:
                return render_template('edit_profile_page.html', user=user, message=str(err))        
        elif user.is_patient():
            try:
                user.medi_num = request.form['medi_num']
            except UserError as err:
                return render_template('edit_profile_page.html', user=user, message=str(err))        
        return render_template('edit_profile_page.html', user=user, message="Change Successful")
    return render_template('edit_profile_page.html', user=user, message="")

# simple shutdown by Armin Ronacher (2011/08/29) from "flask.pocoo.org"
# additional code is of my creation (z5208931)
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

# shutdown app route    
@app.route('/shutdown', methods=['GET'])
@auth_manager.admin_required
def server_shutdown():
    system.pickle_save_booking()
    system.pickle_save_providers()
    system.pickle_save_patients()
    system.pickle_save_centres()
    shutdown_server()
    return 'Server is shutting down...'
