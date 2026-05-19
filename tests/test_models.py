from src.models import AnalysisInput
from src.models import Competitor
from src.models import AnalysisResult
from pydantic import ValidationError
import pytest


# ANALYSIS INPUT TESTS
def test_analysis_input_valid():
    data = {
        "latitude": 45.0,
        "longitude": 9.0,
        "categories": ["restaurant"],
        "search_area": {
            "type": "Polygon",
            "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]
        }
    }

    model = AnalysisInput(**data)
    assert model.latitude == 45.0
    assert model.longitude == 9.0
    assert model.categories == ["restaurant"]
    assert model.search_area["type"] == "Polygon"
    assert model.search_area["coordinates"] == [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]


# test passa se mancanza campi restituisce errore
def test_analysis_input_missing_fields():
    with pytest.raises(ValidationError):
        AnalysisInput(
            latitude=45.0,
            longitude=9.0
            # manca categories e search_area
        )


# deve passare perchè categoria può essere vuota
def test_analysis_input_empty_categories():
    data = {
        "latitude": 45.0,
        "longitude": 9.0,
        "categories": [],
        "search_area": {
            "type": "Polygon",
            "coordinates": [[[0,0],[1,0],[1,1],[0,0]]]
        }
    }

    model = AnalysisInput(**data)
    assert model.categories == []


# ANALISI COMPETITOR TESTS
def test_competitor_creation():
    c = Competitor(
        name="Test",
        category="restaurant",
        subcategory="italian_restaurant",
        address="Via Roma",
        latitude=45.0,
        longitude=9.0,
        distance_meters=100.0
    )

    assert c.name == "Test"
    assert c.category == "restaurant"
    assert c.subcategory == "italian_restaurant"
    assert c.address == "Via Roma"
    assert c.latitude == 45.0
    assert c.longitude == 9.0
    assert c.distance_meters == 100.0




# ANALYSIS RESULT TESTS
def test_analysis_result_structure():
    result = AnalysisResult(
        target_location={"latitude": 45.0, "longitude": 9.0},
        competitors=[],
        total_competitors=0,
        average_distance_meters=None,
        nearest_competitor_distance=None,
        competition_density="LOW"
    )

    assert result.target_location == {"latitude": 45.0, "longitude": 9.0}
    assert result.competitors == []
    assert result.total_competitors == 0
    assert result.average_distance_meters is None
    assert result.nearest_competitor_distance is None
    assert result.competition_density == "LOW"