import uvicorn
from .app import init_api

def main():
  app = init_api()
  uvicorn.run(app, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()