from src.Booking import *
from src.User import User, Patient, Provider, Admin, UserError
import pytest
'''Test booking'''

def test_failed_booking():

    # for pytest.raises(BookingError)

    # provider can never been invalid as in routes.py: 
    # if not mprovider:
    #    abort(404)
    # will return 404 error, stopping Booking() from running
    # patient can never be invalid as patient is the one 
    # making the booking
    # reason can never be invalid

    # not specifying date

    # not specifying date and correct time format
    try: 
        Booking("toby@gmail.com","","12:30","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Specify a date"
        pytest.raises(BookingError)
    
    # not specifying date and incorrect time format
    try: 
        Booking("toby@gmail.com","","1230","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Specify a date"
        pytest.raises(BookingError)

    # not specifying date and not specifying time
    try: 
        Booking("toby@gmail.com","","","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Specify a date"
        pytest.raises(BookingError)



    # not specifying time

    # not specifying time and correct date format
    try:
        Booking("toby@gmail.com","2018-12-12","","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Specify a time"
        pytest.raises(BookingError)
    
    # not specifying time and incorrect date format
    try:
        Booking("toby@gmail.com","20181212","","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Specify a time"
        pytest.raises(BookingError)



    # invalid date format

    # not including dashes in between numbers in date
    try:
        Booking("toby@gmail.com","20181212","12:30","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Invalid date format"
        pytest.raises(BookingError)

    # letters in date
    try:
        Booking("toby@gmail.com","abcd-ab-cd","12:30","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Invalid date format"
        pytest.raises(BookingError) 

    # special characters in date
    try:
        Booking("toby@gmail.com","2018@12$12","12:30","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Invalid date format"
        pytest.raises(BookingError) 

    # extra numbers in date
    try:
        Booking("toby@gmail.com","2018-12-120","12:30","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Invalid date format"
        pytest.raises(BookingError)     

    # invalid date format and invalid time format
    try:
        Booking("toby@gmail.com","20181212","1230","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Invalid date format"
        pytest.raises(BookingError)

    # having month exceed 12
    try:
        Booking("toby@gmail.com","2018-13-12","12:30","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Invalid date format"
        pytest.raises(BookingError)

    # having day exceed 31
    try:
        Booking("toby@gmail.com","2018-12-32","12:30","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Invalid date format"
        pytest.raises(BookingError)

    # having day 31 for a month with 30 days (example November)
    try:
        Booking("toby@gmail.com","2018-11-31","12:30","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Invalid date format"
        pytest.raises(BookingError)                  
    
    # having day 29 for February on non-leap year (eg. 2019)
    try:
        Booking("toby@gmail.com","2019-02-29","12:30","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Invalid date format"
        pytest.raises(BookingError)



    # invalid time format

    # not including colon in between numbers in time
    try:
        Booking("toby@gmail.com","2018-12-12","1100","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Invalid time format"
        pytest.raises(BookingError)

    # letters in time
    try:
        Booking("toby@gmail.com","2018-12-12","ab:cd","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Invalid time format"
        pytest.raises(BookingError)

    # special characters in time
    try:
        Booking("toby@gmail.com","2018-12-12","11$00","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Invalid time format"
        pytest.raises(BookingError)

    # extra numbers in time
    try:
        Booking("toby@gmail.com","2018-12-12","10:000","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Invalid time format"
        pytest.raises(BookingError)

    # having number of minutes exceed 59
    try:
        Booking("toby@gmail.com","2018-12-12","10:60","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Invalid time format"
        pytest.raises(BookingError)

    # having number of hours exceed 23
    try:
        Booking("toby@gmail.com","2018-12-12","24:00","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Invalid time format"
        pytest.raises(BookingError)


    # invalid date entered         
    
    # year before current year
    try:
        Booking("toby@gmail.com","2017-12-12","12:30","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Invalid booking"
        pytest.raises(BookingError)   

    # month before current month in the same year (2018)
    try:
        Booking("toby@gmail.com","2018-02-12","12:30","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Invalid booking"
        pytest.raises(BookingError)     

    # day before current day in the same year and month (2018 and October)
    try:
        Booking("toby@gmail.com","2018-10-14","12:30","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Invalid booking"
        pytest.raises(BookingError)

    # time before current time in the same year, month and day (2018, October and 15th)
    try:
        Booking("toby@gmail.com","2018-10-15","00:00","jack@gmail.com","Sick")
        assert False
    except BookingError as err:
        assert str(err) == "Invalid booking"
        pytest.raises(BookingError)    


def test_successful_booking():

    # for pytest.fail(BookingError)

    # successful booking    
    try:
        Booking("toby@gmail.com","2018-12-12","12:30","jack@gmail.com","Sick")
    except BookingError as err:
        assert str(err) == ""
        pytest.fail(BookingError)

    # successful booking with different provider and different patient
    try:
        Booking("gary@gmail.com","2018-12-12","12:30","tom@gmail.com","Sick")
    except BookingError as err:
        assert str(err) == ""
        pytest.fail(BookingError)    

    # successful booking with different patient
    try:
        Booking("gary@gmail.com","2018-12-12","12:30","isaac@gmail.com","Sick")
    except BookingError as err:
        assert str(err) == ""
        pytest.fail(BookingError) 

    # year changed but still valid as after current year (2018)
    try:
        Booking("anna@gmail.com","2020-12-12","12:30","isaac@gmail.com","Sick")
    except BookingError as err:
        assert str(err) == ""
        pytest.fail(BookingError)
        

def test_failed_user_implementation():

    # test phone number
    # phone number cannot have letters
    try:
        user = Patient("jack@gmail.com","cs1531")
        user.phone_no = "123456789a"
        assert False
    except UserError as err:
        assert str(err) == "Not a valid phone number"
        pytest.raises(UserError)
    
    # phone number cannot have special characters
    try:
        user = Patient("jack@gmail.com","cs1531")
        user.phone_no = "1234@56-78"
        assert False
    except UserError as err:
        assert str(err) == "Not a valid phone number"
        pytest.raises(UserError)

    # phone number cannot have more than two dashes
    try:
        user = Patient("jack@gmail.com","cs1531")
        user.phone_no = "012-345-6-78"
        assert False
    except UserError as err:
        assert str(err) == "Not a valid phone number"
        pytest.raises(UserError)

    # phone number cannot have spaces
    try:
        user = Patient("jack@gmail.com","cs1531")
        user.phone_no = "04 1234 5678"
        assert False
    except UserError as err:
        assert str(err) == "Not a valid phone number"
        pytest.raises(UserError)    
      
    # phone number cannot start on a dash
    try:
        user = Patient("jack@gmail.com","cs1531")
        user.phone_no = "-12345678"
        assert False
    except UserError as err:
        assert str(err) == "Not a valid phone number"
        pytest.raises(UserError)    


    # test Medicare number

    # Medicare number cannot have letters
    try:
        user = Patient("jack@gmail.com","cs1531")
        user.medi_num = "1234567a"
        assert False
    except UserError as err:
        assert str(err) == "Not a valid Medicare number"
        pytest.raises(UserError) 
    
    # Medicare number cannot have special characters
    try:
        user = Patient("jack@gmail.com","cs1531")
        user.medi_num = "1234567@" 
        assert False
    except UserError as err:
        assert str(err) == "Not a valid Medicare number"
        pytest.raises(UserError)

    # Medicare number cannot have spaces
    try:
        user = Patient("jack@gmail.com","cs1531")
        user.medi_num = "1234 5678" 
        assert False
    except UserError as err:
        assert str(err) == "Not a valid Medicare number"
        pytest.raises(UserError)     


    # test email

    # Email doesn't have @
    try:
        user = Patient("jack@gmail.com","cs1531")
        user.email = "jack123gmail.com"
        assert False
    except UserError as err:
        assert str(err) == "Not a valid email"
        pytest.raises(UserError)

    # Email doesn't have .com
    try:
        user = Patient("jack@gmail.com","cs1531")
        user.email = "jack123@gmail.co"
        assert False
    except UserError as err:
        assert str(err) == "Not a valid email"
        pytest.raises(UserError) 

    # Email doesn't have @ and .com
    try:
        user = Patient("jack@gmail.com","cs1531")
        user.email = "jack123$gmail.cm"
        assert False
    except UserError as err:
        assert str(err) == "Not a valid email"
        pytest.raises(UserError)       
    
    
    # test profession type

    # Profession cannot have special characters
    try:
        user = Provider(5,"toby@gmail.com","cs1531","Pathologist")
        user.provider_type = "Path$$$gist"
        assert False
    except UserError as err:
        assert str(err) == "Not a valid profession type"
        pytest.raises(UserError)
    
    # Profession cannot have numbers
    try:
        user = Provider(5,"toby@gmail.com","cs1531","Pathologist")
        user.provider_type = "P4th0l0g15t"
        assert False
    except UserError as err:
        assert str(err) == "Not a valid profession type"
        pytest.raises(UserError)

    # Profession cannot have spaces
    try:
        user = Provider(5,"toby@gmail.com","cs1531","Pathologist")
        user.provider_type = "Pa th olo gist"
        assert False
    except UserError as err:
        assert str(err) == "Not a valid profession type"
        pytest.raises(UserError)    


    # test provider number

    # Provider number cannot have letters
    try:
        user = Provider(5,"toby@gmail.com","cs1531","Pathologist")
        user.prov_num = "a123"
        assert False
    except UserError as err:
        assert str(err) == "Not a valid provider number"
        pytest.raises(UserError)

    # Provider number cannot have special characters
    try:
        user = Provider(5,"toby@gmail.com","cs1531","Pathologist")
        user.prov_num = "@123#"
        assert False
    except UserError as err:
        assert str(err) == "Not a valid provider number"
        pytest.raises(UserError)

    # Provider number cannot have spaces
    try:
        user = Provider(5,"toby@gmail.com","cs1531","Pathologist")
        user.prov_num = "1234 5678"
        assert False
    except UserError as err:
        assert str(err) == "Not a valid provider number"
        pytest.raises(UserError)



def test_successful_user_implementation():         
    
    # correct phone number
    try:
        user = Patient("jack@gmail.com","cs1531")
        user.phone_no = "04-1234-2729"
    except UserError as err:
        assert str(err) == ""
        pytest.fails(UserError)              

    # correct Medicare number
    try:
        user = Patient("jack@gmail.com","cs1531")
        user.medi_num = "123456789"
    except UserError as err:
        assert str(err) == ""
        pytest.fails(UserError)

    # correct email
    try:
        user = Patient("jack@gmail.com","cs1531")
        user.email = "jack@gmail.com"
    except UserError as err:
        assert str(err) == ""
        pytest.fails(UserError)    

    # correct profession
    try:
        user = Provider(5,"toby@gmail.com","cs1531","Pathologist")
        user.provider_type = "Pathologist"
    except UserError as err:
        assert str(err) == ""
        pytest.fails(UserError) 

    # correct provider number
    try:
        user = Provider(5,"toby@gmail.com","cs1531","Pathologist")
        user.prov_num = "12345678"
    except UserError as err:
        assert str(err) == ""
        pytest.fails(UserError)      
