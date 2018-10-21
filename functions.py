
def test_the_password(password1, password2):
    """Test if the password matches the requirements"""
    """Write some doctest here!"""

    if password1.isalnum():
        upper = True
        lower = True
        character = True
        for char in password1:
            if char.isupper() and upper:
                upper = False
            if char.islower() and lower:
                lower = False
            if char in ['!@#$%^&*(){}[]/?'] and character:
                character = False
        if upper or lower or character:     ##If it doesn't match the requirements return False
            return True

    return False 