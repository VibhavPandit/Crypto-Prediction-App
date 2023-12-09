# Crypto Prediction App

## Overview
The Crypto Prediction App is an advanced tool designed to assist users in making informed decisions about cryptocurrency investments. Utilizing a sophisticated Random Forest algorithm, the application analyzes real-time data to predict the future value of various cryptocurrencies. Key features include calculating moving averages and the Relative Strength Index (RSI), which are crucial for understanding market trends. The app integrates seamlessly with live data from CoinAPI.io API, ensuring that predictions are based on the most current market information.

## Installation and Setup
To set up the application, please follow these steps:

1. **Download and Setup:**
   - Download the application files without altering their locations to maintain the file structure integrity.

2. **Database Configuration:**
   - Set up a MySQL server.
   - Provide the necessary details such as the host name, user name, password, and database name in the application's configuration settings. Make these changes in the database.py file like this
     ```
     db_config = {
      'host': 'localhost', 
      'user': 'root',  
      'password': 'password123', 
      'database': 'crypto_prediction'
      }
     
     ```

3. **Running the Application:**
   - Launch the Flask application `stocks.py` by executing the command:
     ```
     python stocks.py
     ```
   - This initiates the server and hosts the application locally.

4. **Accessing the Web Interface:**
   - Navigate to the provided local address in your web browser.
   - The landing page will prompt you to select a cryptocurrency.
   - After selection, the app will provide a prediction and recommend whether to "BUY" or "SELL" the selected coin.
  
5. **Building Docker Files**
   - Make sure you have DockerHub installed in your system.
   - There is a Docker file called ModelDockerfile.txt
   - Open cmd and locate to this project file directory in your local system.
   - Execute these codes to create the docker files.
     ```
     docker build -t application-name-of-your-choice -f ModelDockerfile.txt .
     ```
     ```
     docker run -p 5000:5000 application-name
     ```
6. **Kubernetes**
   - There are two .yaml files called deployment.yaml and service.yaml
   - Execute the below codes to get the kubernetes up and running
     ```
     kubectl apply -f deployment.yaml
     kubectl get deployments
     ```

     ```
     kubectl apply -f service.yaml
     kubectl get services
     ```

## Usage Limitations
- Please note that the application allows a maximum of 100 requests per user.

## Conclusion
This Crypto Prediction App serves as a powerful tool for both novice and experienced cryptocurrency traders, offering real-time, data-driven insights to guide trading decisions. Its user-friendly interface and robust backend ensure an optimal balance of simplicity and functionality.

---

*This document is the official README for the Crypto Prediction App GitHub repository.*
