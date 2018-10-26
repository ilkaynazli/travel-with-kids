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


def hash_password(password):
    """hash the password before adding to database"""
    return argon2.hash(password)


def check_hashed_password(password_input, password_hashed):
    """Check if the entered password matches the hashed password in database"""
    return argon2.verify(password_input, password_hashed)
