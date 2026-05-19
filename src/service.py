import pandas as pd
from src.models import Competitor, AnalysisInput, AnalysisResult
from geopy.distance import geodesic
from shapely.geometry import Point, Polygon


def analyze_data(df: pd.DataFrame, analysis: AnalysisInput) -> AnalysisResult:
    # LOGICA ANALISI

    # Creazione poligono di ricerca
    coords = analysis.search_area["coordinates"]
    polygon = Polygon(coords[0])

    # Filtraggio per area di ricerca
    rows = []

    for i in range(len(df)):   
        point = Point(df.iloc[i]["longitude"], df.iloc[i]["latitude"])
        if(polygon.contains(point)):
            rows.append(df.iloc[i])
            

    df1 = pd.DataFrame(rows)

    # Filtraggio per categoria 
    filtered_rows = []
    for i in range(len(df1)):
        subcategory = df1.iloc[i]["subcategory"]
        category_match = any(cat in subcategory for cat in analysis.categories)
        if category_match:
            filtered_rows.append(df1.iloc[i])

    df2 = pd.DataFrame(filtered_rows)

    # Calcolo distanza per ogni punto filtrato
    distance_meters = []

    for i in range(len(df2)): 
        distance_meters.append(round(geodesic((analysis.latitude, analysis.longitude), (df2.iloc[i]["latitude"], df2.iloc[i]["longitude"])).meters, 0))
    df2["distance_meters"] = distance_meters

    # Ordinamento per distanza crescente
    df2 = df2.sort_values("distance_meters", ascending=True)

    # Inserimento metriche di competizione
    competitors = []

    for i in range(len(df2)):
        competitor = Competitor(
            name=df2.iloc[i]["name"], 
            category=df2.iloc[i]["category"], 
            subcategory=df2.iloc[i]["subcategory"], 
            address=df2.iloc[i]["address"], 
            latitude=df2.iloc[i]["latitude"], 
            longitude=df2.iloc[i]["longitude"], 
            distance_meters=df2.iloc[i]["distance_meters"]
        )
        competitors.append(competitor)

    # Metriche di competizione
    total_competitors = None
    avg_distance = None
    min_distance = None

    total_competitors = len(df2)
    avg_distance = df2["distance_meters"].mean() if not df2.empty else None
    min_distance = df2["distance_meters"].min() if not df2.empty else None

    # Densità di competizione
    density = None

    if total_competitors <= 4:
        density = "LOW"
    elif total_competitors <= 8:
        density = "MEDIUM"
    else:
        density = "HIGH"


    output = AnalysisResult(
        target_location={
            "latitude": analysis.latitude,
            "longitude": analysis.longitude
        }, 
        competitors=competitors, 
        total_competitors=total_competitors, 
        average_distance_meters=avg_distance, 
        nearest_competitor_distance=min_distance, 
        competition_density=density,
    )

    return output
