import nltk
nltk.download('stopwords')
from Questgen import main

#########################################
#   @author: Pradeep CH                 #
#   @version: 1.0                       #
#                                       #
#########################################

# Sample 1
qe= main.BoolQGen()
payload = {
            "input_text": "Sachin Ramesh Tendulkar is a former international cricketer from India and a former captain of the Indian national team. He is widely regarded as one of the greatest batsmen in the history of cricket. He is the highest run scorer of all time in International cricket."
        }
output = qe.predict_boolq(payload)

# sample 2
qg = main.QGen()
output = qg.predict_mcq(payload)

# sample 3
output = qg.predict_shortq(payload)

#sample 4
payload2 = {
    "input_text" : "What is Sachin Tendulkar profession?",
    "max_questions": 5
}
output = qg.paraphrase(payload2)

#sample 5
answer = main.AnswerPredictor()
payload3 = {
    "input_text" : '''Sachin Ramesh Tendulkar is a former international cricketer from 
              India and a former captain of the Indian national team. He is widely regarded 
              as one of the greatest batsmen in the history of cricket. He is the highest
               run scorer of all time in International cricket.''',
    "input_question" : "Who is Sachin tendulkar ? "
    
}
output = answer.predict_answer(payload3)
