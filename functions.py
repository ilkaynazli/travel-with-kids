from model import Business
from passlib.hash import argon2

def test_the_password(password):
    """Test if the password matches the requirements"""
    """Write some doctest here!"""

    if password.isalnum():
        upper = True
        lower = True
        character = True
        for char in password:
            if char.isupper() and upper:
                upper = False
            if char.islower() and lower:
                lower = False
            if char in ['!@#$%^&*(){}[]/?'] and character:
                character = False
        if upper or lower or character:     ##If it doesn't match the requirements return True
            return True

    return False 

def add_business_to_database(result):
    """Add the business info to database"""
    if Business.query.filter(Business.business_id != result.get('business_id')).first():
        business_id = result.get('business_id')
        name = result.get('name')
        coords = result.get('coords')
        lat = coords['latitude']
        lng = coords['longitude']
        business_type = result.get('business_type')
        business = Business(business_id=business_id,
                            business_name=name,
                            business_type=business_type,
                            latitude=lat,
                            longitude=lng)
        db.session.add(business)
        db.session.commit()    

def hash_password(password):
    """hash the password before adding to database"""
    return argon2.hash(password)


def check_hashed_password(password_input, password_hashed):
    """Check if the entered password matches the hashed password in database"""
    return argon2.verify(password_input, password_hashed)
