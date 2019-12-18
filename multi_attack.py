import time
import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import io
from urllib import request
from PIL import Image
from datetime import datetime
import numpy as np
from dnn import model

def attack_captcha(webdriver, idx):

    now_time = datetime.now().strftime('%s')

    elem = webdriver.find_element_by_xpath('//*[@id="num_img"]')
    url = elem.get_attribute('src')
    f = io.BytesIO(request.urlopen(url).read())
    img = Image.open(f)
    img_path = './img/' + now_time + '.jpg'
    img.save(img_path)
    img_arr = np.asarray(img) / 255

    pre_label = model.predict(img_arr)

    time.sleep(1)

    write = str(pre_label)

    webdriver.find_element_by_xpath('/html/body/form/p[1]/input').send_keys(write)

    print("idx: ", idx, "predict:", write)

    time.sleep(1)

    webdriver.find_element_by_xpath('/html/body/form/p[2]/input').click()

    message = webdriver.find_elements_by_css_selector('p.ans')

    print("idx: ", idx, "message:", message[0].text)

    time.sleep(3)

    webdriver.quit()


th_objs = []
driver = {}

browsers = [
    { "size-x": "640", "size-y": "480", "pos-x": "0",    "pos-y": "0"},
    { "size-x": "640", "size-y": "480", "pos-x": "640",  "pos-y": "0"},
    { "size-x": "640", "size-y": "480", "pos-x": "1280", "pos-y": "0"},
    { "size-x": "640", "size-y": "480", "pos-x": "0",    "pos-y": "480"},
    { "size-x": "640", "size-y": "480", "pos-x": "640",  "pos-y": "480"},
    { "size-x": "640", "size-y": "480", "pos-x": "1280", "pos-y": "480"}
]

def proc(idx):
    browser = browsers[idx]
    tid = threading.get_ident()

    driver[tid] = webdriver.Chrome(executable_path='/Users/ryuto/Downloads/chromedriver')

    driver[tid].set_window_size(browser['size-x'], browser['size-y'])
    driver[tid].set_window_position(browser['pos-x'], browser['pos-y'])


    print("idx: ", idx, "id:", threading.get_ident())
    driver[tid].get('http://localhost:5000/')
    time.sleep(3)

    attack_captcha(driver[tid], idx)


if __name__ == '__main__':

    for idx in range(0,len(browsers)):
        th_objs.append( threading.Thread( target=proc,args=(idx,)))

    for i in range(0,len(browsers)):
        th_objs[i].start()
