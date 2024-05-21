import json
from channels.generic.websocket import WebsocketConsumer
import random

class TypingConsumer(WebsocketConsumer):
    snippets_list = [
        'the man',
        'its hakus',
        'houssem'
    ]

    def __init__(self):
        super().__init__()
        self.snippet = random.choice(self.snippets_list)
        self.current_snippet_index = 0
        self.player_score = 0
        
    def connect(self):
        self.accept()

    def send_new_snippet(self):
        self.snippet = random.choice(self.snippets_list)
        if self.current_snippet_index < len(self.snippets_list):
            snippet_text = self.snippet.lower()
            self.send(json.dumps({
                'typed_text':'',
                'snippet_text':snippet_text,
                'remaining_text':snippet_text,
                'is_correct':False,
                'player_score':self.player_score,
                }))
        else:
            self.send(json.dumps({
                'game_over':True,
                'player_score':self.player_score,
            }))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action', None)
        
        if action in ['start']:
            self.player_score = 0
            self.current_snippet_index = 0
            self.send_new_snippet()
            return
        
        typed_text = data.get('typed_text', '').lower()
        snippet_text = data.get('snippet_text', '').lower()
        
        is_correct = typed_text == snippet_text
        if is_correct:
            self.player_score += 1
            self.current_snippet_index += 1
            self.send(json.dumps({
                'is_correct':is_correct,
                'player_score':self.player_score,
            }))
            self.send_new_snippet()
        else:
            remaining_text = snippet_text[len(typed_text):]
            self.send(json.dumps({
                'snippet_text':snippet_text,
                'typed_text':typed_text,
                'remaining_text':remaining_text,
            }))