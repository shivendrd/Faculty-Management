from fastapi import FastAPI, Depends,Request
from controllers import admin, assignments, books
from configration.config import FacultySettings, ServerSettings
import logging
import time



app = FastAPI()
app.include_router(admin.router)
app.include_router(assignments.router)
app.include_router(books.router)


def build_config():
    return FacultySettings()


def fetch_config():
    return ServerSettings(
        production_server="example.com",
        prod_port=8080,
        development_server="localhost",
        dev_port=8000
    )


@app.get("/index")
def index_faculty(
    config: FacultySettings = Depends(build_config),
    fconfig: ServerSettings = Depends(fetch_config),
):
    return {
        "project_name": config.application,
        "webmaster": config.webmaster,
        "created": config.created,
        "production_server": fconfig.production_server,
        "prod_port": fconfig.prod_port,
    }



# Configure logging
logging.basicConfig(
    filename='api_logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

@app.middleware("http")
async def log_endpoint(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time

    # Log relevant information
    log_data = {
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "latency_seconds": latency,
        "client_ip": request.client.host,
    }
    
    # Log 'log_data' to the file using the logging library
    logging.info(log_data)

    return response