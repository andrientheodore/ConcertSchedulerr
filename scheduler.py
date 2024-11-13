import pandas as pd

# 1. Read the files
schedule_df = pd.read_csv('schedule.csv')
favorite_df = pd.read_csv('favorite.csv')

# 2. Join the data based on artist_name
merged_df = schedule_df.merge(favorite_df, on='artist_name')

# 3. Round down start_date and end_date
merged_df['start_date'] = pd.to_datetime(merged_df['start_date'])
merged_df['end_date'] = pd.to_datetime(merged_df['end_date'])

merged_df['start_date'] = merged_df['start_date'].dt.floor('H')
merged_df['end_date'] = merged_df['end_date'].dt.floor('H')

# 4. Create a duration column
merged_df['duration'] = (merged_df['end_date'] - merged_df['start_date']).dt.total_seconds() / 3600

# 5. Find min start time, end time, and distribute duration
min_start_time = merged_df['start_date'].min()
max_end_time = merged_df['end_date'].max()
total_duration = (max_end_time - min_start_time).total_seconds() / 3600

# Distribute duration evenly
merged_df['new_duration'] = total_duration / len(merged_df)

# Calculate new end_date based on new_duration
merged_df['new_end_date'] = merged_df['start_date'] + pd.to_timedelta(merged_df['new_duration'], unit='H')

# 6. Format start_date and new_end_date
merged_df['start_date'] = merged_df['start_date'].dt.strftime('%m/%d/%y %I.%M %p')
merged_df['new_end_date'] = merged_df['new_end_date'].dt.strftime('%m/%d/%y %I.%M %p')

# 7. Output the final dataframe
print(merged_df[['artist_name', 'start_date', 'new_end_date']])
