import os
current_dir = os.getcwd()

DataDirectory = f"data"
ImageDirectory = f"{DataDirectory}\image"
Chatlogfile = rf"{DataDirectory}\Chatlog.json"


if not os.path.exists(DataDirectory):
    os.makedirs(ImageDirectory)

if not os.path.exists(ImageDirectory):
    os.makedirs(ImageDirectory)
