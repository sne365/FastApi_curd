
from random import randrange
from typing import Union,Optional

from fastapi import FastAPI, Response,status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    publish: bool=True
    rating:Optional[int] = 4
 

my_posts =[{"title":"title of post 1", "content":"content of post 1","id":1},{"title":"favorite foods","content":"I like pizza", "id":2}]   

def find_postByid(id):
    for p in my_posts:
        if p["id"]==id:
            return p

def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p["id"]==id:
            return i

@app.get("/")
def read_root():
    return {"Hello": "Welcome"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/create", status_code=status.HTTP_201_CREATED)
def create_post(new_post:Post):
    post_dict = new_post.dict()
    post_dict['id']= randrange(0,10000000)
    my_posts.append(post_dict)
    return post_dict
  # print(new_post) 
   #return {"new post": f"title:{new_post.title} , content:{new_post.content}, publish:{new_post.publish}, rating:{new_post.rating}"}


@app.get("/posts/{id}")
def get_post(id:int):
    post= find_postByid(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return{"post_details":post}

@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    index= find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    post_dict =post.dict()
    print("yes")
    post_dict['id']=id
    my_posts[index]= post_dict
    return {"data": post_dict}

@app.delete("/posts/{id}")
def delete_post(id:int):
    index= find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)




