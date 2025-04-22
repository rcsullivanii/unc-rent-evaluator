# UNC Rent Evaluator

## Data Cleaning Process

The cleaned data (zillow_cleaned.parquet) is a consolidated DataFrame that contains only Zillow listings meeting the following criteria...

Columns retained: Only the features listed in COLUMNS_TO_KEEP (e.g., zpid, zestimate, rent_zestimate, latitude, longitude, bedrooms, bathrooms, etc.).

Data cleaning: It drops any rows missing values for critical features ('rent_zestimate', 'latitude', or 'longitude').

Geographic filtering: It calculates the distance from each listing to a reference point (the Old Well) and then filters out any listings farther than 5 miles.

It’s stored in a Parquet file because Parquet is a columnar format that provides efficient storage, good compression, and fast querying—advantages that are especially useful when handling large datasets.
