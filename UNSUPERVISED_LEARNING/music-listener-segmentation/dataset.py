import pandas as pd

df = pd.read_excel('/content/music_listeners.xlsx')

display(df.head())

required_columns = ['listening_hours_per_week', 'songs_per_day', 'skip_rate', 'playlist_count']

if all(col in df.columns for col in required_columns):
    print('All required columns are present in the DataFrame.')
else:
    missing_columns = [col for col in required_columns if col not in df.columns]
    print(f'The following required columns are missing: {missing_columns}')
    print('Current columns:', df.columns.tolist())