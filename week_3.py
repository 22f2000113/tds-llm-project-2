from FileUtil import read_file,current_dir
from codes.w3 import w3q1, w3q2,w3q3,w3q4,w3q5

def W3Q1(question):
    return {"answer": w3q1.get_payload_request(question)}

def W3Q2(question):
    return {"answer": w3q2.get_tokens(question)}

def W3Q3(question):
    return {"answer":w3q3.get_payload(question)}

def W3Q4(question):
    return {"answer":w3q4.get_image_hash(question)}

def W3Q5(question):
    return {"answer":w3q5.get_json_body(question)}

def W3Q6(question):
    file_path = current_dir + "/output/w3/w3_ans6.txt"
    return {"answer":read_file(file_path)}

def W3Q7(question):
    return {"answer":"http://35.226.189.115:3000/similarity"}

def W3Q8(question):
    return {"answer":" http://35.226.189.115:8000/execute"}

