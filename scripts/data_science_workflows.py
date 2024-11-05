import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import ruptures as rpt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings("ignore")
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the data
data = pd.read_csv('../data/brent_oil_prices.csv', parse_dates=['Date'], dayfirst=True)
data.set_index('Date', inplace=True)
print(data.head())

# Assuming your 'Price' column contains the oil prices
class OilPriceAnalysis:
    def __init__(self, data):
        self.data = data

    def seasonal_decomposition(self):
        # Decompose the time series to analyze trend and seasonality
        decomposition = seasonal_decompose(self.data['Price'], model='additive', period=30)
        
        # Plot the decomposition
        plt.figure(figsize=(14, 10))
        decomposition.plot()
        plt.suptitle("Seasonal Decomposition of Brent Oil Prices", fontsize=14)
        plt.show()

    def change_point_analysis(self):
        # Prepare the price data as an array
        price_series = self.data['Price'].values

        # Define the model as 'rbf' for kernel-based change point detection
        model = "rbf"
        algo = rpt.Pelt(model=model).fit(price_series)

        # Increase the penalty to reduce the number of change points
        change_points = algo.predict(pen=15)  # Adjust the penalty as needed

        # Plotting the results
        plt.figure(figsize=(12, 6))
        plt.plot(self.data.index, price_series, label="Brent Oil Prices", color='blue')

        # Plot each change point, with only one label in the legend
        for i, cp in enumerate(change_points):
            if i == 0:  # Add label only for the first change point
                plt.axvline(self.data.index[cp - 1], color='red', linestyle='--', label="Change Point")
            else:
                plt.axvline(self.data.index[cp - 1], color='red', linestyle='--')

        plt.legend()
        plt.title("Change Point Analysis on Brent Oil Prices")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.show()


    def check_stationarity(self):
        """
        Checks the stationarity of the 'Price' column using the Augmented Dickey-Fuller (ADF) test.
    
    If the series is non-stationary (p > 0.05), applies first differencing and plots the differenced series.
    """
        if self.data is None:
            print("Data not loaded. Please load data before calling check_stationarity.")
            return

        print("Performing Augmented Dickey-Fuller test for stationarity.")
        result = adfuller(self.data['Price'])
        print(f"ADF Statistic: {result[0]}")
        print(f"p-value: {result[1]}")
    
        if result[1] > 0.05:
            print("Data is non-stationary; applying first differencing.")
            self.data['price_diff'] = self.data['Price'].diff()

            # Drop the NaN value resulting from differencing
            plt.figure(figsize=(14, 6))
            plt.plot(self.data.index[1:], self.data['price_diff'].dropna(), color='green')  # Use dropna() to align lengths
            plt.title('Differenced Brent Oil Prices')
            plt.xlabel("Date")
            plt.ylabel("Differenced Price")
            plt.show()
        else:
            print("Data is stationary; proceed without differencing.")


# Check for missing values
print(data.isnull().sum())

# Fill missing values through forward fill
data['Price'].fillna(method='ffill', inplace=True)

# Check for outliers
plt.figure(figsize=(10, 5))
sns.boxplot(x=data['Price'])
plt.title('Boxplot of Brent Oil Prices')
plt.show()

# Plot the time series data
plt.figure(figsize=(15, 7))
plt.plot(data['Price'], label='Brent Oil Price')
plt.xlabel('Date')
plt.ylabel('Price (USD per barrel)')
plt.title('Historical Brent Oil Prices')
plt.legend()
plt.show()

# ACF and PACF plots
plot_acf(data['Price'], lags=50)
plot_pacf(data['Price'], lags=50)
plt.show()


def change_point_analysis(self):
    """
        Performs change point analysis on the 'Price' data using the ruptures library.
        Plots the Brent oil prices and highlights detected change points.
    """
    if self.data is None:
        logging.warning("Data not loaded. Please load data before calling change_point_analysis.")
        return
        
    logging.info("Performing change point analysis.")
        
    # Prepare the price data as an array
    price_series = self.data['Price'].values

    # Define the model as 'rbf' for kernel-based change point detection
    model = "rbf"
    algo = rpt.Pelt(model=model).fit(price_series)

        # Increase the penalty to reduce the number of change points
    change_points = algo.predict(pen=15)  # we can adjust the penalty to find significant changes

        # Plotting the results
    plt.figure(figsize=(12, 6))
    plt.plot(self.data.index, price_series, label="Brent Oil Prices", color='blue')

        # Plot each change point, with only one label in the legend
    for i, cp in enumerate(change_points):
        if i == 0:  # Add label only for the first change point
            plt.axvline(self.data.index[cp - 1], color='red', linestyle='--', label="Change Point")
        else:
            plt.axvline(self.data.index[cp - 1], color='red', linestyle='--')

    plt.legend()
    plt.title("Change Point Analysis on Brent Oil Prices")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.show()
