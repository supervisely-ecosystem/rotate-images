import supervisely as sly

from supervisely.app.widgets import Container

import src.globals as g
import src.ui.input as input
import src.ui.image_selector as image_selector
import src.ui.image_preview as image_preview
import src.ui.output as output

images_container = Container(
    widgets=[image_selector.card, image_preview.card],
    direction="horizontal",
    fractions=[1, 1],
)

layout = Container(
    widgets=[input.card, images_container, output.card], direction="vertical"
)

app = sly.Application(layout=layout, static_dir=g.STATIC_DIR)
image_selector.build_table()
