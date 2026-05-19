import json
import pandas as pd


def load_data():
    with open("data/pois.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    return df


def load_sample_input():
    with open("data/sample_input.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    return data


def load_input(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)