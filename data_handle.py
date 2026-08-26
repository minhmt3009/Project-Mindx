import pandas as pd
df = pd.read_csv(r'D:\Data Science\Project cuối khóa 1 Mindx\spotify_data_processed.csv')

# Thêm bài hát mới => tự generate track id
def new_track():
    if df.empty:
        return 'TRK-00001'

    numeric_parts = df["track_id"].str.replace("TRK-", "", regex=False).astype(int)
    next_number = numeric_parts.max() + 1
    
    return f"TRK-{next_number:05d}" 
