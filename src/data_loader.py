import json
import pandas as pd
from typing import Any, cast


def load_data() -> pd.DataFrame:
    with open("data/pois.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    return df


def load_sample_input() -> dict[str, Any]:
    with open("data/sample_input.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    return cast(dict[str, Any], data)


def load_input(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)
        return data