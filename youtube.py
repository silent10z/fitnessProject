from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

import urllib.request

driver = webdriver.Chrome()
driver.get("https://www.youtube.com/")
search = driver.find_element_by_name("search_query")
# 검색할 키워드 정하기
searchKey = ["양선수", "피지컬갤러리", "세계적으로 유명한 운동 정보", "자연산 광호야 WNBF Pro"]
search.send_keys(searchKey[3])
search.send_keys(Keys.ENTER)
time.sleep(2)
# 동영상 갯수 가져오기
video_count = int(driver.find_element_by_css_selector("#video-count").text[4:-1])

# 메인화면 클릭
driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-renderer/div/div[1]/a/div/yt-img-shadow/img").click()

time.sleep(2)
# 동영상 클릭
driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/app-header-layout/div/app-header/div[2]/app-toolbar/div/div/paper-tabs/div/div/paper-tab[2]").click()


time.sleep(2)

playList = driver.find_elements_by_css_selector("#items > ytd-grid-video-renderer")
# 유트브 영상길이 만큼 스크롤 끝까지 내리기
while(video_count > 0):
    time.sleep(2)
    driver.find_element_by_tag_name('body').send_keys(Keys.END)

    video_count = video_count - len(playList)
# 모든 리스트 영상 링크와 제목 가져오기
all_playLists = driver.find_elements_by_css_selector("#items > ytd-grid-video-renderer")

title_list = []
video_list = []
for all_playList in all_playLists:
    print(all_playList.find_element_by_css_selector("#thumbnail").get_attribute("href"))
    print(all_playList.find_element_by_css_selector("#meta > h3").text)
    title_list.append(all_playList.find_element_by_css_selector("#meta > h3").text)
    video_list.append(all_playList.find_element_by_css_selector("#thumbnail").get_attribute("href"))

youtube_info = pd.DataFrame({"title_list":title_list, "video_list":video_list})
print(youtube_info)
vidoeList = youtube_info.to_csv()