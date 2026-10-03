import json
from pathlib import Path

CONFIG_FILE = Path("config.json")


def create_config(sheet_url: str, creds_path: str) -> None:
    data = {
        "sheet_url": sheet_url,
        "creds_path": creds_path,
    }

    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def config_exists() -> bool:
    return CONFIG_FILE.exists()


def read_config() -> dict:
    if not config_exists():
        raise FileNotFoundError("config.json does not exist.")

    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_sheet_url(name: str) -> str:
    return read_config()["sheets"][name]


def get_creds_path() -> str:
    return read_config()["creds_path"]


def set_sheet_url(sheet_url: str) -> None:
    data = read_config()
    data["sheet_url"] = sheet_url

    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def set_creds_path(creds_path: str) -> None:
    data = read_config()
    data["creds_path"] = creds_path

    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def credentials_exist() -> bool:
    return Path(get_creds_path()).is_file()

def get_sheet_names() -> list[str]:
    return list(read_config()["sheets"].keys())