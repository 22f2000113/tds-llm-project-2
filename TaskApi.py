# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "fastapi",
#     "requests",
#     "uvicorn",
#     "duckdb",
#     "numpy",
#     "sentence-transformers",
#     "pandas",
#     "python-multipart",
#     "google-auth",
#     "google-auth-oauthlib",
#     "beautifulsoup4",
#     "lxml",
#     "tabula-py",
#
# ]
# ///

from fastapi import FastAPI,  HTTPException, File, UploadFile, Form,Query
import uvicorn
from typing import List
import os
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from io import BytesIO
from FileUtil import extract_zip_file, write_file
from QuestionDb import  init_db
from QuestionDb import search_similar
from codes.w2 import w2q9
from codes.w3 import w3q7,w3q8
from models import SimilarityRequest
from week_2 import *
from week_1 import *
from week_3 import *
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=['GET', 'POST'],
    allow_headers=["*"],  # Allow any headers
)

conn, model = init_db()


@app.get("/home")
def home():
    return {"message": "Welcome to Task API"}

@app.post("/api",response_class=JSONResponse)
async def run_tasks(question: str = Form(...), file: Optional[UploadFile] = File(None)):
    try:

        api_que = search_similar(conn=conn,model=model,query=question)
        print(f"question is matching with {api_que}")

        if file:
            file_path = current_dir+os.path.join("/inputs", api_que)
            print(f"file path {file_path}")
            os.makedirs(file_path, exist_ok=True)
            file_content = await file.read()
            if file.content_type == 'application/zip':
                zip_file = BytesIO(file_content)
                extract_zip_file(file_path, zip_file)
            else:
                print(f"before writing to file {file.filename} {file.content_type} {file_path}")
                file_path =file_path+f"/{file.filename}"
                write_file(file_path,content=file_content, content_type=file.content_type)
                print("file created successfully")
        selected_method = eval(api_que)
        output = selected_method(question)
        return JSONResponse(content=output, status_code=200)
        #return {"answer",output}
       
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api")
async def get_classes(class_: Optional[List[str]] =  Query(None, alias="class")):
   return w2q9.get_json(class_)


@app.post("/similarity")
async def compute_similarity(request: SimilarityRequest):
    return w3q7.get_similarity(request)

@app.get("/execute")
async def execute(q: str):
    try:
        result = w3q8.analyze_query(q)
        return result
    except HTTPException as e:
        raise e

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
