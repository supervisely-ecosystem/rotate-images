<div align="center" markdown>
<img src="https://is5-ssl.mzstatic.com/image/thumb/Purple116/v4/20/fd/36/20fd3616-baef-1114-73fc-bbc3c83e2f06/AppIcon-0-0-1x_U007emarketing-0-0-0-7-0-0-sRGB-0-0-0-GLES2_U002c0-512MB-85-220-0-0.png/1200x600wa.png"/>

# Rotate images with annotations

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#Preparation">Preparation</a> •
  <a href="#How-To-Run">How To Run</a>
</p>

placeholder for ecosystem badge
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
placeholder for release badge
placeholder for views badge
placeholder for runs badge

</div>

## Overview
This app allows you to rotate images along with annotations. After selecting a dataset to work with, the app will generate a table with all images in the dataset. You can open an image in the preview window and rotate it left or right and even on a custom angle with the slider. After rotating the image, you can save replace the original image with the rotated one or save it as a new image. The app will also rotate all annotations on the image.

## Preparation
The app requires a dataset of images to work with, so before running the app, you need to create a dataset and upload images to it. Besides this you don't need any additional preparations, the app is ready to run.

## How To Run

If you don't run the app from the dataset, first of all you need to specify the dataset to work with. You need to select a dataset in the `Input dataset` section. After selecting the dataset, click the button `Load data` under the dataset selector. The app will load the dataset and generate a table with all images in the dataset.<br>
Note: when the data from the dataset will be loaded, the dataset selector will be locked until you click the `Change` dataset button.<br>
Now you can follow these steps to rotate images:<br>
<br>
**Step 1:** The image names in the table are clickable, which may help you to find the image you need. When you find the image you need, click on the `SELECT` button in the rightmost column. The image will be opened in the preview window.<br><br>
**Step 2:** Now you can click `Rotate left` and `Rotate right` buttons to rotate the image by 90 degrees.<br><br>

PLACEHOLDER FOR SCREENSHOT WITH TABLE, IMAGE PREVIEW AND ROTATE BUTTONS (custom angle checkbox is unchecked)<br><br>

**Step 3:** If you need to rotate the image on a custom angle, you can use the slider, which is hidden by default. To show the slider, check the `Rotate the `image with `the precise` angle` checkbox. The rotate buttons will be hidden and the slider will be shown instead.<br><br>

**Step 4:** You can select the angle by dragging the slider or by typing the angle in the input field. The range of allowed angles is from -180 to 180 degrees. After selecting the angle, click the `Apply` button under the slider. The image will be rotated on the selected angle.<br><br>

PLACEHOLDER FOR SCREENSHOT WITH TABLE, IMAGE PREVIEW AND SLIDER (custom angle checkbox is checked)<br><br>

**Step 5:** You can reset the current image rotation by clicking the `Reset` button under the slider. The image will be rotated back to the original state.<br><br>

**Step 6:** When you finish rotating the image, you can save the result. Follow the `Save` method` section and choose one of two options: replace the original image with the rotated one or save the rotated image as a new image.<br><br>

PLACEHOLDER FOR SCREENSHOT WHERE SUCCESS RESULT MESSAGE APPEARED<br><br>

**Step 7:** After selecting the save method, click the `Save image` button. The app will save the image to the _same dataset_ and will show the success message, which also contains the link to the image in the dataset. Note: if you didn't make any changes to the image, the app will show the error message and won't save the image.<br><br>

**Note:** the app will write information about the rotation angle, date and time of applying the rotation to the image metadata. You can find this information in the `Image properties - Info` section of the image in the labeling tool.<br>