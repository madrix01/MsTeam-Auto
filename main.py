from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import json


opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.notifications": 1 
})


driver = webdriver.Chrome(options=opt)
driver.get("https://teams.microsoft.com/")
time.sleep(4)
f = open('teams.json')
config = json.load(f)


def login():
    #Username
    username = driver.find_element_by_css_selector('#i0116')
    username.send_keys(config["login"]["email"])
    driver.find_element_by_css_selector('#idSIButton9').click() #next

    #password
    password = driver.find_element_by_css_selector('#i0118')
    password.send_keys(config["login"]["pwd"])
    time.sleep(2)
    nxt = driver.find_element_by_css_selector('#idSIButton9') #next
    nxt.click()

    #stay signed in
    driver.find_element_by_css_selector('#idSIButton9').click()
    #Continue to web app 
    driver.find_element_by_css_selector('#download-desktop-page > div > a').click()

def openTeam(tm):
    try:
        team_xp = '//*[@id="' + config["team"][tm] + '"]/a'
        team_to_join = driver.find_element_by_xpath(team_xp)
        if team_to_join is not None:
            team_to_join.click()
        time.sleep(5)
    except:
        print("No team found. Check xpath")
    #finding join button
    try:
        join_meeting = driver.find_elements_by_css_selector("button[ng-click='ctrl.joinCall()']")
        if join_meeting is not None:
            join_meeting[0].click()
    except:
        print("There is no active meeting")
        return 0
    time.sleep(4)
    
    #turn off mic
    audio_btn = driver.find_element_by_css_selector("toggle-button[data-tid='toggle-mute']>div>button")
    audio_is_on = audio_btn.get_attribute("aria-pressed")
    if audio_is_on == "true":
        audio_btn.click()

    #turn off camera 
    video_btn = driver.find_element_by_css_selector("toggle-button[data-tid='toggle-video']>div>button")
    video_is_on = video_btn.get_attribute("aria-pressed")
    if video_is_on == "true":
        video_btn.click()
    
    time.sleep(4)
    #join meeting
    join_now_btn = driver.find_element_by_css_selector("button[data-tid='prejoin-join-button']")
    if join_now_btn is not None:
        join_now_btn.click()



if __name__ == '__main__':
    login()
    time.sleep(5)
    openTeam("Test")