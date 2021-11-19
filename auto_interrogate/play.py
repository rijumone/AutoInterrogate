'''
- Game will be in ready-to-play state.
- Screencap and download
- Figure out question and options
- Check records for question
    - answer if record found
- if not found    
    - Save question and options
    - Select one
    - Remember selection
'''
from subprocess import call
from loguru import logger
from parse_img import *
from nlp import *
from entities import *

questions_superset = []

TOKEN_MISMATCH_THRESHOLD = 1
OPTION_COORDS = {
    1: (430, 1180),
    2: (1048, 1180),
    3: (430, 1630),
    4: (1048, 1630),
}

def play():
    print('Ctrl + C to exit.')
    while True:
        try:
            img_path = screencap_pull()
            img = load_img(img_path)
            q_txt = parse_question(img)
            tokens = get_tokens(q_txt)

            opts_txt = parse_options(img)
            # attempting to match question
            prev_q = find_q_match(tokens)
            logger.info(prev_q)
            selected_option = 1 # hardcoded for now
            q = Question(
                text=q_txt,
                tokens=tokens,
                options=opts_txt,
                selected_option=Option(text=opts_txt[selected_option]),
            )
            logger.debug(q)
            questions_superset.append(q)
            
            tap_option(selected_option)
            # input()
        except KeyboardInterrupt:
            print(questions_superset)
            break

def find_q_match(tokens):
    tokens_set = set(tokens)
    for q in questions_superset:
        match_cnt = 0
        q_tokens_set = set(q.tokens)
        for t in tokens_set:
            if t in q_tokens_set:
                match_cnt += 1
        if abs(match_cnt-len(tokens_set)) <= TOKEN_MISMATCH_THRESHOLD and abs(len(tokens_set & q_tokens_set)) <= TOKEN_MISMATCH_THRESHOLD:
            logger.debug(match_cnt)
            logger.debug(tokens_set)
            logger.debug(q_tokens_set)
            return q
        



def tap_option(option):
    coords = OPTION_COORDS[option]
    _cmd = f'adb shell input tap {coords[0]} {coords[1]}'
    print(_cmd)
    call(_cmd.split(' '))

def screencap_pull():
    _local_path = 'auto_interrogate/res/raw/screen.png'
    _cmd = ['adb',]
    call(_cmd+['shell', 'screencap', '-p', '/sdcard/screen.png'])
    call(_cmd+(f'pull /sdcard/screen.png {_local_path}').split(' '))
    return _local_path

if __name__ == '__main__':
    # _local_path = screencap_pull()
    # print(_local_path)
    play()