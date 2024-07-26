from sqladmin import ModelView

from .models import Advertisement


class AdvertisementAdmin(ModelView, model=Advertisement):
    name = "Advertisement"
    name_plural = "Advertisements"
    column_list = [
        "id",
        "title",
        "author",
        "views_count",
        "position"
    ]

    column_labels = {
        "id": "ID",
        "title": "Title",
        "author": "Author",
        "views_count": "Views Count",
        "position": "Position"
    }
