# %% [markdown]
# ## Libraries and Dependencies

# %%
import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3

# %% [markdown]
# ## Code

# %% [markdown]
# Constants

# %%
DATABASE_LOCATION = 'sqlite::///my_played_tracks.sqlite'
USER_ID = 'Yorudan'
TOKEN = 'BQD2O9PIp--do7loSI1b33ZchaiwJt2CW4wxvTCEqHziyhnPokNb34NoAu_1rNvJRtSpg6_sY_00tZcbzCxsBOqsAJ252kxEwawuxggWgM2bz5bqjPApsTnQ3_46k7cmLJ1-KzufzsCrV_jOMhWfKYYsQE6yQE3mKfodSJbAJYB6cDRzauH3rFShHpvhFCCseKB0dw'

# %% [markdown]
# Validation

# %%
def check_if_valid_data(df: pd.DataFrame) -> bool:
    # check if df is empty
    if df.empty:
        print('No songs downloaded. Finishing execution')
        return False
    
    # primary key check
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception('Primary key check violated')

    # check for nulls
    if df.isnull().values.any():
        raise Exception('Null value found')

    # check that all timestamps are yesterday's date
    # yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
    # yesterday = yesterday.replace(hour = 0, minute = 0, second = 0, microsecond = 0)

    # timestamps = df['timestamp'].tolist()
    # for timestamp in timestamps:
    #     if datetime.datetime.strptime(timestamp, '%Y-%m-%d') >= yesterday:
    #         raise Exception('At least one of the returned songs does not come from within 24hrs')

    return True

# %% [markdown]
# Main

# %%
if __name__ == '__main__':
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {token}'.format(token = TOKEN)
    }

    # convert time to unix timestamp in ms
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days = 1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # download all songs i've listened in the last 24hrs
    r = requests.get('https://api.spotify.com/v1/me/player/recently-played?after={time}'.format(time=yesterday_unix_timestamp), headers = headers)
    data = r.json()
    
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    # extract only the relevant data from json obj
    for song in data['items']:
        song_names.append(song['track']['name'])
        artist_names.append(song['track']['album']['artists'][0]['name'])
        played_at_list.append(song['played_at'])
        timestamps.append(song['played_at'][0:10])

    # prepare a dictionary in order to turn it into a pd df
    song_dict = {
        'song_name': song_names,
        'artist_name': artist_names,
        'played_at': played_at_list,
        'timestamp': timestamps
    }

    song_df = pd.DataFrame(song_dict, columns = ['song_name', 'artist_name', 'played_at', 'timestamp'])
    display(song_df)

    # validate
    if check_if_valid_data(song_df):
        print('Data valid, proceed to load stage')


