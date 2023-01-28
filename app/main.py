
from random import randrange
from typing import Union,Optional

from fastapi import FastAPI, Response,status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    publish: bool=True
    # rating:Optional[int] = 4

try:
    conn = psycopg2.connect(host="localhost",database="Fastapi",user="postgres",password="postgres", cursor_factory=RealDictCursor)    
    cursor = conn.cursor()
    print("Database is connected successfully")
except Exception as error:
    print("Connection error",error)
 

# my_posts =[{"title":"title of post 1", "content":"content of post 1","id":1},{"title":"favorite foods","content":"I like pizza", "id":2}]   


@app.get("/")
def read_root():
    return {"Hello": "Welcome"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts =cursor.fetchall()
    # print(posts)
    return {"data": posts}

@app.post("/create", status_code=status.HTTP_201_CREATED)
def create_post(new_post:Post):
    # cursor.execute(f"INSERT INTO posts (title,content, publish) where VALUES({new_post.title},{new_post.content},{new_post.publish})")
    cursor.execute("""INSERT INTO posts (title,content, publish) VALUES(%s,%s,%s) RETURNING * """,(new_post.title,new_post.content,new_post.publish))
    post= cursor.fetchone()
    conn.commit()
    return {"data":post}


@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute("""SELECT * FROM posts WHERE id=%s""", (id,))
    post= cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return{"post_details":post}

@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    cursor.execute("""UPDATE posts SET title=%s,content=%s WHERE ID=%s RETURNING *""", (post.title, post.content,id,))
    post=cursor.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    return {"data": post}

@app.delete("/posts/{id}")
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id=%s returning *""", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)




