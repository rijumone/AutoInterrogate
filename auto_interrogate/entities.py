from collections import namedtuple

Question = namedtuple('Question', [
    'text', 'tokens', 'options', 'selected_option'])
Option = namedtuple('Option', ['text'])