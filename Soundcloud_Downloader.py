#   Author: Ryan Guidice
#   Description: Script to automate downloading soundcloud songs and importing them into iTunes

import sys
import os
from selenium import webdriver
import time

if __name__ == "__main__":
    song_link = sys.argv[1]
    sc_download_website = 'https://scdownloader.io/'
    chrome_options = webdriver.ChromeOptions()
    music_direc = "D:\Ryan\Downloads"
    prefs = {'download.default_diretory':music_direc}
    chrome_options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(sc_download_website)

    driver.find_element_by_id("videoURL").click()
    driver.find_element_by_id("videoURL").send_keys(song_link)
    driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div[5]/div[1]/div[1]/form/button").click()
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/a/i").click()




