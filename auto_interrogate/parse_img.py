# from time import time
import pytesseract
from PIL import Image

# t = time()
QUES_COORDS = (0, 450, 1440, 930)
OPTS_COORDS = [
    (10, 900, 720, 1440),
    (730, 900, 1440, 1440),
    (10, 1430, 720, 1900),
    (730, 1430, 1440, 1900),
]

def parse_question(img):
    q_img = img.crop(QUES_COORDS)
    # q_img.show()
    return parse_text(q_img)

def parse_options(img):
    opt_texts = tuple()
    for opt in OPTS_COORDS:
        o_img = img.crop(opt)
        # o_img.show()
        opt_texts += (parse_text(o_img), )
    return opt_texts

def parse_text(img):
    txt = ''
    while txt == '':
        txt = pytesseract.image_to_string(img)
        txt = txt.strip()
        txt = txt.replace('\n', ' ')
        # hacks start
        txt = txt.replace('|', 'I')
        # txt = txt.lower()
        if txt != '':
            break
        img = crop_reduce(img)
        # img.show()
    return txt

def load_img(path):
    return Image.open(path)

def crop_reduce(img, ratio=0.2):
    '''
    crop reduce image from all four
    directions by the passed ratio
    '''
    height, width = img.size
    rfh = ((width * ratio) / 2) # reduce from horizontal
    rfv = ((height * ratio) / 2) # reduce from vertical
    
    left = rfh
    top = rfv
    right = width - rfh
    bottom = height - rfv

    c_img = img.crop((left, top, bottom, right, ))
    # c_img.show()
    return c_img
    
    

if __name__ == '__main__':
    for raw in [
        # 'Screenshot_20211007-104155_Indefinite.jpeg',
        # 'Screenshot_20211007-104201_Indefinite.jpeg',
        # 'Screenshot_20211007-104204_Indefinite.jpeg',
        # 'Screenshot_20211007-104210_Indefinite.jpeg',
        # 'Screenshot_20211007-104213_Indefinite.jpeg',
        # 'Screenshot_20211007-104216_Indefinite.jpeg',
        'screen.png',
        # 'age.png',
        # 'kill.png',
    ]:
        img = load_img(f'auto_interrogate/res/raw/{raw}')
        
        # print(img.size)
        q = parse_question(img)
        print(q)

        os = parse_options(img)
        for o in os:
            print(f'- {o}')

        print('=========')

# print(time()-t)