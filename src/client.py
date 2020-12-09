from .AdminSystem import AdminSystem
from .HAMSSystem import HAMSSystem
from .AuthenticationManager import AuthenticationManager
from .User import Patient, Provider, Admin
from .Centre import Centre
import csv

def bootstrap_system(auth_manager):

    admin_system = AdminSystem(auth_manager)
    system = HAMSSystem(admin_system, auth_manager)
    csv_flag_prov = False
    csv_flag_cent = False

    #We only need to have one admin:
    admin_system.add_admin(Admin('admin', 'password'))
    
    if not system.patients:
        with open('patient.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                #Add all the patient logins
                system.add_patient(Patient(row['email'], row['password']))

    if not system.providers:
        csv_flag_prov = True
        with open('provider.csv') as g:
            reader = csv.DictReader(g)
            for row in reader:
                #Add all the healthcare provider logins with empty affiliation profiles
                system.add_provider(Provider(0, row['provider'], row['password'], row['type'], []))

    if not system.centres:
        csv_flag_cent = True
        with open('health_centres.csv') as h:
            reader = csv.DictReader(h)
            for row in reader:
                #Add all the centre info
                system.add_centre(Centre(row['type'], row['post'], row['name'], row['phone'], row['suburb'], []))

    # adds in bilateral associations
    if csv_flag_prov or csv_flag_cent:
        with open('provider_health_centre.csv') as i:
            reader = csv.DictReader(i)
            for row in reader:
                if csv_flag_prov:
                    system.add_affil(row['provider'], row['centre'], True)
                if csv_flag_cent:
                    system.add_affil(row['provider'], row['centre'], False)

    return system