# 인프런 크롤링
import time
import schedule
import re
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import os
# Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록한다.
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
# import django
# 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만든다.
# django.setup()

from posts.models import Post


def get_inflearn_results():
    driver = webdriver.Chrome()

    # 검색할 키워드
    search_text = ["Django", "React", "Spring","C언어", "Python", "Java"]

    count_all = 0
    all_results = []

    for i in range(len(search_text)):
        # 크롬드라이버로 원하는 url로 접속
        url = 'https://www.inflearn.com/'
        driver.get(url)
        time.sleep(3)  # 페이지 로딩을 위해 3초간 기다림.

        # 검색창에 키워드 입력 후 엔터
        element = driver.find_element(By.XPATH, '//*[@id="pg___main"]/section[2]/div/div/div/input')
        element.send_keys(search_text[i])
        element.send_keys(Keys.ENTER)

        result = []
        time.sleep(10)
        list_items = driver.find_elements(By.CSS_SELECTOR,'div.column.is-3-fullhd.is-3-widescreen.is-3-desktop.is-4-tablet.is-6-mobile')

        count = 0

        for item in list_items:
            
            # lesson_title
            lesson_title = item.find_element(By.CSS_SELECTOR, 'div.course_title').text
            if 'Javascript' in lesson_title or '자바스크립트' in lesson_title:
                break

            # image_url
            image_tag = item.find_element(By.CSS_SELECTOR, 'div.card-image img')
            code_image = image_tag.get_attribute('src')


            # site_url
            course_link = item.find_element(By.CSS_SELECTOR, 'a.course_card_front.e_course_click').get_attribute('href')
            if course_link:
                course_link
            else:
                course_link = None


            # price
            price_elem = item.find_element(By.CSS_SELECTOR, 'div.price')
            try:
                price_low_elem = price_elem.find_element(By.CSS_SELECTOR, 'span.pay_price')
                price_text = price_low_elem.text
            except NoSuchElementException:
                price_text = price_elem.text
                
            if price_text.strip().lower() == "무료":
                price = 0
            else:
                price = re.sub(r'[^0-9]', '', price_text)
            
            
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

        all_results.append(result)
        # print("Count:", count)


    # Selenium이 사용한 브라우저를 닫습니다.
    driver.quit()

    #print("총 갯수:", count_all) # sum(len(result) for result in all_results)) 동일
    #print(all_results)
    return all_results

"""
if __name__ == '__main__':
    data_dict = get_inflearn_results()

    for result_list in data_dict:
        for dic in result_list:
            n = dic['lesson_title']
            u = dic['site_url']
            img = dic['image']
            p = dic['price']
            f = dic['field']
                
            # 이미 존재하는 데이터인지 확인 후 저장
            if not Post.objects.filter(lesson_title=n, site_url=u, image=img, price=p, field=f).exists():
                Post(lesson_title=n, site_url=u, image=img, price=p, field=f).save()
"""