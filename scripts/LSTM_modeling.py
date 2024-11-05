import os
from datetime import datetime
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error,r2_score

class LSTM_Modelling:
    def train_lstm(self,data,model_name):
        data=data[['Date','Price']]
        data['Price'] = data['Price'].astype(float)

        # Split the data into training and testing sets (80-20 split)
        train_size = int(len(data) * 0.8)
        train_data, test_data = data['Price'][:train_size], data['Price'][train_size:]

        # Scale the 'Price' column
        scaler = MinMaxScaler(feature_range=(0, 1))
        train_scaled = scaler.fit_transform(train_data.values.reshape(-1, 1))
        test_scaled = scaler.transform(test_data.values.reshape(-1, 1))

        # Function to create dataset with time steps
        def create_dataset(data, time_step=1):
            X, Y = [], []
            for i in range(len(data) - time_step - 1):
                X.append(data[i:(i + time_step), 0])
                Y.append(data[i + time_step, 0])
            return np.array(X), np.array(Y)

        # Set time step (e.g., 60 days)
        time_step = 60
        X_train, y_train = create_dataset(train_scaled, time_step)
        X_test, y_test = create_dataset(test_scaled, time_step)

        # Reshape data to be compatible with LSTM input (samples, time steps, features)
        X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
        X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

        # Build the LSTM model
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(units=1))  # Output layer for regression

        model.compile(optimizer='adam', loss='mean_squared_error')

        # Train the model
        history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test), verbose=1)

        # Make predictions on the test set
        train_predict = model.predict(X_train)
        test_predict = model.predict(X_test)

        # Inverse transform predictions to original scale
        train_predict = scaler.inverse_transform(train_predict)
        test_predict = scaler.inverse_transform(test_predict)
        y_train = scaler.inverse_transform(y_train.reshape(-1, 1))
        y_test = scaler.inverse_transform(y_test.reshape(-1, 1))
        
        # Create the folder if it doesn't exist
        folder_path='models/'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # Generate timestamp in format dd-mm-yyyy-HH-MM-SS-00
        timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S-00")
        
        # Create a filename with the timestamp
        filename = f'{folder_path}{model_name}-{timestamp}.pkl'
        
        # Save the model using pickle
        with open(filename) as file:
            pickle.dump(model, file)
        
        print(f"Model saved as {filename}")
        

        return test_data,y_test,test_predict
    
    def evaluate_lstm_model(self,y_true,y_pred):        
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        r2_Score=r2_score(y_true,y_pred)
        mape = mean_absolute_percentage_error(y_true, y_pred)
        
        # Print metrics
        print("Mean Absolute Error (MAE):", mae)
        print("Mean Squared Error (MSE):", mse)
        print("Root Mean Squared Error (RMSE):", rmse)
        print("R Square Score (r2_score):", r2_Score)
        print("Mean Absolute Percentage Error (MAPE):", mape, "%")
        
    def plot_result(self,y_test,y_pred):
        actual_vs_prediction=pd.DataFrame(y_test, columns=["original_Price"])
        actual_vs_prediction["predicted_Price"]=pd.DataFrame(y_pred)

        plt.figure(figsize=(14, 5))
        plt.plot(actual_vs_prediction.index, actual_vs_prediction['original_Price'], label="Original Price")
        plt.plot(actual_vs_prediction.index,actual_vs_prediction['predicted_Price'], label="Predicted Price")
        plt.title('LSTM Model Brent Oil Price Prediction')
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.show()