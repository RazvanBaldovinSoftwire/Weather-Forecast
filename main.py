import random

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVR


def dataset_info(dataframe: pd.DataFrame):
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
	sns.histplot(data=dataframe, x="temp_max", bins=40)
	plt.title("Temperature Max Histogram (40 bins)")
	plt.show()


def temp_max_facegrid_lineplot(dataframe: pd.DataFrame):
	dataframe['month'] = pd.DatetimeIndex(dataframe['date']).month
	dataframe['year'] = pd.DatetimeIndex(dataframe['date']).year

	graph = sns.FacetGrid(data=dataframe, col="year")
	graph.map_dataframe(sns.lineplot, "month", "temp_max")
	graph.set(xlabel="Month", ylabel="Max Temperature")
	graph.set(xlim=(0, 12))
	plt.show()


def precipitation_facegrid_scatterplot(dataframe: pd.DataFrame):
	dataframe['month'] = pd.DatetimeIndex(dataframe['date']).month
	dataframe['year'] = pd.DatetimeIndex(dataframe['date']).year

	graph = sns.FacetGrid(data=dataframe, col="year")
	graph.map_dataframe(sns.scatterplot, "month", "wind")
	graph.set(xlabel="Month", ylabel="Precipitation")
	graph.set(xlim=(0, 12))
	plt.show()

def weather_countplot(dataframe: pd.DataFrame):
	graph = sns.countplot(data=dataframe, x="weather")
	graph.set(xlabel="Weather", ylabel="Count")
	graph.bar_label(graph.containers[0], label_type='edge')
	plt.title("Weather Countplot")
	plt.show()

def weather_piechart(dataframe: pd.DataFrame):
	dataframe["weather"].value_counts().plot(kind="pie", autopct="%1.1f%%")
	plt.title("Weather Piechart")

	plt.show()


def modify_dataframe(dataframe: pd.DataFrame):
	dataframe['month'] = pd.DatetimeIndex(dataframe['date']).month
	dataframe['day'] = pd.DatetimeIndex(dataframe['date']).day
	dataframe.loc[dataframe['weather'] == "sun", "weather"] = 0
	dataframe.loc[dataframe['weather'] == "rain", "weather"] = 1
	dataframe.loc[dataframe['weather'] == "snow", "weather"] = 2
	dataframe.loc[dataframe['weather'] == "drizzle", "weather"] = 3
	dataframe.loc[dataframe['weather'] == "fog", "weather"] = 4

	return dataframe


def split_data(dataframe: pd.DataFrame):
	X = dataframe.drop(["temp_max", "date"], axis=1)
	y = dataframe["temp_max"]

	return X, y


def plot_predictions(y_test, y_pred):
	plt.plot(range(len(y_test)), y_test, color='blue', linewidth=0.7)
	plt.plot(range(len(y_pred)), y_pred, color='red', linewidth=0.7)
	plt.legend(['Actual', 'Predicted'])
	plt.title("Actual vs Predicted Maximum Temperature over Time")
	plt.xlabel("Days")
	plt.ylabel("Temperature")
	plt.show()

def lr_predictor_random_split(dataframe: pd.DataFrame):
	dataframe = modify_dataframe(dataframe)

	test_split = random.uniform(0, 1)
	train, test = train_test_split(dataframe, test_size=test_split, train_size=1-test_split, shuffle=True)
	print("Random split")
	print(f"train_split: {1-test_split}")
	print(f"test_split: {test_split}")

	X_train, y_train = split_data(train)
	X_test, y_test = split_data(test)

	reg = LinearRegression().fit(X_train, y_train)

	y_predicted = reg.predict(X_test)

	plot_predictions(y_test, y_predicted)
	print(f"Mean Squared Error: {mean_squared_error(y_test, y_predicted)}")
	print(f"r2 score: {r2_score(y_test, y_predicted)}")


def lr_predictor_default_split(dataframe: pd.DataFrame):
	dataframe = modify_dataframe(dataframe)

	train, test = train_test_split(dataframe, test_size=0.2, train_size=0.8, shuffle=True)

	X_train, y_train = split_data(train)
	X_test, y_test = split_data(test)

	reg = LinearRegression().fit(X_train, y_train)

	y_predicted = reg.predict(X_test)

	plot_predictions(y_test, y_predicted)
	print(f"Mean Squared Error: {mean_squared_error(y_test, y_predicted)}")
	print(f"r2 score: {r2_score(y_test, y_predicted)}")


def svr_predictor_default_split(dataframe: pd.DataFrame):
	dataframe = modify_dataframe(dataframe)

	train, test = train_test_split(dataframe, test_size=0.2, train_size=0.8, shuffle=False)

	X_train, y_train = split_data(train)
	X_test, y_test = split_data(test)

	reg = make_pipeline(StandardScaler(), LinearSVR(tol=1e-5))

	reg.fit(X_train, y_train)

	y_predicted = reg.predict(X_test)

	plot_predictions(y_test, y_predicted)
	print(f"Mean Squared Error: {mean_squared_error(y_test, y_predicted)}")
	print(f"r2 score: {r2_score(y_test, y_predicted)}")

def main():
	df = pd.read_csv('seattle-weather.csv')
	dataset_info(df)
	# temp_max_histplot(df)
	# temp_max_facegrid_lineplot(df)
	# precipitation_facegrid_scatterplot(df)
	# weather_countplot(df)
	# weather_piechart(df)
	# lr_predictor_random_split(df)
	# lr_predictor_default_split(df)
	# svr_predictor_default_split(df)

if __name__ == '__main__':
	main()
