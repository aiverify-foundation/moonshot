import sys
import warnings
from moonshot.integrations.web_api import __main__ as web_api

"""
Run the Moonshot application
"""
# Setting the warnings to be ignored
warnings.filterwarnings("ignore")

def main():
    if len(sys.argv) < 2:
        print("Invalid number of argument given.")
        sys.exit(1)
    option = sys.argv[1]
    if option == "web_api":
        web_api.start_app()
    else: 
        print("Unrecognized arguments. Please use web_api")
        sys.exit(1)

if __name__ == "__main__":
    main()
