import uvicorn

def main():
   uvicorn.run(
      app_dir='app',
      app="main:app",
      host="localhost",
      port=85,
      reload=True,
   )

if __name__ == "__main__":
   main()
