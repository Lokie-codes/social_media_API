from typing import Union
from pydantic import BaseModel
from .data import my_posts


class Post(BaseModel):
    title: str
    content: str
    rating: Union[float, None] = None
    published: bool = True


def get_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i