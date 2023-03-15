import supervisely as sly

from supervisely.app.widgets import Container

import src.globals as g
import src.ui.input as input
import src.ui.rotator as rotator
import src.ui.output as output

images_container = Container(
    widgets=[rotator.table_card, rotator.preview_card],
    direction="horizontal",
    fractions=[1, 1],
)

layout = Container(
    widgets=[input.card, images_container, output.card], direction="vertical"
)

app = sly.Application(layout=layout, static_dir=g.STATIC_DIR)
