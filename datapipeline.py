import pandas as pd
import numpy as np

from sklearn.preprocessing import QuantileTransformer, LabelEncoder

from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor 

import plotly.express as px
import plotly.figure_factory as ff

import warnings
warnings.simplefilter(action = "ignore", category = Warning)

class DataPipeline:

    def __init__(self, filename):
        self.__filename = filename
        self.__data = None
        self.__stats = None
        self.__total_nulls = None
        self.__total_duplicates = None
        self.__data_no_outliers = None

    @property
    def data(self):
        return pd.DataFrame.copy(self.__data)
    
    @property
    def stats(self):
        return pd.DataFrame.copy(self.__stats)
    
    @property
    def total_nulls(self):
        return self.__total_nulls
    
    @property
    def total_duplicates(self):
        return self.__total_duplicates
    
    @property
    def data_no_outliers(self):
        return pd.DataFrame.copy(self.__data_no_outliers)

    def __load_data(self):
        # Load data
        try:
            self.__data = pd.read_csv(self.__filename)
            print("Data loaded!")
        except FileNotFoundError:
            raise FileNotFoundError

    def __check_nulls(self):
        check_nulls = self.__data.isnull().sum()
        self.__total_nulls = check_nulls.sum()

        # Check if there are any nulls
        if self.__total_nulls > 0:
            self.__data = self.__data.dropna()
            print(f"{self.__total_nulls} nulls were found!")
        else:
            print(f"No nulls were found!")
        
    def __check_duplicates(self):
        self.__total_duplicates = self.__data.duplicated().sum()

        # Check if there are any duplicates
        if self.__total_duplicates > 0:
            self.__data = self.__data.drop_duplicates()
            print(f"{self.__total_duplicates} duplicates were found!")
        else:
            print(f"No duplicates were found!")

    def __statistics(self):
        # Create statistics dataframe
        self.__stats = self.__data.describe().transpose()
        print("Stats were obtained!")

    def __save_clean_data(self):
        # Save the data as .csv
        self.__data.to_csv("clean_data.csv", index = False)
        print("Clean data was saved!")
        self.__stats.to_csv("stats.csv", index = True)
        print("Stat data was saved!")

    def __correlation_matrix(self):
        # Obtain numeric variables
        self.__numerical_variables_list = self.__data.select_dtypes(include = ["int64", "float64"]).columns.to_list()
        self.__correlation = self.__data[self.__numerical_variables_list].corr().round(decimals = 4)
        self.__mask = np.triu(np.ones_like(self.__correlation, dtype = bool))
        self.__correlation_masked = self.__correlation.mask(self.__mask)

        # Graph
        fig = ff.create_annotated_heatmap(z = self.__correlation_masked.to_numpy(), 
                                  x = self.__correlation_masked.columns.tolist(),
                                  y = self.__correlation_masked.columns.tolist(),
                                  colorscale = px.colors.diverging.RdBu,
                                  hoverinfo = "none", #Shows hoverinfo for null values
                                  showscale = True, ygap = 1, xgap = 1)

        fig.update_xaxes(side = "bottom")

        fig.update_layout(
            title_text = 'Heatmap', 
            title_x = 0.5, 
            width = 750, 
            height = 750,
            xaxis_showgrid = False,
            yaxis_showgrid = False,
            xaxis_zeroline = False,
            yaxis_zeroline = False,
            yaxis_autorange = 'reversed',
            template = 'plotly_white')
        
        # Save graph
        fig.write_image("correlation_matrix.png")

    def __variance_inflation_factor(self):
        X = self.__data[self.__numerical_variables_list]
        # The calculation of variance inflation requires a constant
        X['intercept'] = 1
        
        # create dataframe to store vif values
        self.__vif = pd.DataFrame()
        self.__vif["Variable"] = X.columns
        self.__vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
        self.__vif = self.__vif[self.__vif['Variable']!='intercept']
        print(self.__vif)

    def __interquartile_range(self):
        # Calculate Q1 and Q3
        self.__Q1 = self.__data[self.__numerical_variables_list].quantile(0.25)
        self.__Q3 = self.__data[self.__numerical_variables_list].quantile(0.75)

        # Calculate IQR
        self.__IQR = self.__Q3 - self.__Q1

        # Lower and upper bounds
        lower_bound = self.__Q1-1.5*self.__IQR
        upper_bound = self.__Q3+1.5*self.__IQR

        # Identify the outliers
        self.__outliers = (self.__data[self.__numerical_variables_list] < lower_bound) | (self.__data[self.__numerical_variables_list] > upper_bound)

        # Remove outliers
        self.__data_no_outliers = self.__data[~self.__outliers.any(axis = 1)]
        self.__data_no_outliers.reset_index(inplace = True, drop = True)

    def __skewness(self, transformation, method):
        # Calculate skewness for each variable
        self.__skewness = []
        for numerical_variable in self.__numerical_variables_list:
            self.__skewness.append(self.__data[numerical_variable].skew().round(decimals = 4))
        self.__skewness = pd.DataFrame(self.__skewness, index = self.__numerical_variables_list, 
                                        columns = ["Skewness"])
        self.__skewness.to_csv("skewness.csv", index = True)
        print("Calculated skewness for each numeric variable:")
        print(self.__skewness)     

        # Try different transformations
        if transformation:
            log_skewness = []
            sqrt_skewness = []
            yeojohnson_skewness = []
            quantiletransf_skewness = []

            for numerical_variable in self.__numerical_variables_list:
                # Transport data to be > 0
                transported_data = self.__data[numerical_variable]
                transported_data = transported_data - transported_data.values.min() + 1e-8

                # Log transformation
                log_skewness_val = np.log(transported_data).skew().round(decimals = 4)
                log_skewness.append(log_skewness_val)
  
                # SQRT transformation
                sqrt_skewness_val = np.sqrt(transported_data).skew().round(decimals = 4)
                sqrt_skewness.append(sqrt_skewness_val)

                # YeoJohnson transformation
                yeojohnson_transformation, _ = stats.yeojohnson(transported_data)
                yeojohnson_skewness_val = pd.Series(yeojohnson_transformation).skew().round(decimals = 4)
                yeojohnson_skewness.append(yeojohnson_skewness_val)

                # Quantile transformation
                quantiletransf_transformation = QuantileTransformer(output_distribution = "normal", 
                                                              random_state = 0).fit_transform(transported_data.values.reshape((-1,1)))
                quantiletransf_skewness_val = pd.DataFrame(quantiletransf_transformation).skew()[0].round(decimals = 4)
                quantiletransf_skewness.append(quantiletransf_skewness_val)

            # Join all skewness data
            self.__transformed_skewness = self.__skewness.copy(deep = False)
            self.__transformed_skewness.loc[:, "Log"] = log_skewness
            self.__transformed_skewness.loc[:, "Sqrt"] = sqrt_skewness
            self.__transformed_skewness.loc[:, "YeoJohnson"] = yeojohnson_skewness
            self.__transformed_skewness.loc[:, "QuantileTransf"] = quantiletransf_skewness

            # Median of skewness
            print("Median skewness per transformation:")
            print(self.__transformed_skewness.median())

            print(f"The smallest median skewness is for: {self.__transformed_skewness.median().abs().nsmallest(1)}")

            # Save the data
            self.__transformed_skewness.to_csv("transformed_skewness.csv", index = True)
   
            # Tranform the data selecting the method
            if method == "log":
                self.__transformed_data = pd.DataFrame()
                for numerical_variable in self.__numerical_variables_list:
                    self.__transformed_data["Log_"+numerical_variable] = np.log(self.__data[numerical_variable])
                self.__transformed_data.to_csv("log_transformed_data.csv", index = True)

            elif method == "sqrt":
                self.__transformed_data = pd.DataFrame()
                for numerical_variable in self.__numerical_variables_list:
                    self.__transformed_data["SQRT_"+numerical_variable] = np.sqrt(self.__data[numerical_variable])
                self.__transformed_data.to_csv("sqrt_transformed_data.csv", index = True)
                   
            elif method == "yeojohnson":
                self.__transformed_data = pd.DataFrame()
                for numerical_variable in self.__numerical_variables_list:
                    self.__transformed_data["YeoJohnson_"+numerical_variable],_ = stats.yeojohnson(self.__data[numerical_variable])
                self.__transformed_data.to_csv("yeojohnson_transformed_data.csv", index = True)

            elif method == "quantile":
                self.__transformed_data = pd.DataFrame()
                for numerical_variable in self.__numerical_variables_list:
                    self.__transformed_data["QuantileTransf_"+numerical_variable] = pd.DataFrame(QuantileTransformer(output_distribution = "normal", 
                                                                         random_state = 0).fit_transform(self.__data[numerical_variable].values.reshape((-1,1))))
                self.__transformed_data.to_csv("quantile_transformed_data.csv", index = True)
   
    def run_pipeline(self, **kwargs):
        self.__load_data()
        self.__check_nulls()
        self.__check_duplicates()
        self.__statistics()
        self.__save_clean_data()
        self.__correlation_matrix()
        self.__variance_inflation_factor()
        self.__interquartile_range()
        self.__skewness(kwargs.get("transformation", False), kwargs.get("method", None))