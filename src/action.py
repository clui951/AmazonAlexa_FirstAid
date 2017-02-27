"""First Aid.
This project uses a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located on github.
"""
GLOBAL_ATTRIBUTES = {"CURRENT_CPR_STEP" : "compression", "EXPLAINED_COMPRESSION" : False, "EXPLAINED_BREATH" : False}

def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])


def on_launch(launch_request, session):
    return get_welcome_response()

def get_welcome_response():
    print("IN GET_WELCOME_RESPONSE")
    session_attributes = {}
    card_title = "Welcome"
    reprompt_text = ""
    should_end_session = False

    speech_output = ("First Aid here, what can I help you with?")
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def call_911_response():
    session_attributes = {}
    card_title = "Call 911"
    reprompt_text = ""
    should_end_session = False

    speech_output = ("Call 911")
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "FirstAidIntent":
        return FirstAidIntent(intent_request)
    elif "CPR" in intent_name:
        if intent_name == "CPRExplainIntent":
            return CPRExplainIntent(intent_request)
        elif intent_name == "CPRStepIntent":
            return CPRStepIntent(intent_request)
        elif intent_name == "CPRStopIntent":
            return CPRStopIntent()
        elif intent_name == "CPRStopYesIntent":
            GLOBAL_ATTRIBUTES["CURRENT_CPR_STEP"] = "None"
            return CPRStopYesIntent()
        elif intent_name == "CPRStopNoIntent":
            return CPRRestartIntent() 
        elif intent_name == "CPRReadyIntent":
            return CPRReadyIntent()
        elif intent_name == "CPRDoneIntent":
            return CPRDoneIntent()
        elif intent_name == "CPRRestartIntent":
            return CPRRestartIntent()
    elif intent_name == "FirstAidMainIntent":
        GLOBAL_ATTRIBUTES["CURRENT_CPR_STEP"] = "compression"
        GLOBAL_ATTRIBUTES["EXPLAINED_COMPRESSION"] = False
        GLOBAL_ATTRIBUTES["EXPLAINED_BREATH"] = False
        return get_welcome_response()
    elif intent_name == "HelpIntent":
        return HelpIntent()


def HelpIntent():
    session_attributes = {}
    card_title = "CPR"
    reprompt_text = ""
    should_end_session = False
    speech_output = "You can say I need help with any of the following. "
    events = ["Checking an Injured Adult", "Choking", "CPR", "AED", "Controlling Bleeding", "Burns", "Poisoning", "Neck Injuries", "Spinal Injuries", "Stroke"]
    for event in events:
        speech_output += event
        speech_output += ". "
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def CPRStopYesIntent():
    session_attributes = {}
    card_title = "CPR"
    reprompt_text = ""
    should_end_session = False
    speech_output = "Thank you for performing CPR."
    GLOBAL_ATTRIBUTES["CURRENT_CPR_STEP"] = "compression"
    GLOBAL_ATTRIBUTES["EXPLAINED_COMPRESSION"] = False
    GLOBAL_ATTRIBUTES["EXPLAINED_BREATH"] = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def FirstAidIntent(intent_request):
    situation = intent_request["intent"]["slots"]["FirstAidItem"]["value"]
    if situation == "CPR":
        GLOBAL_ATTRIBUTES["CURRENT_CPR_STEP"] = "compression"

        session_attributes = {}
        card_title = "CPR"
        reprompt_text = ""
        should_end_session = False
        speech_output = "You will give 30 chest compressions. " + chest_compression_instructions() + " When you are ready, say ready."
        GLOBAL_ATTRIBUTES["EXPLAINED_COMPRESSION"] = True
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
    else:
        return call_911_response()

def CPRReadyIntent():
    session_attributes = {}
    card_title = "CPR"
    reprompt_text = ""
    should_end_session = False
    speech_output = "Begin. When you are done, say done."
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def CPRDoneIntent():
    print("IN CPRDONEINTENT")
    print(GLOBAL_ATTRIBUTES["CURRENT_CPR_STEP"])
    print("STEP ABOVE")
    session_attributes = {}
    card_title = "CPR"
    reprompt_text = ""
    should_end_session = False
    speech_output = ""
    if "compression" == GLOBAL_ATTRIBUTES["CURRENT_CPR_STEP"]:
        GLOBAL_ATTRIBUTES["CURRENT_CPR_STEP"] = "breath"
        if GLOBAL_ATTRIBUTES["EXPLAINED_BREATH"]:
            speech_output = "You will give 2 rescue breaths. When you are ready, say ready."
        else:
            GLOBAL_ATTRIBUTES["EXPLAINED_BREATH"] = True
            speech_output = "You will give 2 rescue breaths. " + rescue_breath_instructions() + " When you are ready, say ready."
    elif "breath" == GLOBAL_ATTRIBUTES["CURRENT_CPR_STEP"]:
        GLOBAL_ATTRIBUTES["CURRENT_CPR_STEP"] = "compression"
        if GLOBAL_ATTRIBUTES["EXPLAINED_COMPRESSION"]:
            speech_output = "You will give 30 chest compressions. When you are ready, say ready."
        else:
            GLOBAL_ATTRIBUTES["EXPLAINED_COMPRESSION"] = True
            speech_output = "You will give 30 chest compressions. " + chest_compression_instructions() + " When you are ready, say ready."
    print(speech_output)
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def CPRRestartIntent():
    session_attributes = {}
    card_title = "CPR"
    reprompt_text = ""
    should_end_session = False
    step = GLOBAL_ATTRIBUTES["CURRENT_CPR_STEP"]
    speech_output = ""
    if "compression" in step:
        GLOBAL_ATTRIBUTES["CURRENT_CPR_STEP"] = "compression"
        speech_output = "You will give 30 chest compressions. When you are ready, say ready."
    elif "breath" in step:
        GLOBAL_ATTRIBUTES["CURRENT_CPR_STEP"] = "breath"
        speech_output = "You will give 2 rescue breaths. When you are ready, say ready."
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def CPRStepIntent(intent_request):
    step = intent_request["intent"]["slots"]["CPRStep"]["value"]
    # restart at this step
    session_attributes = {}
    card_title = "CPR"
    reprompt_text = ""
    should_end_session = False
    speech_output = ""
    if "compression" in step:
        GLOBAL_ATTRIBUTES["CURRENT_CPR_STEP"] = "compression"
        speech_output = "You will give 30 chest compressions. When you are ready, say ready."
    elif "breaths" in step:
        GLOBAL_ATTRIBUTES["CURRENT_CPR_STEP"] = "breath"
        speech_output = "You will give 2 rescue breaths. When you are ready, say ready."
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def CPRExplainIntent(intent_request):
    step = intent_request["intent"]["slots"]["CPRStep"]["value"]

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
    return "To do chest compressions, push hard, push fast in the middle of the chest at least 2 inches deep" + " and at least 100 compressions per minute."

def rescue_breath_instructions():
    return "To do rescue breaths, tilt the head back and lift the chin. Pinch the nose and make a seal over the person's mouth." + " Blow in for 1 second to make the chest clearly rise. Give breaths one after the other."


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



