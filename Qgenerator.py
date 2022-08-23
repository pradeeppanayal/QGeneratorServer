from urllib import response
import nltk
nltk.download('stopwords')
from Questgen import main
import logging
import random

#########################################
#   @author: Pradeep CH                 #
#   @version: 1.0                       #
#                                       #
#########################################
# This is an abstract class which has two functions defined 
# Implemented subclass has to define 'predict'
class Questiongenerator(object):
    def __init__(self) :        
        self.qg = main.QGen()
        self.answer = main.AnswerPredictor()
        self.qe= main.BoolQGen()

    def generate(self,payload:map):
        self.validate(payload)
        return self.predict(payload)

    def predict(self, payaload):
        raise NotImplemented()

    def validate(self, payload):
        if not payload:
            raise Exception("Payload cannot be null or empty")
        if 'input_text' not in payload:
            raise Exception("input_text not found in payload")
    def asText(self, response:map) -> str:
        raise Exception("Not implmented")

class MCQQuestionGenerator(Questiongenerator):
    def predict(self,payload:map): 
        response = self.qg.predict_mcq(payload)
        # code to add the answer as an option
        if response and 'questions' in response:
            for question in response['questions']:
                ansIndex = random.randint(0,len(question['options']));
                question['options'].insert(ansIndex,question['answer']);
        return response
    def asText(self, response) ->str:
        if not response or not 'questions' in response:
            return 'No data'
        text = ""
        c = 1
        for question in response['questions']:
            text += f"\n{c}: {question['question_statement']}"
            text +="\nOptions:"      

            for option in question['options']:
                text +=f'\n{option}' 
            if question['extra_options']:
                text +="\nAdditional Options:"
                for option in question['extra_options']:
                    text +=f'\n{option}' 
            text +=f"\nAnswer: { question['answer']}"
            text +="\n"
            c +=1
        return text

class YesOrNoQuestionGenerator(Questiongenerator):
    def predict(self,payload:map):
        return self.qe.predict_boolq(payload)

    def asText(self, response) ->str:
        if not response or 'Boolean Questions' not in response:
            return 'No data'
        text = "Questions:"
        c = 1
        for question in response['Boolean Questions']:
            text +=f"\n{c}:{question}"
            c +=1
        return text

class ShortQuestionGenerator(Questiongenerator):
    def predict(self,payload:map):        
        return self.qg.predict_shortq(payload)

    def asText(self, response) ->str:
        if not response or 'questions' not in response:
            return 'No data'
        text = "Questions:"
        c = 1
        for entry in response['questions']:
            text +=f"\n{c}: {entry['Question']}"
            text +=f"\nAns: {entry['Answer']}"
            text +=f"\nTip: {entry['context']}"
            c +=1
        return text

class ParaphraseGenerator(Questiongenerator):
    def predict(self,payload:map):
        return self.qg.paraphrase(payload)

    def asText(self, response) ->str:
        if not response or 'Paraphrased Questions' not in response:
            return 'No data'
        text = "Paraphrased Questions:"
        c = 1
        for question in response['Paraphrased Questions']:
            text +=f"\n{c}:{question}"
            c +=1
        return text

class AnswerGenerator(Questiongenerator):
    def predict(self,payload:map):
        return self.answer.predict_answer(payload) 

    def validate(self, payload):
        super().validate(payload)
        if 'input_question' not  in payload:
            raise Exception('input_question not payload in payload')
      
    def asText(self, response) ->str:
        if not response:
            return 'No data'
        return f"Answer :{response}"

class QuestionGeneratorBuilder(object):
    YES_OR_NO = 'YesOrNo'
    MCQ = 'mcq'
    SHORT = 'short'
    PARAPHRASE = 'paraphrase'
    ANSWER = 'answer'

    GENERATOR_MAPPER = {
        YES_OR_NO : YesOrNoQuestionGenerator(),
        MCQ : MCQQuestionGenerator(),
        SHORT :ShortQuestionGenerator(),
        PARAPHRASE: ParaphraseGenerator(),
        ANSWER: AnswerGenerator()
    }
    @staticmethod
    def getGenerator(mode:str) ->Questiongenerator:
        logging.debug(f"Getting generator with mode {mode}")
        if not mode:
            raise Exception('Mode should be specified') 
        if mode not in QuestionGeneratorBuilder.GENERATOR_MAPPER:
            raise Exception(f"Question mode {mode} not found. Allowed Are : { QuestionGeneratorBuilder.GENERATOR_MAPPER.keys()}" )
        return QuestionGeneratorBuilder.GENERATOR_MAPPER[mode]




