import os
from datapipeline import *

dir = r"C:\Users\Usuario\OneDrive\Escritorio\Projects\ETL"
os.chdir(dir)

# Test
filename = "crop_recommendation.csv"

data = DataPipeline(filename)
data.run_pipeline(transformation = True, method = "quantile")

