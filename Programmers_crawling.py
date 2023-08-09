# 프로그래머스 스쿨 크롤링

import os
import time
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import os
# Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록한다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django


# 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만든다.
django.setup()
from posts.models import Post

def get_all_results():

    driver = webdriver.Chrome()

    # 검색할 키워드 
    # search_text = ["c언어"]
    search_text = ["Django", "React", "Spring","C언어", "Python", "Java"]

    count_all = 0


    for i in range(len(search_text)):
        
        # 크롬드라이버로 원하는 url로 접속
        url = 'https://school.programmers.co.kr/learn/'
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(3)  # 페이지 로딩을 위해 3초간 기다림.

        # 검색창에 키워드 입력 후 엔터
        search_input = driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[1]/section/div/form/input')
        search_input.send_keys(search_text[i])
        search_input.send_keys(Keys.ENTER)

        result = []
        time.sleep(10)
        list_items = driver.find_elements(By.CSS_SELECTOR,'a.CourseCardstyle__Item-sc-ohrux3-0.cjNXwy')
        
        count = 0
        all_results = []
        
        for item in list_items:
            
            # lesson_title
            lesson_title_element = item.find_element(By.CSS_SELECTOR, 'div.CourseCardstyle__ItemTop-sc-ohrux3-3.klZNCl h3.CourseCardstyle__ItemTitle-sc-ohrux3-4.htqgyH')
            lesson_title = lesson_title_element.text.strip()
            if 'Javascript' in lesson_title or '자바스크립트' in lesson_title:
                break

            
            # image_url    
            image_tag = item.find_element(By.CSS_SELECTOR, 'div.CourseCardstyle__Thumbnail-sc-ohrux3-1.iuZcqv img')
            code_image = image_tag.get_attribute('src')
            
            
            # site_url
            course_link = item.get_attribute('href')
            if course_link:
                course_link
            else:
                course_link = None
            

            # price
            price_element = item.find_element(By.CSS_SELECTOR, 'div.CourseCardstyle__PriceBox-sc-ohrux3-8.gFCcKC strong.CourseCardstyle__Result-sc-ohrux3-11.iROISk')
            price = price_element.text.strip()
            if price == "무료":
                price = 0
            else:
                price = re.sub(r'[^0-9]', '', price)


            # field
            field = i+1
            
            
            #count
            count+=1
            count_all += 1


            item_obj = {
                'lesson_title': lesson_title,
                'site_url': course_link,
                'image' : code_image,
                'price': price,
                'field': field,
            }

            result.append(item_obj)

            """
            # 크롤링한 데이터를 콘솔에 출력
            print("Lesson Title:", lesson_title)
            print("Image:", code_image)
            print("Site URL:", course_link)
            print("Price:", price)
            print("Field:", field)
            print("Count:", count)
            print("-------------------------------")
            """
        all_results.append(result)


    # Selenium이 사용한 브라우저를 닫습니다.
    driver.quit()
    return all_results

if __name__ == '__main__':
    data_dict = get_all_results()
    
    for result_list in data_dict:
        for dic in result_list:
            n = dic['lesson_title']
            u = dic['site_url']
            img = dic['image']
            p = dic['price']
            f = dic['field']
            
            Post(lesson_title=n, site_url=u, image=img, price=p, field=f).save()



