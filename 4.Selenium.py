# https://selenium-python.readthedocs.io/installation.html

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driverpath = r'D:\Python BootCamp 2021 by Uncle Engineer\classs main\RPA3-4\chromedriver_win32\chromedriver.exe'
driver = webdriver.Chrome(driverpath)

url = 'http://www.uncle-machine.com/'
driver.get(url)

username = driver.find_element_by_id('username')
username.send_keys('prayut@gmail.com')

password = driver.find_element_by_id('password')
password.send_keys('1234') 


#password.send_keys(keys.RETURN)  # press enter aafter type password

button = driver.find_element_by_xpath('/html/body/div[2]/form/button')
button.click()

addurl = 'http://www.uncle-machine.com/addproduct/'

driver.get(addurl)  # goto addurl

# add Product

pdname = driver.find_element_by_id('name')
pdprice = driver.find_element_by_id('price')
pddetail= driver.find_element_by_id('detail')

pd1_name = 'ทุเรียนจากเซี่ยงไฮ้ก็อปเกรด A'
pd1_price = 1000
pd1_detail = ''' ทุเรียน เป็นไม้ผลในวงศ์ฝ้าย 
'''

time.sleep(2)

pdname.send_keys(pd1_name)
pdprice.send_keys(pd1_price)
pddetail.send_keys(pd1_detail)

button = driver.find_element_by_xpath('/html/body/div[2]/form/button')
button.click()

