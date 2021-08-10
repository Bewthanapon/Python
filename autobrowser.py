# pip install PyAutoGUI
# pip install pillow  # จัดการภาพ ไม่ต้อง import PIL

# part 1
import webbrowser
import pyautogui as pg
import time
import pyperclip

def Search(keyword, eng=False, scroll=False, sctime=10):
	# 1- open webbrower and goto google
	url = 'https://www.google.com'
	webbrowser.open(url)
	time.sleep(1)

	# 2- type "keyword"
	if eng == True:
		pg.write(keyword, interval = 0.25)
	else:
		pyperclip.copy(keyword)
		time.sleep(1)
		pg.hotkey('ctrl', 'v')

	time.sleep(1)

	# 3- press enter for searching
	pg.press('enter')
	time.sleep(1)

	# 4- capture (screenshot) and save to file
	if scroll == True:
		for i in range(sctime):
			pg.scroll(-200)
			pg.screenshot('{}-{} .png'.format(keyword, i+1))
			time.sleep(1)
	else:
		pg.screenshot(keyword + '.png')
	

Search('ราคาน้ำมัน',scroll=True)
#Search('bill gate')
#Search('steve job')	


# part 2 

import webbrowser
import pyautogui as pg
import time

def Scan(url, sctime=10):
	
	webbrowser.open(url)
	time.sleep(2)
	webname = url.split('//')[1]

	for i in range(sctime):
		pg.scroll(-500)
		pg.screenshot('{}-{} .png'.format(webname, i+1))
		time.sleep(1)

url = 'https://www.bbc.com'
Scan(url, sctime=5)




