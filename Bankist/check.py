import random

def generate_account_number():
    # Generate a 10-digit random account number
    return ''.join([str(random.randint(0, 9)) for _ in range(5)])

account_number =f"5000{generate_account_number()}"
print(f"Generated Account Number: {account_number}")
