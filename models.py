from pydantic import BaseModel


class PageOptions(BaseModel):
    PageName: str = "Александр Мокин"
    PageOption: str = "content"
