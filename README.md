<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/115161827/225969759-5699c73c-fbac-4eb3-aa10-c66f9e375ca5.jpg"/>

# Rotate images with annotations

**Warning! This app does not support working with Cuboids!**

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/rotate-images)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/rotate-images)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/rotate-images)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/rotate-images)](https://supervise.ly)

</div>

## Overview
This app allows you to rotate images along with annotations. After selecting a dataset to work with, the app will generate a table with all images in the dataset. You can open an image in the preview window and rotate it left or right and even on a custom angle with the slider. After rotating the image, you can save replace the original image with the rotated one or save it as a new image. The app will also rotate all annotations on the image.

## How To Run

If you don't run the app from the context menu of a dataset, first of all you need to specify the dataset to work with. You need to select a dataset in the `Input dataset` section. After selecting the dataset, click the button `Load data` under the dataset selector. The app will load the dataset and generate a table with all images in the dataset.<br>
Note: when the data from the dataset will be loaded, the dataset selector will be locked until you click the `Change dataset` button.<br>
Now you can follow these steps to rotate images:<br>
<br>
**Step 1:** The image names in the table are clickable, which may help you to find the image you need to work with. When you find the needed image, click on the `SELECT` button in the rightmost column. The image will be opened in the preview window.<br><br>
**Step 2:** Now you can click `Rotate left` and `Rotate right` buttons to rotate the image by 90 degrees.

<img src="https://user-images.githubusercontent.com/115161827/225948144-395cab9c-9317-4721-8b09-bd859732f6c0.png"/> <br><br>

**Step 3:** If you need to rotate the image on a custom angle, you can use the slider, which is hidden by default. To show the slider, check the `Rotate the image with a precise angle` checkbox. The rotate buttons will be hidden and the slider will be shown instead.<br><br>

**Step 4:** You can select the angle by dragging the slider or by typing the angle in the input field. The range of allowed angles is from -180 to 180 degrees. After selecting the angle, click the `Apply` button under the slider. The image will be rotated on the selected angle.<br><br>

<img src="https://user-images.githubusercontent.com/115161827/225950116-57dc36db-0054-4106-8d6b-99000fb2ff5f.png"/> <br><br>

**Step 5:** You can reset the current image rotation by clicking the `Reset` button under the slider. The image will be rotated back to the original state.<br><br>

**Step 6:** When you finish rotating the image, you can save the result. Follow the `Save method` section and choose one of two options: replace the original image with the rotated one or save the rotated image as a new file.<br><br>

<img src="https://user-images.githubusercontent.com/115161827/225951045-440f86f7-b058-4172-be5d-eea94a2b6172.png"/> <br><br>

**Step 7:** After selecting the save method, click the `Save image` button. The app will save the image to the _same dataset_ and will show the success message, which also contains the link to the image in the dataset. Note: if you didn't make any changes to the image, the app will show the error message and won't save the image.<br><br>

**Step 8:** After finishing using the app, don't forget to stop the app session manually in the Workspace tasks.

**Note:** the app will write information about the rotation angle, date and time of applying the rotation to the image metadata. You can find this information in the `Image properties - Info` section of the image in the labeling tool.<br>
