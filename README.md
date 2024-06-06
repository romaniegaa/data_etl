<h2 align="center">Data Cleaning Pipeline</h2>

<h2 align="center">Introduction</h2>

ETL (Extract-Transform-Load) pipelines are automated processes used to move and transform data from various sources into a centralized data warehouse or database for analysis and reporting. These pipelines include the following steps:

<br>

1. **Extract:** Data is collected from the source, such as: databases, APIs or flat files. This stage focuses on retrieving raw data and ensuring it is available for processing.
2. **Transform:** The extracted data is cleaned, normalized and transformed into a suitable format for analysis.
3. **Load:** The transformed data is then loaded into a data warehouse or database.

<br>

ETL pipelines are crucial for consolidating data from multiple sources, improving data quality, and making data readily available for analytics applications.

<br>

<h2 align="center">Pipeline</h2>

The pipeline can be used by calling the class ```DataPipeline()``` and adding the filepath. Afterwards, the ```run_pipeline(transformation=False, method="none")``` method can be called to start the pipeline. By default, no transformation will be done. Here are the processes that the pipeline does in order:

<br>

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

<h2 align="center">Dataset</h2>

The dataset used as a practical example of the pipeline was obtained from Kaggle, named "<a href="(https://www.kaggle.com/datasets/varshitanalluri/crop-recommendation-dataset)">Crop Recommendation Dataset</a>". This dataset contains the following variables:

<br>
- Nitrogen: ratio of nitrogen in the soil.
- Phosphorus: ratio of Phosphorus content in the soil.
- Potassium: ratio of Potassium content in the soil.
- Temperature: temperature in degrees Celsius.
- Humidity: relative humidity in %.
- pH_Value: pH value of the soil.
- Rainfall: rainfall in mm.
- Crop: contains 22 unique values of different grown crop types.

In total, there are 2200 cases in this dataset.
