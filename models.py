from pydantic import BaseModel


class ImageFolder(BaseModel):
    display_name: str = ""
    description: str = ""

    raw_url: str = ""
    images_abs_paths: list[str] = []


class Config(BaseModel):
    root_folder: str
    folder_html: str
    host: str
    port: int