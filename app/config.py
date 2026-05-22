from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


load_dotenv()


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_")

    host: str = "localhost"
    port: int = 3306
    name: str = "bot"
    user: str = "bot"
    password: str = ""

    @property
    def url(self) -> str:
        return f"mysql+aiomysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}?charset=utf8mb4"


class MyuzDatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_MYUZ_")

    host: str = "localhost"
    port: int = 3306
    name: str = "cloud_yuuz12_top"
    user: str = "cloud_yuuz12_top"
    password: str = ""

    @property
    def url(self) -> str:
        return f"mysql+aiomysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}?charset=utf8mb4"


class InvitationDatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_INVITATION_")

    host: str = "localhost"
    port: int = 3306
    name: str = "skin_fstmc_top"
    user: str = "skin_fstmc_top"
    password: str = ""

    @property
    def url(self) -> str:
        return f"mysql+aiomysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}?charset=utf8mb4"


class DeepSeekSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DEEPSEEK_")

    api_key: str = ""
    base_url: str = "https://api.deepseek.com/v1"


class QwenSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="QWEN_")

    api_key: str = ""
    base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"


class OsuSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="OSU_")

    api_key: str = ""


class BaiduSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BAIDU_")

    client_id: str = ""
    client_secret: str = ""


class BtPanelSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BT_PANEL_")

    url: str = ""
    key: str = ""


class SmtpSettings(BaseSettings):
    host: str = "smtp.qq.com"
    port: int = 465
    email: str = ""
    password: str = ""
    display_name: str = ""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    db: DatabaseSettings = DatabaseSettings()
    db_myuz: MyuzDatabaseSettings = MyuzDatabaseSettings()
    db_invitation: InvitationDatabaseSettings = InvitationDatabaseSettings()

    auth_tokens: list[str] = []

    deepseek: DeepSeekSettings = DeepSeekSettings()
    qwen: QwenSettings = QwenSettings()
    osu: OsuSettings = OsuSettings()
    baidu: BaiduSettings = BaiduSettings()
    bt_panel: BtPanelSettings = BtPanelSettings()

    smtp_kirino: SmtpSettings = SmtpSettings()
    smtp_shiruku: SmtpSettings = SmtpSettings()

    cors_origins: list[str] = []

    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_debug: bool = False


settings = Settings()
