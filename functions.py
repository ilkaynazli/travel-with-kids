
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