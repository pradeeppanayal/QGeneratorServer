from flask import Flask, request, send_from_directory, Response
import json
import logging
from Qgenerator import QuestionGeneratorBuilder

#########################################
#   @author: Pradeep CH                 #
#   @version: 1.0                       #
#                                       #
#########################################

# The app object which is consumed by the Server
app = Flask(__name__)

#log info
LOG_FILE ="log.log"
LOG_LEVEL = logging.DEBUG

# Index page
@app.route('/qgenerator/<filename>')
def index(filename):
   logging.info(f"Providing file {filename}")
   return send_from_directory('static',filename)

# API end point
@app.route('/qgenerator/api/generate',methods=['POST'])
def generateQuestions():   
    try:      
      logging.info(f"Payload {request.json}")
      data = request.json  
      if 'mode' not in data:
        data['mode'] = QuestionGeneratorBuilder.YES_OR_NO
      if 'payload' not in data:
        return prepareResponse("Payload missing",False), 400
      generator = QuestionGeneratorBuilder.getGenerator(data['mode'])
      result = generator.generate(data['payload'])

      if 'ouputType' in data and data['ouputType'] == 'text':
        result= generator.asText(result)

      logging.debug(f"Result : {result}")
      return prepareResponse(result)
    except Exception as e:
      logging.exception(e)
      return prepareResponse(f'Request failed with error : {e}', False), 500

def prepareResponse(data, success = True) -> str:
  resp = {'data': data}
  if success:
    resp['status'] = 'Success'
  else:
    resp['status'] = 'Error'
  return json.dumps(resp)

def _initLogging():  
  loggingLevel = logging.DEBUG; 
  logging.basicConfig(filename=LOG_FILE, level=loggingLevel,format='%(asctime)s %(levelname)s %(message)s');

# init the log files
_initLogging()

if __name__ == '__main__': 
    app.run() 