import re

def validate_username(username):
    """Check if username is valid"""
    if not username:
        return False, "Username is required"
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    if len(username) > 30:
        return False, "Username must be less than 30 characters"
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, "Username can only contain letters, numbers, underscores, and hyphens"
    return True, ""

def validate_display_name(name):
    """Check if display name is valid"""
    if not name:
        return False, "Display name is required"
    if len(name) < 3:
        return False, "Display name must be at least 3 characters"
    if len(name) > 50:
        return False, "Display name must be less than 50 characters"
    return True, ""

def validate_email(email):
    """Check if email is valid"""
    if not email:
        return False, "Email is required"
    if len(email) > 255:
        return False, "Email is too long"
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return False, "Invalid email format"
    return True, ""

def validate_password(password):
    """Check if password meets requirements"""
    if not password:
        return False, "Password is required"
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, ""

def validate_bio(bio):
    """Check if bio is valid"""
    if bio and len(bio) > 160:
        return False, "Bio must be less than 160 characters"
    return True, ""

def validate_caption(caption):
    """Check if caption is valid"""
    if caption and len(caption) > 1000:
        return False, "Caption is too long (max 1000 characters)"
    return True, ""

def validate_tags(tags):
    """Check if tags are valid"""
    if not tags:
        return True, ""
    if len(tags) > 5:
        return False, "Maximum 5 tags allowed"
    for tag in tags:
        if len(tag) > 30:
            return False, f"Tag '{tag}' is too long (max 30 characters)"
        if not re.match(r'^[a-zA-Z0-9_\s-]+$', tag):
            return False, f"Tag '{tag}' contains invalid characters"
    return True, ""