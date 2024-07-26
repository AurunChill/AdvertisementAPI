from pathlib import Path

import pandas as pd

from logger import app_logger as logger
from advertisement.schemas import AdvertisementCreate
from advertisement.models import Advertisement
from advertisement.service import get_advertisements_all, create_advertisement


async def load_advertisement_fixture(file_path: Path | str):
    """
    Asynchronously loads data from a CSV file located at the given file path and creates new advertisements if they do not already exist.

    Args:
        file_path (Path | str): The path to the CSV file containing the data to be loaded.

    Returns:
        None
    """
    logger.debug(f"Loading data from {file_path}")
    df = pd.read_csv(file_path)
    all_advertisements = await get_advertisements_all()
    all_adv_hashes = {hash(adv) for adv in all_advertisements}
    
    for _, row in df.iterrows():
        data = {
            'id': row['id'],
            'title': row['title'],
            'author': row['author'],
            'views_count': row['views_count'],
            'position': row['position']
        }
        advertisement = Advertisement(**data)
        if hash(advertisement) not in all_adv_hashes:
            await create_advertisement(AdvertisementCreate(**data))
        
        