
from random import randrange
from typing import Union,Optional

from fastapi import FastAPI, Response,status,Depends,HTTPException
from fastapi.params import Body

import psycopg2
from psycopg2.extras import RealDictCursor
from . import models,schemas
from .database import engine,get_db_connection
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()



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


@app.get("/sqlalchemy")
def test(db:Session=Depends(get_db_connection)):
    posts = db.query(models.Post).all()
    return {"Hello": posts}


@app.get("/posts")
def get_posts(db:Session=Depends(get_db_connection)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts =cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/create", status_code=status.HTTP_201_CREATED)
def create_post(new_post:schemas.Post,db:Session=Depends(get_db_connection)):
    # cursor.execute(f"INSERT INTO posts (title,content, publish) where VALUES({new_post.title},{new_post.content},{new_post.publish})")
    # cursor.execute("""INSERT INTO posts (title,content, publish) VALUES(%s,%s,%s) RETURNING * """,(new_post.title,new_post.content,new_post.publish))
    # post= cursor.fetchone()
    # conn.commit()
    post= models.Post(**new_post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"data":post}

@app.get("/posts/{id}")
def get_post(id:int,db:Session=Depends(get_db_connection)):
    # cursor.execute("""SELECT * FROM posts WHERE id=%s""", (id,))
    # post= cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return{"post_details":post}

@app.put("/posts/{id}")
def update_post(id:int, updated_post:schemas.Post,db:Session=Depends(get_db_connection)):
    # cursor.execute("""UPDATE posts SET title=%s,content=%s WHERE ID=%s RETURNING *""", (post.title, post.content,id,))
    # post=cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit() 
    return {"data": post_query.first()}

@app.delete("/posts/{id}")
def delete_post(id:int,db:Session=Depends(get_db_connection)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s returning *""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id==id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)




