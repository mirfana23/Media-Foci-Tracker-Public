from selenium import webdriver
import pandas as pd
import time
import json
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import clipboard
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import pyautogui
import os.path

#26 일이 조지 플로이드 사건
#그래서 25일 ~ 14일

papernames = ["usa-today-us-edition", "the-washington-post", "los-angeles-times", "the-dallas-morning-news", "houston-chronicle"]
dates = []
date_was = ["20200528", "20200529", "20200530", "20200601", "20200602", "20200603", "20200604", "20200605", "20200606", "20200608", "20200609", "20200610", "20200611", "20200612", "20200613"]
date_today = ["20200526", "20200527", "20200528", "20200529", "20200601", "20200602", "20200603", "20200604", "20200605", "20200608", "20200609", "20200610", "20200611", "20200612"]
date_los = ["20200525", "20200526", "20200527", "20200528", "20200529", "20200530", "20200531", "20200601", "20200602", "20200603", "20200604", "20200605", "20200606", "20200607", "20200608", "20200609", "20200610", "20200611", "20200612", "20200613", "20200614"]
date_dal = ["20200525", "20200526", "20200527", "20200528", "20200529", "20200530", "20200531", "20200601", "20200602", "20200603", "20200604", "20200605", "20200606", "20200607", "20200608", "20200609", "20200610", "20200611", "20200612", "20200613", "20200614"]
date_hous = ["20200525", "20200526", "20200527", "20200528", "20200529", "20200530", "20200601", "20200602", "20200603", "20200604", "20200605", "20200606", "20200608", "20200609", "20200610", "20200611", "20200612", "20200613"]

dates.append(date_today)
dates.append(date_was)
dates.append(date_los)
dates.append(date_dal)
dates.append(date_hous)
index = list(range(25))
settings = {
    "appState": {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local"
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }  
}
prefs = {'printing.print_preview_sticky_settings': json.dumps(settings)}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--kiosk-printing')
#chrome_options.add_argument('headless')
#chrome_options.add_argument('window-size=1920x1080')
#chrome_options.add_argument('disable-gpu')

for i in range(len(papernames)):
    for j in dates[i]:
        count = 1
        dobreak = False
        for k in index:
            if(dobreak):
                break
            try:
                driver = webdriver.Chrome(r'C:\Users\Asui\Downloads\chromedriver_win32 (2)\chromedriver.exe', chrome_options=chrome_options)
                driver.get("https://www.pressreader.com/usa/" + papernames[i] +"/"+j+"/page/1/textview")
                actions1 = webdriver.common.action_chains.ActionChains(driver)
                actions2 = webdriver.common.action_chains.ActionChains(driver)

                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="thumbsToolbarBottom_0"]/a')))

                bottom_button = driver.find_element_by_xpath('//*[@id="thumbsToolbarBottom_0"]/a')
    
                bottom_button.click()

                time.sleep(2)

                all_bottom = driver.find_element_by_xpath('//*[@id="thumbsToolbarBottomPreview_0"]')
                all_news = all_bottom.find_elements_by_xpath('//a[@page-number="1"]')
                
                news = all_news[k]
                first = True
            
                article_id = news.get_attribute("article-id")
                print(article_id)
                actions1.move_to_element(news).perform()
                news.click()



                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//article[@aid="'+str(article_id)+'"]')))
                time.sleep(2)
                arti = driver.find_element_by_xpath('//article[@aid="'+str(article_id)+'"]')
                head = arti.find_element_by_tag_name("hgroup")
                time.sleep(1)
                actions2.move_to_element(head).perform()
                time.sleep(1)
                actions2.context_click(head).perform()

                time.sleep(2)
                printbutton = driver.find_element_by_xpath('/html/body/div[12]/div/section/div/div/ul/li[7]/a')
                printbutton.click()

                time.sleep(1)

                printtext = driver.find_element_by_xpath('/html/body/div[12]/div/section/div/div/ul/li[1]/a')
                printtext.click()

                time.sleep(4)
                name = ""
                if(count < 10):
                    name = papernames[i]+"_"+j +"_"+"0"+ str(count)
                    pyautogui.typewrite(papernames[i]+"_"+j +"_"+"0"+ str(count))
                else:
                    name = papernames[i]+ "_"+j +"_" + str(count)
                    pyautogui.typewrite(papernames[i]+ "_"+j +"_" + str(count))
                        
                    
                time.sleep(1)
                pyautogui.press('enter')
                print("saved" + name)
    
                time.sleep(10)
                
                count+=1
                if k == len(all_news)-1:
                    driver.quit()
                    dobreak = True
                    break
                driver.quit()
                time.sleep(1)
            except:
                print("failed on" + papernames[i]+j+str(k))
                driver.quit()
                continue






