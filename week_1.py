from FileUtil import read_file
from codes.w1 import w1q2,w1q3,w1q4,w1q5,w1q7,w1q8,w1q9,w1q10,w1q12,w1q13,w1q14,w1q16,w1q17,w1q18

def W1Q1(question):   
    return {"answer": read_file("./output/w1/ans1.txt")}

def W1Q2(question):
    return {"answer": w1q2.get_command(question)}

def W1Q3(question):
    return {"answer": w1q3.get_sha_code(question)}

def W1Q4(question):
    return w1q4.calculate_sum(question)

def W1Q5(question):
   return  w1q5.calculate_sum(question)

def W1Q6(question):
   return {"answer": "Not Done"}

def W1Q7(question):
   return {"answer": w1q7.get_date_count(question)}

def W1Q8(question):
    return {"answer": w1q8.get_number_from_csv(question,"./inputs/W1Q8")}

def W1Q9(question):
   return {"answer": w1q9.sorted_json(question)}

def W1Q10(question):
   return {"answer":  w1q10.get_hash(question)}

def W1Q11(question):
   return {"answer":"Not Done"}

def W1Q12(question):
   return {"answer": w1q12.sum_of_symbols(question)}

def W1Q13(question):
   return {"answer": w1q13.create_email_repo(question)}

def W1Q14(question):
   return {"answer": w1q14.get_file_hash(question)}

def W1Q16(question):
   return {"answer": w1q16.get_file_move_and_hash(question)}

def W1Q17(question):
   return {"answer": w1q17.compare_files(question)}

def W1Q18(question):
   return {"answer": "SELECT SUM(units * price) AS total_sales FROM tickets WHERE TRIM(UPPER(type)) = 'GOLD';"}