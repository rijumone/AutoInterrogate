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
from pprint import pprint
from loguru import logger
from parse_img import *
from nlp import *
from entities import *

questions_superset = []

TOKEN_MISMATCH_THRESHOLD = 0
OPTION_COORDS = {
    0: (430, 1180),
    1: (1048, 1180),
    2: (430, 1630),
    3: (1048, 1630),
}


def play():
    print('Ctrl + C to exit.')
    while True:
        try:
            img_path = screencap_pull()
            img = load_img(img_path)
            q_txt = parse_question(img)
            tokens = get_tokens(q_txt)
            logger.debug(q_txt)
            opts_txt = parse_options(img)
            # attempting to match question
            prev_q = find_q_match(tokens)
            logger.success(prev_q)
            if prev_q:
                selected_option = get_correct_option(prev_q, opts_txt)
            else:
                selected_option = 0
            if selected_option is None:
                logger.critical(tokens)
            logger.success(selected_option)
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
            pprint(questions_superset)
            break


def get_correct_option(q, opts):
    logger.debug(q)
    for i, o in enumerate(opts):
        logger.debug(o)
        if o == q.selected_option.text:
            return i


def find_q_match(tokens):
    tokens_set = set(tokens)
    for q in questions_superset:
        match_cnt = 0
        q_tokens_set = set(q.tokens)

        # logger.debug(tokens_set)
        # logger.debug(q_tokens_set)
        for t in tokens_set:
            if t in q_tokens_set:
                match_cnt += 1
        # logger.debug(match_cnt)
        mismatch_cnt = len(tokens_set) - match_cnt
        # logger.debug(mismatch_cnt)
        if mismatch_cnt <= TOKEN_MISMATCH_THRESHOLD:
            return q


def tap_option(option):
    coords = OPTION_COORDS[option]
    _cmd = f'adb shell input tap {coords[0]} {coords[1]}'
    print(_cmd)
    call(_cmd.split(' '))


def screencap_pull():
    _local_path = 'auto_interrogate/res/raw/screen.png'
    _cmd = ['adb', ]
    call(_cmd+['shell', 'screencap', '-p', '/sdcard/screen.png'])
    call(_cmd+(f'pull /sdcard/screen.png {_local_path}').split(' '))
    return _local_path


if __name__ == '__main__':
    # _local_path = screencap_pull()
    # print(_local_path)
    
    # i = get_correct_option(
    #     q=Question(text='Where were you born?', tokens=['where', 'were', 'born'], options=(
    #         'Germany', 'The United  States', 'China', 'Indonesia'), selected_option=Option(text='The United  States')),
    #     opts=('Italy', 'Mexico', 'The United  States', 'Israel'),
    # )
    # print(i)

    play()