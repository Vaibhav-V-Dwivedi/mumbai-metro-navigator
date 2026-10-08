import uvicorn

if __name__ == "__main__":
    # The app_dir="backend" argument automatically sets the working directory, 
    # and we change the target simply to "main:app"
    uvicorn.run("main:app", app_dir="backend", host="127.0.0.1", port=8000, reload=True)