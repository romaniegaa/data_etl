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
| |count|mean|std|min|25%|50%|75%|max|
|Nitrogen|2200.0|50.551818181818184|36.9173338337566|0.0|21.0|37.0|84.25|140.0|
|Phosphorus|2200.0|53.36272727272727|32.98588273858715|5.0|28.0|51.0|68.0|145.0|
|Potassium|2200.0|48.14909090909091|50.64793054666013|5.0|20.0|32.0|49.0|205.0|
|Temperature|2200.0|25.616243851779544|5.063748599958843|8.825674745|22.7693746325|25.5986932|28.5616539325|43.67549305|
|Humidity|2200.0|71.48177921778637|22.263811589761083|14.25803981|60.2619528025|80.473145665|89.948770755|99.98187601|
|pH_Value|2200.0|6.469480065256364|0.7739376880298733|3.504752314|5.9716927992499995|6.42504527|6.92364262125|9.93509073|
|Rainfall|2200.0|103.46365541576817|54.95838852487813|20.21126747|64.55168599999999|94.86762427|124.2675078|298.5601175|
