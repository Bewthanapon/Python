# pip install PyAutoGUI
# pip install pillow  # จัดการภาพ

import webbrowser
import pyautogui as pg
import time

def Search(keyword):
	# 1- open webbrower and goto google
	url = 'https://www.google.com'
	webbrowser.open(url)
	time.sleep(1)

	# 2- type "keyword"
	pg.write(keyword, interval = 0.25)
	time.sleep(1)

	# 3- press enter for searching
	pg.press('enter')
	time.sleep(1)

	# 4- capture (screenshot) and save to file
	pg.screenshot(keyword + '.png')

Search('bill gate')
Search('steve job')	
