import uvicorn

from skate_tricks.api_endpoints import app
from skate_tricks.configs.api_config import get_api_settings

if (
    __name__ == "__main__"
):  # TODO check/findout user and password for postgres database on VM
    api_config = get_api_settings()
    uvicorn.run(app, host="127.0.0.1", port=api_config.API_PORT)
