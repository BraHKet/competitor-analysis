import src.data_loader as dl
from src.models import AnalysisInput
from src.service import analyze_data

## CARICAMENTO DATI E INPUT

# Caricamento punti
df = dl.load_data()

# Caricamento input di analisi
analysis = AnalysisInput(**dl.load_sample_input())

# ------------------------------------------

# ANALISI DEI DATI

output = analyze_data(df, analysis)



