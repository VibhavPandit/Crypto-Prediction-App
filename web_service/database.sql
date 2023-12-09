create database crypto_prediction;

use crypto_prediction;

CREATE TABLE stock_predictions(
S_no INT auto_increment PRIMARY KEY,
Symbol VARCHAR(10) NOT NULL,
CurrentPrice FLOAT,
Prediction FLOAT,
Decision VARCHAR(10),
PredictionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM stock_predictions;
