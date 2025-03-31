
from FileUtil import read_file,current_dir
from codes.w2 import w2q3,w2q5,w2q6,w2q7

def W2Q1(question):
    file_path = current_dir+"/output/w2/ans_w2_q1.txt"
    return {"answer": read_file(file_path)}

def W2Q3(question):
    return {"answer":w2q3.create_email_repo()}

def W2Q5(question):
    return {"answer":w2q5.number_of_pixels()}


def W2Q6(question):
    return {"answer":w2q6.get_verl_url()}

def W2Q7(question):
    return {"answer":w2q7.create_email_action()}

def W2Q8(question):
    return {"answer":"https://hub.docker.com/repository/docker/22f2000113/python-flask-app/general"}

def W2Q9(question):
    return {"answer":"http://127.0.0.1:8000/api"}


