import abc
import re
from typing import Any, Dict, Union
import pandas as pd
from pandas import DataFrame
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder


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
    def __init__(self, df: DataFrame):
        """
        Constructor for the MinMaxExecutor class that receives the DataFrame to preprocess
        :param df: The DataFrame to preprocess
        """
        self.df = df

    def execute(self) -> pd.DataFrame:
        """
        Execute the MinMaxScaler preprocessing command and return the preprocessed DataFrame
        :return: The preprocessed DataFrame
        """
        scaler = MinMaxScaler()
        return pd.DataFrame(scaler.fit_transform(self.df), columns=self.df.columns)


class GaussianExecutor(AbstractExecutor):
    # Execute the GaussianScaler preprocessing command
    def __init__(self, df: DataFrame):
        """
        Constructor for the GaussianExecutor class that receives the DataFrame to preprocess
        :param df: The DataFrame to preprocess
        """
        self.df = df

    def execute(self) -> pd.DataFrame:
        """
        Execute the GaussianScaler preprocessing command and return the preprocessed DataFrame
        :return: The preprocessed DataFrame
        """
        scaler = StandardScaler()
        return pd.DataFrame(scaler.fit_transform(self.df), columns=self.df.columns)


class OneHotExecutor(AbstractExecutor):
    # Execute the OneHotEncoder preprocessing command
    def __init__(self, df: DataFrame):
        """
        Constructor for the OneHotExecutor class that receives the DataFrame to preprocess
        :param df: The DataFrame to preprocess
        """
        self.df = df

    def execute(self) -> pd.DataFrame:
        """
        Execute the OneHotEncoder preprocessing command and return the preprocessed DataFrame
        :return: The preprocessed DataFrame
        """
        encoder = OneHotEncoder()
        return pd.DataFrame(encoder.fit_transform(self.df).toarray(), columns=self.df.columns)


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
        elif command_type == "PREPROCESSING":
            task = parameters.get('task')
            command_type = parameters.get('command_type')
            df = parameters.get('df')
            if task is None:
                raise ValueError("Missing task parameter in PREPROCESSING command.")
            if command_type is None:
                raise ValueError("Missing command_type parameter in PREPROCESSING command.")
            if df is None:
                raise ValueError("Missing df parameter in PREPROCESSING command.")
            if task.lower() == "scaling":
                return self.get_scale_preprocessor(command_type, df)
            elif task.lower() == "encoding":
                return self.get_encode_preprocessor(command_type, df)
            else:
                raise ValueError(f"Invalid preprocessing command: {command_type}")
        else:
            raise ValueError(f"Unknown command type {command_type}")

    def get_scale_preprocessor(self, command_type: str, df: DataFrame) -> AbstractExecutor:
        """
        Get the scale preprocessor for the command type and DataFrame received
        :param command_type: The type of the command
        :param df: The DataFrame to preprocess
        :return: The scale preprocessor for the command
        """
        if command_type.lower() == "min_max":
            return MinMaxExecutor(df)
        elif command_type.lower() == "gaussian":
            return GaussianExecutor(df)
        else:
            raise ValueError(f"Invalid preprocessing command: {command_type}")

    def get_encode_preprocessor(self, command_type: str, df: DataFrame) -> AbstractExecutor:
        """
        Get the encode preprocessor for the command type and DataFrame received
        :param command_type: The type of the command
        :param df: The DataFrame to preprocess
        :return: The encode preprocessor for the command
        """
        if command_type.lower() == "one_hot":
            return OneHotExecutor(df)
        else:
            raise ValueError(f"Invalid preprocessing command: {command_type}")
