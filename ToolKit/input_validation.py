# input_validation.py
import re

class UserInputValidator:
    def validate_email(self, email):
        # Simple regex for validating an Email
        pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_name(self, name):
        # Check if the name is not empty and contains only letters and spaces
        return name.isalpha() or " " in name

    def validate_number(self, number):
        return len(number) is not None
