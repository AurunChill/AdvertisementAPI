import pandas as pd

from db import async_session_maker
from advertisement.models import Advertisement

async def load_data_from_csv(file_path):
    df = pd.read_csv(file_path)
    async with async_session_maker() as session:
        for index, row in df.iterrows():
            existing_advertisement = session.query(Advertisement).filter_by(
                title=row['title'],
                author=row['author']
            ).first()
            if not existing_advertisement:
                new_advertisement = Advertisement(
                    id=row['id'],
                    title=row['title'],
                    author=row['author'],
                    views_count=row['views_count'],
                    position=row['position']
                )
                session.add(new_advertisement)
        session.commit()
        print(f"{len(df)} records processed. New entries added to the database.")
