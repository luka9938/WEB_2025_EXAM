import random
import string
def generate_verification_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))