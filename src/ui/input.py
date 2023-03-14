from supervisely.app.widgets import DatasetThumbnail, Card

import src.globals as g


dataset = DatasetThumbnail(g.PROJECT_INFO, g.DATASET_INFO)

card = Card(
    "1️⃣ Input dataset",
    "Images from the selected dataset will be loaded.",
    content=dataset,
)
