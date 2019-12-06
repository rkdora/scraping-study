from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time
import io
from urllib import request
from PIL import Image
from datetime import datetime

webdriver = webdriver.Chrome(executable_path='/Users/ryuto/Downloads/chromedriver')
webdriver.get('http://localhost:5000/')

time.sleep(3)

elem = webdriver.find_element_by_xpath('//*[@id="num_img"]')
url = elem.get_attribute('src')
f = io.BytesIO(request.urlopen(url).read())
img = Image.open(f)
img.save('./img/' + datetime.now().strftime('%s') + '.jpg')

write = str(1)

webdriver.find_element_by_xpath('/html/body/form/p[1]/input').send_keys(write)

print('write', write)

time.sleep(3)

webdriver.find_element_by_xpath('/html/body/form/p[2]/input').click()

time.sleep(3)

message = webdriver.find_elements_by_css_selector('p.ans')

print(message[0].text)

time.sleep(3)

webdriver.quit()
