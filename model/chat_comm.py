import datetime
import uuid 

class Input_Message:
    def __init__(self, id, channel, timestamp, query):
        self.id = id
        self.channel = channel
        self.timestamp = timestamp
        self.query = query

class Output_Message:
    def __init__(self, id, timestamp, input_id, response):
        self.id = id
        self.timestamp = timestamp
        self.input_id = input_id
        self.response = response

class Chat_Comm:
    def __init__(self):
        self.chat_history = []

    def interaction(self, input_message):
        # Here you will implement your chatbot's response logic
        # For now, it just echoes the input message query
        response_text = "Echo: " + input_message.query

        output_message = Output_Message(
            id=str(uuid.uuid4()), 
            timestamp=datetime.datetime.now(), 
            input_id=input_message.id, 
            response=response_text
        )
        
        self.chat_history.append((input_message, output_message))
        return output_message
