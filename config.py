from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379/0"
    pg_dsn: str = "postgresql://quant:quant@localhost:5432/quant"
    shadow_mode: bool = True           # hard lock for 48h
    max_conviction: float = 0.35       # tune post-run
    s_max: float = 1_000               # max notional per market
    min_trade_size: float = 5
    ob_snap_interval_ms: tuple[int, int] = (150, 500)
    ob_history: int = 200
    heartbeat_ms: dict[str, int] = {"CALM":500, "COMPETITIVE":300, "ILLUSORY":150, "PREDATORY":300}
    gks_recovery_window_s: int = 900   # 15 minutes

    class Config:
        env_file = ".env"

settings = Settings()