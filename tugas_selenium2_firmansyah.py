from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


websites = [
    'https://tiket.com',
    'https://tokopedia.com',
    'https://orangsiber.com',
    'https://demoqa.com',
    'https://automatetheboringstuff.com'
]

chrome_options = webdriver.Chrome()
chrome_options.minimize_window()

for website in websites:
        chrome_options.get(website)
        Title = chrome_options.title
        time.sleep(2)
        Name = website.replace('https://','')
        print(Name,'-',Title)

chrome_options.close()
