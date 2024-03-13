import sys
from moonshot.integrations.web_api import __main__ as web_api

"""
Run the Moonshot application
"""

def main():
    if len(sys.argv) != 2:
        print("Invalid number of argument given.")
        sys.exit(1)
    option = sys.argv[1]
    if option == "web_api":
        web_api.start_app()

if __name__ == "__main__":
    main()
