from pydantic import BaseSettings


class ApiSettings(BaseSettings):
    API_PORT: int
    API_SPEC_ROUTE: str


def get_api_settings() -> ApiSettings:
    return ApiSettings()
