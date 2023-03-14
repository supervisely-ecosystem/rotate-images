import os

import pandas as pd
import supervisely as sly

from supervisely.app.widgets import Card, Table

import src.globals as g
import src.ui.image_preview as image_preview

current_image = None
current_image_local_path = None

COL_ID = "image id".upper()
COL_IMAGE = "image".upper()
COL_SIZE = "size (bytes)".upper()
COL_WIDTH = "width (pixels)".upper()
COL_HEIGHT = "height (pixels)".upper()
COL_LABELS = "labels (count)".upper()
SELECT_IMAGE = "select".upper()

columns = [COL_ID, COL_IMAGE, COL_SIZE, COL_WIDTH, COL_HEIGHT, COL_LABELS, SELECT_IMAGE]

rows = []
table = Table(fixed_cols=1, width="100%")

card = Card(
    "2️⃣ Select image",
    "Choose the image to rotate.",
    content=table,
)


def build_table():
    global table, rows
    table.loading = True
    images = g.api.image.get_list(g.DATASET_ID)
    for image in images:
        rows.append(
            [
                image.id,
                image.name,
                image.size,
                image.width,
                image.height,
                image.labels_count,
                sly.app.widgets.Table.create_button(SELECT_IMAGE),
            ]
        )

    df = pd.DataFrame(rows, columns=columns)
    table.read_pandas(df)
    table.loading = False


@table.click
def handle_table_button(datapoint: sly.app.widgets.Table.ClickedDataPoint):
    global current_image
    if datapoint.button_name is None:
        return
    image_id = datapoint.row[COL_ID]
    current_image = g.api.image.get_info_by_id(image_id)
    if datapoint.button_name == SELECT_IMAGE:
        global current_image_local_path
        current_image_local_path = os.path.join(g.STATIC_DIR, current_image.name)
        g.api.image.download(image_id, current_image_local_path)
        image_preview.labeled_image.set(
            title=current_image.name,
            image_url=os.path.join("static", current_image.name),
        )
        image_preview.card.unlock()
        image_preview.rotator.set_value(0)
