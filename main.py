import os.path
import os
from random import choice
import aiofiles as aiofiles
import uvicorn
import yaml
from fastapi import FastAPI, HTTPException
from starlette.responses import HTMLResponse, FileResponse

from models import ImageFolder, Config

app = FastAPI(docs_url="", redoc_url="")
index_html = open('index.html', 'r', encoding='utf-8').read()
config = Config(**yaml.safe_load(open('config.yaml')))


@app.get("/", response_class=HTMLResponse)
async def index():
    return index_html.replace("{images}", await get_folders_html(await get_folder_list(config.root_folder)))


@app.get("/raw/{category}")
async def get_raw_random(category: str):
    folders = await get_folder_dict(config.root_folder)
    folder: ImageFolder = folders.get(category, None)
    if not folder:
        raise HTTPException(status_code=404, detail="Not found")

    image = choice(folder.images_abs_paths)
    return FileResponse(image)


async def get_folder_list(root_path: str) -> list[ImageFolder]:
    folders = []
    for folder_name in os.listdir(root_path):
        folder = os.path.join(root_path, folder_name)
        model = ImageFolder(
            raw_url=f"/raw/{folder_name}"
        )
        images = os.listdir(folder)
        image_paths = list(map(lambda x: os.path.join(folder, x), images))

        if "properties.yaml" in images:
            properties_index = images.index("properties.yaml")
            image_paths.pop(properties_index)
            async with aiofiles.open(os.path.join(folder, "properties.yaml"), mode='r', encoding='utf-8') as f:
                content = await f.read()
                properties = yaml.load(content, yaml.Loader)
                model.display_name = properties.get("display_name", "")
                model.description = properties.get("description", "")

        model.images_abs_paths = image_paths
        folders.append(model)

    return folders


async def get_folder_dict(root_path: str) -> dict[str, ImageFolder]:
    folders = {}
    for folder_name in os.listdir(root_path):
        folder = os.path.join(root_path, folder_name)
        model = ImageFolder(
            raw_url=f"/raw/{folder_name}"
        )
        images = os.listdir(folder)
        image_paths = list(map(lambda x: os.path.join(folder, x), images))

        if "properties.yaml" in images:
            properties_index = images.index("properties.yaml")
            image_paths.pop(properties_index)
            async with aiofiles.open(os.path.join(folder, "properties.yaml"), mode='r', encoding='utf-8') as f:
                content = await f.read()
                properties = yaml.load(content, yaml.Loader)
                model.display_name = properties.get("display_name", "")
                model.description = properties.get("description", "")

        model.images_abs_paths = image_paths
        folders[folder_name] = model

    return folders


async def get_folders_html(folders: list[ImageFolder]) -> str:
    html = ""
    for folder in folders:
        html += config.folder_html.format(raw_url=folder.raw_url, display_name=folder.display_name or folder.raw_url, description=folder.description)
    return html


if __name__ == '__main__':
    uvicorn.run("main:app",
                host=config.host,
                port=config.port, reload=True)