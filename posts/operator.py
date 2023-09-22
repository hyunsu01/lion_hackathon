# posts/operator.py
import sys
import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from django_apscheduler.jobstores import register_events, DjangoJobStore
import time
from .views import *

# 현재 파일의 경로를 가져옴
current_dir = os.path.dirname(os.path.abspath(__file__))
# 프로젝트 루트 디렉토리 경로를 계산
project_root = os.path.abspath(os.path.join(current_dir, '..'))
# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(project_root)

from Goormedu_crawling import get_goormedu_results  # 크롤링 함수 이름 수정
from Inflearn_crawling import get_inflearn_results  # 크롤링 함수 이름 수정
from Programmers_crawling import get_programmers_results # 크롤링 함수 이름 수정


def start():
    scheduler=BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)
    
    # 매일 크롤링 작업을 실행하는 함수 정의
    def daily_crawl():
        
        # 크롤링한 데이터 가져오기
        goormedu_results = get_goormedu_results()
        inflearn_results = get_inflearn_results()
        programmers_results = get_programmers_results()

        # 모든 결과를 하나의 리스트로 합치기
        results = goormedu_results + inflearn_results + programmers_results
        
        # 데이터를 저장하기 전에 이미 있는지 확인하고 저장
        for result_list in results:
            for data_dict in result_list:
                title = data_dict['lesson_title']
                url = data_dict['site_url']
                img = data_dict['image']
                p = data_dict['price']
                f = data_dict['field']

                if not Post.objects.filter(lesson_title=title, site_url=url).exists():
                    Post.objects.create(lesson_title=title, site_url=url, image=img, price=p, field=f)

        # get_goormedu_results()  # 수정된 크롤링 함수 호출
        # get_inflearn_results()  # 수정된 크롤링 함수 호출
        # get_programmers_results()  # 수정된 크롤링 함수 호출

        
    # 매일 자정 (00:00:00)에 작업을 예약합니다.
    scheduler.add_job(daily_crawl, 'cron', hour=0, minute=0, second=0, id='daily_crawl')
    
    # 매 10분마다 실행되도록 설정
    # scheduler.add_job(daily_crawl, 'cron', minute='*/10', id='daily_crawl_10min')
    
    # 매 5분마다 실행되도록 설정
    # scheduler.add_job(daily_crawl, 'cron', minute='*/5', id='daily_crawl_5min')

    # 매 1분마다 실행되도록 설정
    # scheduler.add_job(daily_crawl, 'cron', minute='*', id='daily_crawl_1min')
    
    # 매 15분마다 실행되도록 설정
    # scheduler.add_job(daily_crawl, 'cron', minute='*/15', id='daily_crawl_15min')
    
    # 매일 특정 시각에 작업을 예약합니다.
    # scheduler.add_job(daily_crawl, 'cron', hour=1, minute=33, second=10, id='daily_crawl')

    scheduler.start()