import os

import pandas as pd
import supervisely as sly

from supervisely.app.widgets import Card, Table

import src.globals as g
import src.ui.image_preview as image_preview
import src.ui.output as output

current_image = None
current_image_name = None
current_image_annotation = None
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
    lock_message="Select a dataset on the step 1️⃣.",
)
# card.lock()


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
    global current_image_id
    current_image_id = datapoint.row[COL_ID]
    current_image = g.api.image.get_info_by_id(current_image_id)
    if datapoint.button_name == SELECT_IMAGE:
        global current_image_local_path
        current_image_local_path = os.path.join(g.STATIC_DIR, current_image.name)
        g.api.image.download(current_image_id, current_image_local_path)

        meta_json = g.api.project.get_meta(g.PROJECT_ID)
        project_meta = sly.ProjectMeta.from_json(data=meta_json)

        ann_info = g.api.annotation.download(current_image_id)
        ann_json = ann_info.annotation

        global current_image_annotation
        current_image_annotation = sly.Annotation.from_json(ann_json, project_meta)

        global current_image_name
        current_image_name = current_image.name

        image_preview.labeled_image.set(
            title=current_image_name,
            image_url=os.path.join("static", current_image.name),
            ann=current_image_annotation,
        )

        image_preview.card.unlock()
        image_preview.rotator.set_value(0)

        output.card.unlock()