# Check stationarity
result = adfuller(data['Price'])
print(f'ADF Statistic: {result[0]}')
print(f'p-value: {result[1]}')

def plot_histogram(self, column='Price', cmap='viridis'):
        """
        Plots a histogram for the specified column with a colormap and
        includes vertical lines for mean, median, minimum, and maximum values.

        Parameters
        ----------
        column : str, optional
            The column name to plot (default is 'Price').
        cmap : str, optional
            The colormap to use for the histogram (default is 'viridis').
        """
        if self.data is None:
            logging.warning("Data not loaded. Please load data before calling plot_histogram.")
            return

        plt.figure(figsize=(10, 6))

        # Generate histogram values
        hist_values, bins, patches = plt.hist(self.data[column], bins=20, edgecolor='black', alpha=0.7)

        # Apply colormap to each bin
        cmap = plt.get_cmap(cmap)
        for i, patch in enumerate(patches):
            patch.set_facecolor(cmap(i / len(patches)))

        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.title(f'Histogram for {column}')

        # Calculate statistics
        mean_value = self.data[column].mean()
        median_value = self.data[column].median()
        min_value = self.data[column].min()
        max_value = self.data[column].max()

        # Add vertical lines for mean, median, min, and max
        plt.axvline(mean_value, color='red', linestyle='--', label=f'Mean: {mean_value:.2f}')
        plt.axvline(median_value, color='yellow', linestyle='--', label=f'Median: {median_value:.2f}')
        plt.axvline(min_value, color='green', linestyle='--', label=f'Min: {min_value:.2f}')
        plt.axvline(max_value, color='blue', linestyle='--', label=f'Max: {max_value:.2f}')

        # Adding a legend to describe the lines
        plt.legend()
        plt.grid(axis='y', alpha=0.75)  # Add grid for better readability
        plt.show()
        
        logging.info("Histogram plot generated successfully with statistics and colormap.")


# Differencing to make the series stationary
data['Price_diff'] = data['Price'].diff().dropna()

# Fit ARIMA model
model = auto_arima(data['Price_diff'].dropna(), seasonal=False, trace=True)
model.summary()

# Fit model with ARIMA parameters
arima_model = ARIMA(data['Price'], order=(5, 1, 0))
arima_result = arima_model.fit()
print(arima_result.summary())

# Predictions
pred = arima_result.predict(start=len(data), end=len(data) + 30, typ='levels')

# Plot predictions
plt.figure(figsize=(15, 7))
plt.plot(data['Price'], label='Historical Brent Oil Price')
plt.plot(pred, label='ARIMA Predictions', color='red')
plt.xlabel('Date')
plt.ylabel('Price (USD per barrel)')
plt.title('Brent Oil Price Predictions')
plt.legend()
plt.show()

# Calculate metrics
mse = mean_squared_error(data['Price'][-30:], pred[:30])
mae = mean_absolute_error(data['Price'][-30:], pred[:30])
print(f'MSE: {mse}')
print(f'MAE: {mae}')

# Example: Identify significant events and their impact on oil prices
significant_events = {
    '2020-03-09': 'Oil Price War between Saudi Arabia and Russia',
    '2020-04-20': 'Brent Crude Futures Turn Negative'
}

for date, event in significant_events.items():
    date = pd.to_datetime(date)
    if date in data.index:
        prev_date = date - pd.Timedelta(days=1)
        if prev_date in data.index:
            price_change = data.loc[date]['Price'] - data.loc[prev_date]['Price']
            print(f"Event: {event} on {date.strftime('%Y-%m-%d')}")
            print(f"Price Change: {price_change:.2f}\n")
        else:
            print(f"Previous day's data not available for event: {event} on {date.strftime('%Y-%m-%d')}\n")
    else:
        print(f"Data not available for event: {event} on {date.strftime('%Y-%m-%d')}\n")

    