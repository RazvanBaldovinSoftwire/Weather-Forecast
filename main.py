from datetime import datetime

import pandas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def dataset_info(dataframe: pd.DataFrame):
    """ TODO:
    """
    pd.DataFrame.info(dataframe)

    print("Duplicate rows:")
    duplicates = dataframe.duplicated()
    dupes_exist = False
    for i in duplicates:
        if i is True:
            print(i)
            dupes_exist = True

    if not dupes_exist:
        print("None")

    most_common_weather = dataframe.weather.mode()[0]
    print(f"Most common weather: {most_common_weather} ({dataframe.weather.value_counts()[most_common_weather]} days)")


def temp_max_histplot(dataframe: pd.DataFrame):
    """ TODO:
    """
    sns.histplot(data=dataframe, x="temp_max", bins=40)
    plt.title("Temperature Max Histogram (40 bins)")
    plt.show()


def temp_max_facegrid_lineplot(dataframe: pd.DataFrame):
    """ TODO:
    """
    dataframe['month'] = pd.DatetimeIndex(dataframe['date']).month
    dataframe['year'] = pd.DatetimeIndex(dataframe['date']).year

    graph = sns.FacetGrid(data=dataframe, col="year")
    graph.map_dataframe(sns.lineplot, "month", "temp_max")
    graph.set(xlabel="Month", ylabel="Max Temperature")
    graph.set(xlim=(0, 12))
    plt.show()


def precipitation_facegrid_scatterplot(dataframe: pd.DataFrame):
    """ TODO:
    """
    dataframe['month'] = pd.DatetimeIndex(dataframe['date']).month
    dataframe['year'] = pd.DatetimeIndex(dataframe['date']).year

    graph = sns.FacetGrid(data=dataframe, col="year")
    graph.map_dataframe(sns.scatterplot, "month", "wind")
    graph.set(xlabel="Month", ylabel="Precipitation")
    graph.set(xlim=(0, 12))
    graph.set
    plt.show()

def weather_countplot(dataframe: pd.DataFrame):
    """ TODO:
    """
    graph = sns.countplot(data=dataframe, x="weather")
    graph.set(xlabel="Weather", ylabel="Count")
    graph.bar_label(graph.containers[0], label_type='edge')
    plt.title("Weather Countplot")
    plt.show()

def weather_piechart(dataframe: pd.DataFrame):
    """ TODO:
    """
    dataframe["weather"].value_counts().plot(kind="pie", autopct="%1.1f%%")
    plt.title("Weather Piechart")

    plt.show()

def lr_predictor_random_split(dataframe: pd.DataFrame):
    """ TODO:
    """


def lr_predictor_default_split(dataframe: pd.DataFrame):
    """ TODO:
    """


def svr_predictor_default_split(dataframe: pd.DataFrame):
    """ TODO:
    """


def main():
    df = pd.read_csv('seattle-weather.csv')
    dataset_info(df)
    temp_max_histplot(df)
    temp_max_facegrid_lineplot(df)
    precipitation_facegrid_scatterplot(df)
    weather_countplot(df)
    weather_piechart(df)

if __name__ == '__main__':
    main()
