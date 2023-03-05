from random import randrange
from fastapi import FastAPI, Response, status, HTTPException

from data import my_posts
from post import Post, get_post

app = FastAPI()


@app.get("/")
def root():
    return "Welcome to my social media API"


@app.get("/posts")      # Get all the posts
def get_posts():
    posts = my_posts
    return {"data": posts}


@app.get("/posts/{id}")  # Get only one post
def get_data(id: int):
    post = get_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    return {"data": post}


# Create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


# Delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = get_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    prev_post = get_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    post_dict = post.dict()
    post_dict['id'] = id
    index = my_posts.index(prev_post)
    my_posts[index] = post_dict
    return Response()
