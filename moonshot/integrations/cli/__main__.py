import sys

def start_app():
    #placeholder function
    print("Hello World from CLI")
    if "interactive" in sys.argv:
        print("interactive argument received.")
    

if __name__ == "__main__":
    start_app()