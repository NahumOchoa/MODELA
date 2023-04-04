import abc
import re
from typing import Any, Dict

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from pandas import DataFrame
from scipy.stats import boxcox
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder

import config


class AbstractExecutor(abc.ABC):
    @abc.abstractmethod
    def execute(self) -> Any:
        pass


class LoadFileExecutor(AbstractExecutor):
    """Execute the load data from file command"""

    def __init__(self, file_name: str, work_directory: str):
        """
        Constructor for the LoadFileExecutor class that receives the name of the file to load
        :param file_name: The name of the file to load
        :param work_directory: The directory of the file to load
        """
        self.file_name = file_name
        self.work_directory = work_directory
        self.pattern = r"'[\w\d\-\_]+\.(csv|xlsx|txt)'"

    def execute(self) -> DataFrame:
        """
        Execute the load data from file command and return a pandas dataframe
        :return: The loaded dataframe, or None if there was an error
        """
        match = re.search(self.pattern, self.file_name)
        if not match:
            print(f"Invalid file name: {self.file_name}")
            return None
        file_ext = match.group(1)
        if file_ext == 'csv':
            try:
                return pd.read_csv(self.work_directory[1:-1] + match.group(0)[1:-1])
            except Exception as e:
                print(f"Failed to load CSV file: {str(e)}")
                return None
        elif file_ext == 'xlsx':
            try:
                return pd.read_excel(self.work_directory[1:-1] + match.group(0)[1:-1])
            except Exception as e:
                print(f"Failed to load XLSX file: {str(e)}")
                return None
        else:
            print(f"Invalid file extension: {file_ext}")
            return None


class SetExecutor(AbstractExecutor):
    """Execute the set command to store variables"""

    def __init__(self, t: tuple):
        """
        Constructor for the SetExecutor class that receives the set command token to execute and store the variables
        :param t: The set command token
        """
        self.t = t
        self.names = {}

    def execute(self) -> Dict[str, Any]:
        """
        Execute the set command and return the dictionary of variables
        :return: The dictionary of variables
        """
        if len(self.t) != 4 and not (len(self.t) == 5 and self.t[3] == '='):
            print("Invalid set command format.")
            return self.names
        var_name = self.t[1] if len(self.t) == 4 else self.t[2]
        var_value = self.t[3] if len(self.t) == 4 else self.t[4]
        self.names[var_name] = var_value
        return self.names


class MinMaxExecutor(AbstractExecutor):
    # Execute the MinMaxScaler preprocessing command
    def __init__(self, df: DataFrame, cols: list[str]):
        """
        Constructor for the MinMaxExecutor class that receives the DataFrame to preprocess
        and the columns to scale using MinMaxScaler
        :param df: The DataFrame to preprocess
        :param cols: The list of columns to scale using MinMaxScaler
        """
        self.df = df
        self.cols = cols

    def execute(self) -> pd.DataFrame:
        """
        Execute the MinMaxScaler preprocessing command and return the preprocessed DataFrame
        :return: The preprocessed DataFrame
        """
        scaler = MinMaxScaler()
        for col in self.cols:
            scaled_col = scaler.fit_transform(np.array(self.df[col]).reshape(-1, 1))
            scaled_col = pd.DataFrame(scaled_col)
            # Rename the columns of the scaled feature
            scaled_col.columns = [col + '_scaled']
            self.df = pd.concat([self.df, scaled_col], axis=1)
        return self.df


class StandardGaussianExecutor(AbstractExecutor):
    # Execute the StandardScaler and GaussianTransformer preprocessing command
    def __init__(self, df: DataFrame, cols: list[str]):
        """
        Constructor for the StandardGaussianExecutor class that receives the DataFrame to preprocess
        :param df: The DataFrame to preprocess
        :param cols: A list of columns to apply the preprocessing on
        """
        self.df = df
        self.cols = cols

    def execute(self) -> pd.DataFrame:
        """
        Execute the StandardScaler and GaussianTransformer preprocessing command and return the preprocessed DataFrame
        :return: The preprocessed DataFrame
        """
        # StandardScaler
        scaler = preprocessing.StandardScaler()
        for col in self.cols:
            scaled_col = scaler.fit_transform(np.array(self.df[col]).reshape(-1, 1))
            self.df[col] = pd.DataFrame(scaled_col, columns=[col])

        return self.df


