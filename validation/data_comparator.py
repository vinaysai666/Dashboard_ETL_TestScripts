import pandas as pd

def compare_data(source_df, destination_df):
    """Compare data between source and destination tables."""
    source_df.reset_index(drop=True, inplace=True)
    destination_df.reset_index(drop=True, inplace=True)

    # Ensure uniformity in data
    source_df = source_df.astype(str)
    destination_df = destination_df.astype(str)

    # Perform data comparison
    differences = source_df.compare(destination_df)
    return differences
