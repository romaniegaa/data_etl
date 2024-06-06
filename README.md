<h2 align="center">Data Cleaning Pipeline</h2>

<h2 align="center">Introduction</h2>

ETL (Extract-Transform-Load) pipelines are automated processes used to move and transform data from various sources into a centralized data warehouse or database for analysis and reporting. These pipelines include the following steps:

1. **Extract:** Data is collected from the source, such as: databases, APIs or flat files. This stage focuses on retrieving raw data and ensuring it is available for processing.
2. **Transform:** The extracted data is cleaned, normalized and transformed into a suitable format for analysis.
3. **Load:** The transformed data is then loaded into a data warehouse or database.

<br>

ETL pipelines are crucial for consolidating data from multiple sources, improving data quality, and making data readily available for analytics applications.

<br>

<h2 align="center">Pipeline</h2>

The pipeline can be used by calling the class ```DataPipeline()``` and adding the filepath. Afterwards, the ```run_pipeline(transformation=False, method="none")``` method can be called to start the pipeline. By default, no transformation will be done. Here are the processes that the pipeline does in order:

- Load the data from a ".csv" file.
- Check nulls and delete rows with nulls.
- Check duplicates and delete rows with duplicates.
- Calculate basic statistics with ```describe()``` from ```Pandas```.
- Save clean data and statistics as ".csv" files.
- Calculate the correlation and obtain a heatmap graph with the result.
- Calculate each variable's Variance Inflation Factor.
- Calculate the Interquartile Range and delete the outliers.
- Calculate skewness of each variable.
- If ```transformation = True```: logarithmic, square root, Yeo Johnson and Quantile transformations will be dona and their skewness will be calculated. The median of each skewness will also be calculated to obtain the skewness closest to zero.
- If ```method != None```: a transformation will be done in the data by inputting ```"log"```, ```"sqrt"```, ```"yeojohnson"``` or ```"quantile"```.
- Save the transformed data.

![](https://github.com/romaniegaa/Portfolio/blob/main/images/etldiagrama2.png)

<h2 align="center">Practical expample</h2>

## Dataset

The dataset used as a practical example of the pipeline was obtained from Kaggle, named "<a href="(https://www.kaggle.com/datasets/varshitanalluri/crop-recommendation-dataset)">Crop Recommendation Dataset</a>". This dataset contains the following variables:

- Nitrogen: ratio of nitrogen in the soil.
- Phosphorus: ratio of Phosphorus content in the soil.
- Potassium: ratio of Potassium content in the soil.
- Temperature: temperature in degrees Celsius.
- Humidity: relative humidity in %.
- pH_Value: pH value of the soil.
- Rainfall: rainfall in mm.
- Crop: contains 22 unique values of different grown crop types.

In total, there are 2200 cases in this dataset.

## Pipeline
- Data was successfully loaded.
- No nulls were found.
- No duplicates were found.
- Stats were obtained.

| | count | mean | std | min | 25% | 50% | 75% | max |
|---|---|---|---|---|---|---|---|---|
| Nitrogen | 2200.0 | 50.5518 | 36.9173 | 0.0 | 21.0 | 37.0 | 84.25 | 140.0 |
| Phosphorus | 2200.0 | 53.3627 | 32.9858 | 5.0 | 28.0 | 51.0 | 68.0 | 145.0 |
| Potassium | 2200.0 | 48.1490 | 50.6479 | 5.0 | 20.0 | 32.0 | 49.0 | 205.0 |
| Temperature | 2200.0 | 25.6162 | 5.0637 | 8.8256 | 22.7693 | 25.5986 | 28.5616 | 43.6754 |
| Humidity | 2200.0 | 71.4817 | 22.2638 | 14.2580 | 60.2619 | 80.4731 | 89.9487 | 99.9818 |
| pH_Value | 2200.0 | 6.4694 | 0.7739 | 3.5047 | 5.9716 | 6.4250 | 6.9236 | 9.9350 |
| Rainfall | 2200.0 | 103.4636 | 54.9583 | 20.2112 | 64.55168 | 94.8676 | 124.2675 | 298.5601 |
