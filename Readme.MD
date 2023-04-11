# Modela

Modela is a simple language designed to help data analysts and scientists to automate data preprocessing tasks. 

## Installation

To install the library to use, please run the following command:

pip install -r requirements.txt


## Usage

To use Modela, run the main.py and input any next commands:

- `SET <variable> = <value>`: Sets a variable to a value.
- `LOAD DATA FROM FILE(source=<data path>, type=<data type>)`: Loads data from a file. The data type can be either `csv` or `xlsx`.
- `PREPROCESSING(type=<preprocessing type>, method=<type algorithm>, cols=<name of cols aply preprossesing>)`: Applies a preprocessing method to the data. The preprocessing type can be either `encoding` or `standardization`. The method can be either `min-max`, `gaussian` and `one_hot`. The cols can be a list of columns names or a single column name.
- `MODEL(type=<Model type>,learner=<Method type>,formula=<Formula>)`: Applies a model to the data. The model type can be either `regression`. The method can be either `linear`. The formula can be a text with name of cols. 

## Examples

### Example 1

This example shows how to load a CSV file, apply a min-max scaling to the `age` and `salary` columns and then apply a one-hot encoding to the `gender` column.

```
LOAD DATA FROM FILE(source='data.csv', type=csv)
PREPROCESSING(type=scaling, method=min-max, cols=[age,salary])
```

### Example 2

This example shows how to load an Excel file, apply a gaussian scaling to the `age` and `salary` columns and then apply a one-hot encoding to the `gender` column.

```
LOAD DATA FROM FILE(source='data.xlsx', type=xlsx)
PREPROCESSING(type=scaling, method=gaussian, cols=[age,salary])
PREPROCESSING(type=enconding, method=one_hot, cols=[gender])
```


### Example 3

This example shows how to load a CSV file, apply a min-max scaling to the `age` and `salary` columns and then apply a one-hot encoding to the `gender` columns and apply a linear regression model.

```
LOAD DATA FROM FILE(source='data.csv', type=csv)
PREPROCESSING(type=scaling, method=min_max, cols=[age,salary])
PREPROCESSING(type=encoding, method=one_hot, cols=[gender])
MODEL(type=regression, learner=lr, formula=gender~age+salary)
```

## Contributing

To contribute to Modela, please follow these steps:

1. Fork this repository
2. Create a new branch (`git checkout -b new-feature`)
3. Make your changes and commit them (`git commit -am 'Added a new feature'`)
4. Push your changes to your fork (`git push origin new-feature`)
5. Create a pull request

## License

Modela is licensed under the MIT License. See `LICENSE` for more information.