import abc
import re
from typing import Any
import pandas as pd
from pandas import DataFrame


class AbstractExecutor(abc.ABC):
    @abc.abstractmethod
    def execute(self):
        pass


class LoadFileExecutor(AbstractExecutor):
    # Execute the load data from file command
    def __init__(self, file_name, work_directory):
        """
        Constructor for the LoadFileExecutor class
        that receives the name of the file to load
        :param file_name: The name of the file to load
        """
        self.file_name = file_name
        self.work_directory = work_directory
        self.pattern = r"'[\w\d\-\_]+\.(csv|xlsx|txt)'"

    def execute(self) -> pd.DataFrame | None | Any:
        """
        Execute the load data from file command
        and return a pandas dataframe
        """

        match = re.search(self.pattern, self.file_name)
        if match:
            file_ext = match.group(1)
            if file_ext == 'csv':
                try:
                    return pd.read_csv(self.work_directory[1:-1] + match.group(0)[1:-1])
                except Exception as e:
                    raise ValueError(f"Failed to load CSV file: {str(e)}")
            elif file_ext == 'xlsx':
                try:
                    return pd.read_excel(self.work_directory[1:-1] + match.group(0)[1:-1])
                except Exception as e:
                    raise ValueError(f"Failed to load XLSX file: {str(e)}")
            else:
                raise ValueError(f"Invalid file extension: {file_ext}")
        else:
            return None


class SetExecutor(AbstractExecutor):
    # Execute the set command to store variables
    def __init__(self, t: object):
        """
        Constructor for the SetExecutor class that receives the set command token
        to execute and store the variables
        :param t: The set command token
        """
        self.t = t
        self.names = {}

    def execute(self) -> dict:
        """
        Execute the set command and return the dictionary of variables
        :return: The dictionary of variables
        """
        try:
            if len(self.t) == 4:
                self.names[self.t[1]] = self.t[3]
                return self.names
            elif len(self.t) == 5 and self.t[3] == '=':
                self.names[self.t[2]] = self.t[4]
                return self.names
            else:
                raise ValueError("Invalid set command format.")
        except (IndexError, ValueError) as e:
            print(f"Error executing set command: {str(e)}")
            return self.names


class ExecutorFactory:
    # Factory to create the executors
    def __init__(self):
        """
        Constructor for the ExecutorFactory class
        that creates the executors
        """
        pass

    def getExecutor(self, type: str, parameters: dict) -> AbstractExecutor:
        """
        Get the executor for the command type and parameters received
        :param type: The type of the command
        :param parameters: The parameters of the command to execute
        :return: The executor for the command
        """
        if type == "LOAD_DATA_FROM_FILE":
            file_name = parameters.get('file_name')
            work_directory = parameters.get('work_directory')
            if file_name is None:
                raise ValueError("Missing file_name parameter in LOAD_DATA_FROM_FILE command.")
            if work_directory is None:
                raise ValueError("Missing work_directory parameter in LOAD_DATA_FROM_FILE command.")
            return LoadFileExecutor(file_name, work_directory)
        elif type == "SET":
            set_cmd = parameters.get('set')
            if set_cmd is None:
                raise ValueError("Missing set parameter in SET command.")
            return SetExecutor(set_cmd)
        else:
            raise ValueError(f"Unknown command type {type}")