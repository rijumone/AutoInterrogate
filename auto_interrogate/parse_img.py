from time import time
import concurrent.futures
import pytesseract
from PIL import Image

t = time()
QUES_COORDS = (0, 450, 1440, 930)
OPTS_COORDS = [
    (130, 944, 656, 1348),
    (784, 944, 1300, 1348),
    (130, 1453, 656, 1850),
    (784, 1453, 1300, 1850),
]
CROP_REDUCE_RATIO = 0.225

def parse_question(img):
    q_img = img.crop(QUES_COORDS)
    # q_img.show()
    return parse_text(q_img)

def parse_options(img):
    opt_texts = tuple()
    
    # for opt in OPTS_COORDS:
    #     o_img = img.crop(opt)
    #     opt_texts += (parse_text(o_img), )
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        c_imgs = [img.crop(_) for _ in OPTS_COORDS]
        results = executor.map(parse_text, c_imgs)
        for result in results:
            opt_texts += (result, )



    return opt_texts



def parse_text(img):
    txt = ''
    retry_ctr = 0
    while txt == '':
        if retry_ctr >= 4:
            txt = pytesseract.image_to_string(img, config='--psm 6')
        else:
            txt = pytesseract.image_to_string(img)
        txt = txt.strip()
        txt = txt.replace('\n', ' ')
        # hacks start
        txt = txt.replace('|', 'I')
        # txt = txt.lower()
        if txt != '':
            break
        img = crop_reduce(img, ratio=CROP_REDUCE_RATIO)
        retry_ctr += 1
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
        # 'screen.png',
        # 'age.png',
        # 'kill.png',
        # 'kill_1.png',
        'kill_2.png',
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