class OneHotExecutor(AbstractExecutor):
    # Execute the OneHotEncoder preprocessing command
    def __init__(self, df: DataFrame, cols: list[str]):
        """
        Constructor for the OneHotExecutor class that receives the DataFrame to preprocess
        and the columns to one-hot-encode
        :param df: The DataFrame to preprocess
        :param cols: The list of columns to one-hot-encode
        """
        self.df = df
        self.cols = cols

    def execute(self) -> pd.DataFrame:
        """
        Execute the OneHotEncoder preprocessing command and return the preprocessed DataFrame
        :return: The preprocessed DataFrame
        """
        enc = OneHotEncoder()
        for col in self.cols:
            enc.fit(np.array(self.df[col]).reshape(-1, 1))
            encoded_col = enc.transform(np.array(self.df[col]).reshape(-1, 1)).toarray()
            encoded_col = pd.DataFrame(encoded_col)
            # Rename the columns of the one-hot-encoded feature
            encoded_col.columns = [col + '_' + str(i) for i in range(encoded_col.shape[1])]
            self.df = pd.concat([self.df, encoded_col], axis=1)
        # Remove the original columns that were one-hot-encoded
        self.df.drop(columns=self.cols, inplace=True)
        return self.df


class LinearRegressionExecutor(AbstractExecutor):
    # Execute the LinearRegression command
    def __init__(self, df: DataFrame, formula: str):
        """
        Constructor for the LinearRegressionExecutor class that receives the DataFrame to preprocess
        and the columns to one-hot-encode
        :param df: The DataFrame to preprocess
        :param explanatory_variables: The list of explanatory variables
        :param response_variable: The response variable
        """
        self.df = df
        self.formula = formula

    def execute(self) -> pd.DataFrame:
        """
        Execute the LinearRegression command and return the preprocessed DataFrame
        :return: The preprocessed DataFrame
        """
        # Split the formula into explanatory variables and response variable
        formula = f"""{self.formula}"""
        model = smf.ols(formula=formula, data=self.df)
        fitted = model.fit()
        summary = fitted.summary()
        # Extrae los coeficientes, p-values, R-Squared y MSE del resumen
        coef_pattern = re.compile(
            r'(\b[A-Z]\d?\b)\s+([\-\d\.]+)\s+([\-\d\.]+)\s+([\-\d\.]+)\s+([\-\d\.]+)\s+([\-\d\.]+)\s+([\-\d\.]+)\s+([\-\d\.]+)\s+([\-\d\.]+)')
        coef_lines = re.findall(coef_pattern, summary.tables[1].as_text())

        # Crea un diccionario para almacenar los resultados
        results = {}

        # Agrega los coeficientes, p-values, R-Squared y MSE al diccionario
        for line in coef_lines:
            var_name = line[0]
            results[var_name] = {
                'coef': float(line[1]),
                'std_err': float(line[2]),
                't_stat': float(line[3]),
                'p_value': float(line[4])
            }

        results['R-Squared'] = {
            'value': fitted.rsquared,
            'adj_value': fitted.rsquared_adj
        }

        results['MSE'] = {
            'value': fitted.mse_resid,
            'nobs': fitted.nobs
        }

        # Imprime los resultados
        for var, vals in results.items():
            if 'coef' in vals:
                print(f'{var}: Coef={vals["coef"]}, p-value={vals["p_value"]}')
            elif 'value' in vals:
                print(f'{var}: {vals["value"]}')

        print(fitted.summary())
        return self.df


