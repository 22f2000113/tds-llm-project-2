from FileUtil import read_file
from codes.w4 import w4q1, w4q2, w4q3, w4q4, w4q5, w4q6,w4q7, w4q8, w4q9, w4q10

def W4Q1(question):   
    return {"answer": w4q1.get_command(question)}

def W4Q2(question):
    return {"answer": w4q2.get_movies(question)}

def W4Q3(question):
    return {"answer": w4q3.get_command(question)}

def W4Q4(question):
    return w4q4.get_command(question)

def W4Q5(question):
    return w4q5.get_command(question)

def W4Q6(question):
    return w4q6.get_command(question)

def W4Q7(question):
   return w4q7.get_command(question)

def W4Q8(question):
    return w4q8.get_command(question)

def W4Q9(question):
    return w4q9.get_marks(question)

def W4Q10(question):
    return w4q10.get_command(question)
