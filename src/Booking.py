from datetime import datetime
from flask_login import login_required, current_user
from src.User import User, Patient, Provider, Admin
from src.Notes import *
class BookingError(Exception):
    "Raised when booking details are incorrect"
    pass  
    
class Booking():
	def __init__(self, provider, date, time, patient, reason):
		self._provider = provider
		self._date = date
		self._time = time
		self._patient = patient
		self._reason = reason
		self._notes = []
		self._prescriptions = []
		currentDT = datetime.now()
		date_format = "%Y-%m-%d"
		time_format = "%H:%M"
		if current_user != None:
		    if current_user.is_provider():
		        raise BookingError("A provider can't book with a provider")
		if date == "":
		    raise BookingError("Specify a date")
		if time == "":
		    raise BookingError("Specify a time")     
		try:
		    testdate = datetime.strptime(date,date_format)
		except ValueError:
		    raise BookingError("Invalid date format")
		try:
		    testtime = datetime.strptime(time,time_format) 
		except ValueError:
		    raise BookingError("Invalid time format")
		bookingdate = datetime.strptime("{}, {}".format(date, time), "%Y-%m-%d, %H:%M")    
		if bookingdate < currentDT:
		    raise BookingError("Invalid booking")             

		
	@property
	def provider(self):
		return self._provider

	@property
	def date(self):
		return self._date
		
	@property
	def time(self):
		return self._time

	@property
	def patient(self):
		return self._patient
	
	@property
	def reason(self):
		return self._reason

	@property
	def notes(self):
		return self._notes
	
	def notes_append(self, name, note):
		self._notes.append(Note(name, note))

	@property
	def prescriptions(self):
		return self._prescriptions
	
	def prescriptions_append(self, name, prescript):
		self._prescriptions.append(Prescription(name, prescript))
