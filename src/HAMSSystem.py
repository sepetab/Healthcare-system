import copy
from .User import User, Patient, Provider, Admin
from .Booking import Booking
from flask_login import current_user
'''
persistence manager
'''
import pickle

class HAMSSystem:
    def __init__(self, admin_system, auth_manager):
        self._patients = self.unpickle_save_patients()
        self._providers = self.unpickle_save_providers()
        self._centres = self.unpickle_save_centres()
        self._bookings = self.unpickle_save_booking()
        self._admin_system = admin_system
        self._auth_manager = auth_manager

    '''
    Query Processing Services
    '''
    # get user by id
    def get_user_by_id(self, user_id):
        for c in self.patients:
            if c.get_id() == user_id:
                return c
        for c in self.providers:
            if c.get_id() == user_id:
                return c
        return self._admin_system.get_user_by_id(user_id)

    # search for provider
    def get_search_provider(self, sname, sprof, list_req):
        result = []
        sname = sname.lower()
        sprof = sprof.lower()
        for p in self.providers:
            if sprof == '' and sname == '':
                return self.providers
            elif sname == '':
                if p.provider_type.lower().find(sprof)!=-1:
                    result.append(p)
            elif sprof == '':
                if p.username.lower().find(sname)!=-1:
                    result.append(p)
            else:
                if p.username.lower().find(sname)!=-1 and p.provider_type.lower().find(sprof)!=-1:
                    result.append(p)
        # pythonic bs about empty lists
        if not result:
            return None
        else:
            if (list_req):
                return result
            else:
                return result[0]

    # get patient by name
    def get_patient(self, name):
        for p in self.patients:
            if p.username == name:
                return p
        return None

    # get centre by search type
    def get_search_centre(self, search, stype, list_req):
        result = []
        search = search.lower()
        for c in self.centres:
            if search == "":
                return self.centres
            elif c.name.lower().find(search)!=-1 and stype == "name":
                result.append(c)
            elif c.ctype.lower().find(search)!=-1 and stype == "ctype":
                result.append(c)
            elif c.postCode.lower().find(search)!=-1 and stype == "postCode":
                result.append(c)
            elif c.suburb.lower().find(search)!=-1 and stype == "suburb":
                result.append(c)
        # pythonic bs about empty lists
        if not result:
            return None
        else:
            if (list_req):
                return result
            else:
                return result[0]


    '''
    Booking Services
    '''
    # Make booking
    def make_booking(self, booking):
        self.bookings.append(booking) 

    # change to user id's later
    def get_bookings(self):
        result = []
        if current_user.is_admin():
            return self.bookings
        else:
            return current_user.bookings
        # pythonic bs about empty lists
        if not result:
            return None
        else:
            return result

    '''
    Registration Services
    '''
    def add_patient(self, patient):
        self.patients.append(patient)

    def add_provider(self, provider):
        self.providers.append(provider)

    def add_centre(self, centre):
        self.centres.append(centre)

    def add_affil(self, source, dest, csvProvFlag):
        provider = self.get_search_provider(source, "", False)
        centre = self.get_search_centre(dest, "name", False)

        if csvProvFlag:
            provider.append_cent_affil(centre)
        else:
            centre.append_prov_affil(provider)
            
    '''
    Login Services
    '''
    def login_user(self, username, password):
        for user in self._patients:
            if self._auth_manager.login(user, username, password):
                return True
        for user in self._providers:
            if self._auth_manager.login(user, username, password):
                return True
        return False

    def login_admin(self, username, password):
        return self._admin_system.login(username, password)


    '''
    Properties
    '''
    @property
    def centres(self):
        return self._centres

    @property
    def providers(self):
        return self._providers

    @property
    def patients(self):
        return self._patients

    @property
    def bookings(self):
        return self._bookings

    '''
    Persistence Pickling Functions
    '''
    # dumps bookings into seperate persistent file
    # change to private bookings as property does some
    # strange stuff and kills admin functionality
    def pickle_save_booking(self):
        savefile = open('bookings', 'wb')
        pickle.dump(self._bookings, savefile)
        savefile.close()

    def pickle_save_providers(self):
        savefile = open('providers', 'wb')
        pickle.dump(self._providers, savefile)
        savefile.close()

    def pickle_save_patients(self):
        savefile = open('patients', 'wb')
        pickle.dump(self._patients, savefile)
        savefile.close()

    def pickle_save_centres(self):
        savefile = open('centres', 'wb')
        pickle.dump(self._centres, savefile)
        savefile.close()

    '''
    Persistence Un-Pickling Functions
    '''
    def unpickle_save_booking(self):
        bookings = []
        try:
            savefile = open('bookings', 'rb')
        except FileNotFoundError:
            return bookings
        else:
            bookings = pickle.load(savefile)
            savefile.close()
            return bookings

    def unpickle_save_providers(self):
        providers = []
        try:
            savefile = open('providers', 'rb')
        except FileNotFoundError:
            return providers
        else:
            providers = pickle.load(savefile)
            savefile.close()
            return providers

    def unpickle_save_patients(self):
        patients = []
        try:
            savefile = open('patients', 'rb')
        except FileNotFoundError:
            return patients
        else:
            patients = pickle.load(savefile)
            savefile.close()
            return patients

    def unpickle_save_centres(self):
        centres = []
        try:
            savefile = open('centres', 'rb')
        except FileNotFoundError:
            return centres
        else:
            centres = pickle.load(savefile)
            savefile.close()
            return centres