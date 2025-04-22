# UNC Rent Evaluator

## Data Cleaning Process

The cleaned data (zillow_cleaned.parquet) is a consolidated DataFrame that contains only Zillow listings meeting the following criteria...

Columns retained: Only the features listed in COLUMNS_TO_KEEP (e.g., zpid, zestimate, rent_zestimate, latitude, longitude, bedrooms, bathrooms, etc.).

Data cleaning: It drops any rows missing values for critical features ('rent_zestimate', 'latitude', or 'longitude').

Geographic filtering: It calculates the distance from each listing to a reference point (the Old Well) and then filters out any listings farther than 5 miles.

It’s stored in a Parquet file because Parquet is a columnar format that provides efficient storage, good compression, and fast querying—advantages that are especially useful when handling large datasets.

## Random Forest 

We trained a Random Forest Regressor to predict monthly rents (rentZestimate) for properties near UNC Chapel Hill using Zillow data. After filtering out extreme rent outliers (> $5000), we used features such as:

Bedrooms, bathrooms, living area

Distance to campus (miles_to_old_well)

Home type and listing status (one-hot encoded)

📊 Model Performance (on test set):

R² Score: 0.9294

RMSE: $238.51
