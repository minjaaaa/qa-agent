from pydantic_settings import BaseSettings, SettingsConfigDict


class Podesavanja(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    log_nivo: str = "INFO"
    github_token: str = ""
    docker_host: str = "tcp://docker-socket-proxy:2375"


podesavanja = Podesavanja()