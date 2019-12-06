from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time
import io
from urllib import request
from PIL import Image
from datetime import datetime
import numpy as np

from dnn import model

now_time = datetime.now().strftime('%s')

webdriver = webdriver.Chrome(executable_path='/Users/ryuto/Downloads/chromedriver')
webdriver.get('http://localhost:5000/')

elem = webdriver.find_element_by_xpath('//*[@id="num_img"]')
url = elem.get_attribute('src')
f = io.BytesIO(request.urlopen(url).read())
img = Image.open(f)
img_path = './img/' + now_time + '.jpg'
img.save(img_path)
img_arr = np.asarray(img) / 255

pre_label = model.predict(img_arr)

time.sleep(2)

write = str(pre_label)

webdriver.find_element_by_xpath('/html/body/form/p[1]/input').send_keys(write)

print('write', write)

time.sleep(1)

webdriver.find_element_by_xpath('/html/body/form/p[2]/input').click()

message = webdriver.find_elements_by_css_selector('p.ans')

print(message[0].text)

time.sleep(2)

webdriver.quit()
