import sys

sys.dont_write_bytecode = True

from validation.validator import validate_data
from  utils.email_generator import email_generation

# Run data validation
if __name__ == "__main__":
    validate_data("testcases.json")
    email_generation()
    