class ExecutorFactory:
    # Factory to create the executors
    def __init__(self):
        """
        Constructor for the ExecutorFactory class
        that creates the executors
        """
        pass

    def get_executor(self, command_type: str, parameters: dict) -> AbstractExecutor:
        """
        Get the executor for the command type and parameters received
        :param command_type: The type of the command
        :param parameters: The parameters of the command to execute
        :return: The executor for the command
        """
        if command_type == "LOAD_DATA_FROM_FILE":
            file_name = parameters.get('file_name')
            work_directory = parameters.get('work_directory')
            if file_name is None:
                raise ValueError("Missing file_name parameter in LOAD_DATA_FROM_FILE command.")
            if work_directory is None:
                raise ValueError("Missing work_directory parameter in LOAD_DATA_FROM_FILE command.")
            return LoadFileExecutor(file_name, work_directory)
        elif command_type == "SET":
            set_cmd = parameters.get('set')
            if set_cmd is None:
                raise ValueError("Missing set parameter in SET command.")
            return SetExecutor(set_cmd)
        elif command_type == "MODEL":
            input_command = parameters.get('input_command')
            df = parameters.get('df')
            match = re.match(config.t_MODEL_PATTERN, input_command)
            if match:
                type = match.group(1)
                command_type_mo = match.group(2)
                formula = match.group(3)
            else:
                raise ValueError("Invalid MODEL command.")
            if type is None:
                raise ValueError("Missing type parameter in MODEL command.")
            if command_type_mo is None:
                raise ValueError("Missing command_type parameter in MODEL command.")
            if formula is None:
                raise ValueError("Missing formula parameter in MODEL command.")
            if df is None:
                raise ValueError("Missing df parameter in MODEL command.")
            if type.lower() == "regression":
                return self.get_regression_executor(command_type_mo, df, formula)

            else:
                raise ValueError(f"Invalid MODEL command{type}.")
        elif command_type == "PREPROCESSING":
            input_command = parameters.get('input_command')
            df = parameters.get('df')
            match = re.match(config.t_PREPROCESSING_PATTERN, input_command)
            if match:
                task = match.group(1)
                command_type_pre = match.group(2)
                cols = match.group(3).split(',')
            else:
                raise ValueError("Invalid preprocessing command.")
            if task is None:
                raise ValueError("Missing task parameter in PREPROCESSING command.")
            if command_type_pre is None:
                raise ValueError("Missing command_type parameter in PREPROCESSING command.")
            if df is None:
                raise ValueError("Missing df parameter in PREPROCESSING command.")
            if task.lower() == "scaling":
                return self.get_scale_preprocessor(command_type_pre, df, cols)
            elif task.lower() == "encoding":
                return self.get_encode_preprocessor(command_type_pre, df, cols)
            else:
                raise ValueError(f"Invalid preprocessing command: {command_type}")
        else:
            raise ValueError(f"Unknown command type {command_type}")

    def get_scale_preprocessor(self, command_type: str, df: DataFrame, cols: list[str]) -> AbstractExecutor:
        """
        Get the scale preprocessor for the command type and DataFrame received
        :param command_type: The type of the command
        :param df: The DataFrame to preprocess
        :param cols: The list of columns to scale
        :return: The scale preprocessor for the command
        """
        if command_type.lower() == "min_max":
            return MinMaxExecutor(df, cols)
        elif command_type.lower() == "gaussian":
            return StandardGaussianExecutor(df, cols)
        else:
            raise ValueError(f"Invalid preprocessing command: {command_type}")

    def get_encode_preprocessor(self, command_type: str, df: DataFrame, cols: list[str]) -> AbstractExecutor:
        """
        Get the encode preprocessor for the command type and DataFrame received
        :param command_type: The type of the command
        :param df: The DataFrame to preprocess
        :param cols: The list of columns to one-hot-encode
        :return: The encode preprocessor for the command
        """
        if command_type.lower() == "one_hot":
            return OneHotExecutor(df, cols)
        else:
            raise ValueError(f"Invalid preprocessing command: {command_type}")

    def get_regression_executor(self, command_type: str, df: DataFrame, formula: str) -> AbstractExecutor:
        """
        Get the regression executor for the command type and DataFrame received
        :param command_type: The type of the command
        :param df: The DataFrame to preprocess
        :param formula: The formula for the regression
        :return: The regression executor for the command
        """
        if command_type.lower() == "lr":
            return LinearRegressionExecutor(df, formula)
        else:
            raise ValueError(f"Invalid regression command: {command_type}")
