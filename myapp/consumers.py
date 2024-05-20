import json
from channels.generic.websocket import WebsocketConsumer

class TypingConsumer(WebsocketConsumer):
    snippets = [
        'The quick brown fox jumps over the lazy dog',
        'its hakus',
        'To be or not to be, that is the question'
    ]
    current_snippet_index = 0
    
    def connect(self):
        self.accept()
        self.send_new_snippet()


    def send_new_snippet(self):
        if self.current_snippet_index < len(self.snippets):
            snippet_text = self.snippets[self.current_snippet_index]
            self.send(json.dumps({
                'typed_text': '',
                'remaining_text': snippet_text,
                'is_correct': False
            }))
        else:
            self.send(json.dumps({
                'game_over': True
            }))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        typed_text = data.get('typed_text', '').lower()
        snippet_text = data.get('snippet_text', '').lower()

        is_correct = typed_text == snippet_text
        if is_correct:
            self.current_snippet_index = (self.current_snippet_index + 1)
            self.send_new_snippet()
        else:
            remaining_text = snippet_text[len(typed_text):]
            self.send(json.dumps({
                'typed_text': typed_text,
                'remaining_text': remaining_text,
                'is_correct': is_correct
            }))