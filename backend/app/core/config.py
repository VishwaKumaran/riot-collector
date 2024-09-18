from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class CertificateSettings(BaseSettings):
    type: str
    project_id: str
    private_key_id: str
    private_key: str
    client_email: str
    client_id: str
    auth_uri: str
    token_uri: str
    auth_provider_x509_cert_url: str
    client_x509_cert_url: str
    universe_domain: str

    @field_validator('private_key', mode='before')
    def handle_newlines(cls, v):
        return v.replace('\\n', '\n')


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_ignore_empty=True, extra="ignore", env_nested_delimiter='__'
    )

    PROJECT_NAME: str = 'Riot-Collector'

    API_V1: str = '/api/v1'

    JOB_RELEASE_PATCH: str = 'fb000ab5-ab68-43c9-8328-19f256d3b180'

    CERTIFICATE: CertificateSettings

    CHAMPION_COLLECTION: str = 'champion'
    ITEM_COLLECTION: str = 'item'
    PATCH_COLLECTION: str = 'patch'
    PERKS_COLLECTION: str = 'perks'
    SUMMONER_SPELL_COLLECTION: str = 'summoner_spell'
    SHARD_COLLECTION: str = 'shard'


settings = Settings()
