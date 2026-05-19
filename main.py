import src.data_loader as dl
from src.models import AnalysisInput, AnalysisResult
from src.service import analyze_data
from typing import Any
#CLI
import argparse
import json


def main() -> AnalysisResult:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        type=str,
        default="data/sample_input.json"
    )

    args = parser.parse_args()

    df = dl.load_data()

    input_data = dl.load_input(args.input)
    analysis = AnalysisInput(**input_data)

    return analyze_data(df, analysis)



if __name__ == "__main__":
    result = main()
    print(json.dumps(result.model_dump(), indent=2))

