import pandas as pd

# Directory where Parquet files are stored
parquet_path = 'data/output'

# Read Parquet files into pandas DataFrame
df = pd.read_parquet(parquet_path, engine='auto')  # Use 'pyarrow' or 'fastparquet'

# Display DataFrame
print("DataFrame from Parquet files:")
print(df)
