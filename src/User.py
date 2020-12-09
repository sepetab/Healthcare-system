from flask_login import UserMixin
from abc import ABC, abstractmethod
import random
class UserError(Exception):
    "Raised when user updates are incorrect"
    pass

class User(UserMixin, ABC):
    __id = -1

    def __init__(self, username, password):
        self._id = self._generate_id()
        self._username = username
        self._password = password
        self._email = username
        self._phone_no = "04"+str(random.randint(10,99))+"-"+str(random.randint(100,999))+"-"+str(random.randint(100,999))

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, new):
        self._username = new

    @property
    def is_authenticated(self):
        return True

    @property    
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        """Required by Flask-login"""
        return str(self._id)

    def _generate_id(self):
        User.__id += 1
        return User.__id

    def validate_password(self, password):
        return self._password == password

    @property
    def phone_no(self):
        return self._phone_no

    @phone_no.setter
    def phone_no(self, no):
        counter = 0
        for x in no:
            if x == '-':
                counter = counter + 1
        for x in no:
            if ((x < '0' or x > '9') and x != '-') or no[0] == '-' or counter > 2:
                raise UserError("Not a valid phone number") 
        self._phone_no = no

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email
        flag=0
        for x in email:
            if x == '@':
                flag = 1
        if flag == 0 or email.find(".com") == -1:
            raise UserError("Not a valid email")
        self._email = email        


    @property
    @abstractmethod
    def is_admin(self):
        pass

    @property
    @abstractmethod
    def is_patient(self):
        pass

    @property
    @abstractmethod
    def is_provider(self):
        pass


class Patient(User):
    def __init__(self, username, password):
        self._bookings = []
        self._medi_num = str(random.randint(100000000,999999999))
        super().__init__(username, password)

    @property
    def medi_num(self):
        return self._medi_num

    @medi_num.setter
    def medi_num(self, num):
        for x in num:
            if (x < '0' or x > '9'):
                raise UserError("Not a valid Medicare number")
        self._medi_num = str(num)  

    @property
    def bookings(self):
        return self._bookings
    
    def append_bookings(self, booking):
        self._bookings.append(booking)

    def is_admin(self):
        return False

    def is_patient(self):
        return True

    def is_provider(self):
        return False

    def __str__(self):
        return 'Patient <name: {self._username}>'

class Provider(User):
    def __init__(self, rating, username, password, provider_type, centres=None):
        self._bookings = []
        self._provider_type = provider_type
        self._rating = []
        self._prov_num = str(random.randint(100000000,999999999))
        self._centres = centres
        self._patient_access = []
        self._booked_appointments = {}
        super().__init__(username, password)

    def patient_perm(self, name):
        if (name in self._patient_access):
            return True
        return False

    def patient_perm_append(self, name):
        self._patient_access.append(name)

    @property
    def provider_type(self):
        return self._provider_type

    @provider_type.setter
    def provider_type(self, ptype):
        for x in ptype:
            if (x < 'a' or x > 'z') and (x < 'A' or x > 'Z'):
                raise UserError("Not a valid profession type")
        self._provider_type = ptype

    def add_appointment(self, date, time):
        self._booked_appointments[date] = time
        
    def appointment_present(self, date, time):
        if (date in self._booked_appointments):
            if (self._booked_appointments[date] == time):
                return True
        return False
    
    def is_admin(self):
        return False

    def is_patient(self):
        return False

    def is_provider(self):
        return True

    def add_patient(self):
        return self._add_patient

    @property
    def get_rating(self):
        if not self._rating:
            return float(0)
        return round(float(sum(self._rating))/len(self._rating),1)

    def add_rating(self, rating):
        (self._rating).append(round(rating,1))

    @property
    def bookings(self):
        return self._bookings
    
    def append_bookings(self, booking):
        (self._bookings).append(booking)

    @property
    def centres(self):
        return self._centres

    def append_cent_affil(self, centre):
        self._centres.append(centre)

    @property
    def prov_num(self):
        return self._prov_num

    @prov_num.setter
    def prov_num(self, num):
        for x in num:
            if x < '0' or x > '9':
                raise UserError("Not a valid provider number")
        self._prov_num = num
        
    
    def __str__(self):
        return 'Provider <name: {self._username}>'

class Admin(User):
    def is_admin(self):
        return True

    def is_patient(self):
        return True

    def is_provider(self):
        return True

    def __str__(self):
        return 'Admin <name: {self._username}>'
