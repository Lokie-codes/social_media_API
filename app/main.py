from random import randrange
from fastapi import FastAPI, Response, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from .data import my_posts
from .post import Post, get_post

app = FastAPI()
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='social_media',
                                user='postgres', password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection successful")
        break
    except Exception as err:
        print("Connection to database failed")
        print("Error ", err)
        time.sleep(2)


@app.get("/")
def root():
    return "Welcome to my social media API"


@app.get("/posts")      # Get all the posts
def get_posts():
    cursor.execute("""SELECT  * FROM  public.posts""")
    posts = cursor.fetchall()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No posts found")
    return {"data": posts}


@app.get("/posts/{id}")  # Get only one post
def get_data(id: int):
    cursor.execute("""SELECT * FROM public.posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    return {"data": post}


# Create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """INSERT INTO public.posts (title, content, published, rating) VALUES (%s, %s, %s, %s) RETURNING * """,
        (post.title, post.content, post.published, post.rating))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


# Delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        """DELETE FROM public.posts WHERE id = %s RETURNING * """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE public.posts SET title = %s, content = %s, published = %s, rating = %s WHERE id = %s RETURNING * """,
                   (post.title, post.content, post.published, post.rating, str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    conn.commit()
    return {"data": post}
