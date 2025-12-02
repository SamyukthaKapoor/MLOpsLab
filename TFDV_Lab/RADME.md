## Overview
This is a feature engineering lab that:
- Generates synthetic network metrics (30 days of data)
- Creates 32 engineered features (domain, temporal, statistical)
- Normalizes data using MinMaxScaler
- Creates sliding windows for LSTM training
- Prepares data for time series prediction models

## Features Created
- **Domain Features**: Traffic ratios, Network stress, Request efficiency, Connection health
- **Temporal Features**: Cyclic hour/day/month encoding, Business hours indicator
- **Statistical Features**: Rolling averages (30 min, 1 hour, 2 hour), Rate of change

## Files Generated
- `raw_network_metrics.csv` - Original synthetic data
- `processed_network_metrics.csv` - After feature engineering
- `train_data.csv` / `test_data.csv` - Normalized splits
- `X_train.npy`, `y_train.npy`, `X_test.npy`, `y_test.npy` - Windowed arrays for LSTM
- PNG visualizations of features and correlations

## How to Use
1. Run all cells in the Jupyter notebook in order
2. The script will generate synthetic data and engineer features
3. Output files will be saved in `network_data/` folder
4. Ready to use with TensorFlow/Keras for LSTM model training

## Requirements
- Python 3.7+
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- tensorflow (optional, for model training)

## Installation
\`\`\`bash
pip install pandas numpy matplotlib seaborn scikit-learn tensorflow
\`\`\`
