from src.service import analyze_data
from src.models import AnalysisInput
import src.data_loader as dl
from shapely.geometry import Point, Polygon
import pandas as pd
import json
import pytest
from pydantic import ValidationError

# --------------------------- BASELINE TESTS

def test_analyze_data_runs():
    df = dl.load_data()
    analysis = AnalysisInput(**dl.load_sample_input())
    result = analyze_data(df, analysis)

    assert result is not None


def test_competitors_exist():   
    df = dl.load_data()
    analysis = AnalysisInput(**dl.load_sample_input())
    result = analyze_data(df, analysis)

    assert result.total_competitors >= 0
    assert len(result.competitors) == result.total_competitors


def test_density_values():
    df = dl.load_data()
    analysis = AnalysisInput(**dl.load_sample_input())
    result = analyze_data(df, analysis)

    assert result.competition_density in ["LOW", "MEDIUM", "HIGH"]


# --------------------------- ADDITIONAL TESTS


# il poligono contiene effettivamente tutti i competitor identificati?
def test_poligon_contains_competitors():
    df = dl.load_data()
    analysis = AnalysisInput(**dl.load_sample_input())
    result = analyze_data(df, analysis)

    coords = analysis.search_area["coordinates"]
    polygon = Polygon(coords[0])

    for c in result.competitors:
        point = Point(c.longitude, c.latitude)
        assert polygon.contains(point)


# confronto output mio con output atteso
def test_comparison_output_output():
    df = dl.load_data()
    analysis = AnalysisInput(**dl.load_sample_input())
    result = analyze_data(df, analysis)

    with open("data/expected_output.json", "r", encoding="utf-8") as f:
        expected_output = json.load(f)

    output = result.model_dump()

    # metriche base
    assert output["total_competitors"] == expected_output["total_competitors"]

    assert output["competition_density"] == expected_output["competition_density"]

    # tolleranza float
    assert abs(
        output["average_distance_meters"]
        - expected_output["average_distance_meters"]
    ) <= 1

    assert abs(
        output["nearest_competitor_distance"]
        - expected_output["nearest_competitor_distance"]
    ) <= 1

    # competitors
    assert len(output["competitors"]) == len(expected_output["competitors"])

    for out_c, exp_c in zip(output["competitors"], expected_output["competitors"]):
        assert out_c["name"] == exp_c["name"]

        assert abs(
            out_c["distance_meters"]
            - exp_c["distance_meters"]
        ) <= 1


# nessun POI corrisponde alle categorie fornite
def test_no_category_match():
    df = dl.load_data()
    analysis = AnalysisInput(**dl.load_sample_input())

    analysis.categories = ["nonexistent_category"]

    result = analyze_data(df, analysis)

    assert result.total_competitors == 0
    assert result.competitors == []
    assert result.average_distance_meters is None
    assert result.nearest_competitor_distance is None


def test_no_categories():
    df = dl.load_data()
    analysis = AnalysisInput(**dl.load_sample_input())

    analysis.categories = []

    result = analyze_data(df, analysis)

    assert result.total_competitors == 0
    assert result.competitors == []
    assert result.average_distance_meters is None
    assert result.nearest_competitor_distance is None


# nessun POI ricade nell’area di ricerca
def test_no_pois_in_polygon():
    df = dl.load_data()
    analysis = AnalysisInput(**dl.load_sample_input())

    analysis.search_area = {
        "type": "Polygon",
        "coordinates": [[[0, 0], [0, 0.001], [0.001, 0.001], [0.001, 0], [0, 0]]]
    }

    result = analyze_data(df, analysis)

    assert result.total_competitors == 0
    assert result.competitors == []


# un solo competitor (tutte le metriche devono comunque funzionare)
def test_single_competitor():
    df = dl.load_data()
    analysis = AnalysisInput(**dl.load_sample_input())

    analysis.search_area = {
        "type": "Polygon",
        "coordinates": [        # poligono attorno a [9.1850, 45.4630]
            [
                [9.1849, 45.4629],
                [9.1849, 45.4631],
                [9.1851, 45.4631],
                [9.1851, 45.4629],
                [9.1849, 45.4629]   
            ]
        ]
    }  # abbastanza grande da includere 1 solo POI
    analysis.categories = ["restaurant"]

    result = analyze_data(df, analysis)

    assert result.total_competitors == 1
    assert len(result.competitors) == 1

    assert result.average_distance_meters == result.nearest_competitor_distance


# input non valido (campi mancanti, coordinate fuori range, categorie vuote)
def test_invalid_input_missing_fields():
    with pytest.raises(ValidationError):
        AnalysisInput(
            latitude=45.0
            # manca longitude, categories, search_area
        )


# match categorie per substring (esempio "restaurant" matcha "italian restaurant", ma non "pizzeria")
def test_category_substring_matching():
    df = dl.load_data()
    analysis = AnalysisInput(**dl.load_sample_input())

    analysis.categories = ["restaurant"]

    result = analyze_data(df, analysis)

    for c in result.competitors:
        assert "restaurant" in c.subcategory