"""First Aid.
This project uses a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located on github.
"""

CURRENT_CPR_STEP = "None"

def lambda_handler(event, context):
	print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

	if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    print("Starting Session")

def on_launch(launch_request, session):
    return get_welcome_response()

def on_session_ended(session_ended_request, session):
	print("Ending Session")

def get_welcome_response():
	session_attributes = {}
	card_title = "Welcome"
	reprompt_text = ""
    should_end_session = False

    speech_output = ("First Aid here, what can I help you with?")
    return build_response(session_attributes, build_speechlet_response(
    	card_title, speech_output, reprompt_text, should_end_session))

def call_911_response():
	session_attributes = {}
	card_title = "Call 911"
	reprompt_text = ""
    should_end_session = False

    speech_output = ("Call 911")
    return build_response(session_attributes, build_speechlet_response(
    	card_title, speech_output, reprompt_text, should_end_session))


def on_intent(intent_request, session):
	intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "FirstAidIntent":
    	return FirstAidIntent(intent_request)
    elif "CPR" in intent_name:
	    elif intent_name == "CPRExplainIntent":
	    	return CPRExplainIntent(intent_request)
	   	elif intent_name == "CPRStepIntent":
	   		return CPRStepIntent(intent_request)
	   	elif intent_name == "CPRStopIntent":
	   		return CPRStopIntent()
	   	elif intent_name == "CPRStopYesIntent":
	   		nonlocal CURRENT_CPR_STEP
	   		CURRENT_CPR_STEP = "None"
	   		return get_welcome_response()
	   	elif intent_name == "CPRStopNoIntent":
	   		return CPRRestartIntent() 
	   	elif intent_name == "CPRReadyIntent":
	   		return CPRReadyIntent()
	   	elif intent_name == "CPRDoneIntent":
	   		return CPRDoneIntent()
	   	elif intent_name == "CPRRestartIntent":
	   		return CPRRestartIntent()
   	elif intent_name == "FirstAidMainIntent":
   		nonlocal CURRENT_CPR_STEP 
   		CURRENT_CPR_STEP = "compression"
   		return get_welcome_response()


def FirstAidIntent(intent_request):
	situation = intent_request["slots"]["FirstAidItem"]["value"]
	if situation == "CPR":
		nonlocal CURRENT_CPR_STEP
		CURRENT_CPR_STEP = "Compression"

		session_attributes = {}
		card_title = "CPR"
		reprompt_text = ""
	    should_end_session = False
		speech_output = "You will give 30 chest compressions. " + chest_compression_instructions() + " When you are ready, say ready."
		return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
	else:
		return call_911_response()

def CPRReadyIntent(intent_request):
	session_attributes = {}
	card_title = "CPR"
	reprompt_text = ""
	should_end_session = False
	speech_output = "Begin. When you are done, say done."
	return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def CPRDoneIntent(intent_request):
	session_attributes = {}
	card_title = "CPR"
	reprompt_text = ""
	should_end_session = False
	nonlocal CURRENT_CPR_STEP
	if "compression" in CURRENT_CPR_STEP:
		CURRENT_CPR_STEP = "breath"
		speech_output = "You will give 2 rescue breaths. When you are ready, say ready."
	elif "breath" in CURRENT_CPR_STEP:
		CURRENT_CPR_STEP = "compression"
		speech_output = "You will give 30 chest compressions. When you are ready, say ready."
	return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def CPRRestartIntent(intent_request):
	session_attributes = {}
	card_title = "CPR"
	reprompt_text = ""
    should_end_session = False
    nonlocal CURRENT_CPR_STEP
	step = CURRENT_CPR_STEP
	speech_output = ""
	if "compression" in step:
		CURRENT_CPR_STEP = "compression"
		speech_output = "You will give 30 chest compressions. When you are ready, say ready."
	elif "breath" in step:
		CURRENT_CPR_STEP = "breath"
		speech_output = "You will give 2 rescue breaths. When you are ready, say ready."
	return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def CPRStepIntent(intent_request):
	step = intent_request["slots"]["CPRStep"]["value"]
	# restart at this step
	session_attributes = {}
	card_title = "CPR"
	reprompt_text = ""
    should_end_session = False
    speech_output = ""
	nonlocal CURRENT_CPR_STEP
	if "compression" in step:
		CURRENT_CPR_STEP = "compression"
		speech_output = "You will give 30 chest compressions. When you are ready, say ready."
	elif "breaths" in step:
		CURRENT_CPR_STEP = "breath"
		speech_output = "You will give 2 rescue breaths. When you are ready, say ready."
	return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def CPRExplainIntent(intent_request):
	step = intent_request["slots"]["CPRStep"]["value"]

	session_attributes = {}
	card_title = "CPR"
	reprompt_text = ""
    should_end_session = False
	if step == "compressions" or step == "chest compressions":
		speech_output = chest_compression_instructions()
		return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
	elif step == "rescue breaths" or step == "breaths":
		speech_output = rescue_breath_instructions()
		return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def chest_compression_instructions():
	return "To do chest compressions, push ahrd, push fast in the middle of the chest at least 2 inches deep" +
		" and at least 100 compressions per minute."

def rescue_breath_compressions():
	return "To do rescue breaths, tilt the head back and lift the chin. Pinch the nose and make a seal over the person's mouth." +
		" Blow in for 1 second to make the chest clearly rise. Give breaths one after the other."


def CPRStopIntent():
	session_attributes = {}
	card_title = "CPR"
	reprompt_text = ""
    should_end_session = False
    speech_output = "Are you sure you want to stop CPR?"
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))



def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }



