from re import A
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from time import sleep

title, dept, writer, date, pk = [], [], [], [], []

driver = webdriver.Chrome('/Users/yoon.jh/Desktop/MOP_project/chromedriver')
driver.implicitly_wait(3)
curr_url = ''
driver.get('https://portal.gist.ac.kr/login.jsp')

while(1):
    if(driver.current_url != 'https://portal.gist.ac.kr/login.jsp'):
        break
    driver.find_element_by_name('user_id').send_keys('ysa5347')
    driver.find_element_by_name('user_password').send_keys('jinhyun@@99')
    sleep(1)
    driver.find_element_by_class_name('btn_login').click()
    sleep(3)
    print(driver.current_url)

i = 1
while(i):
    driver.get(f'https://portal.gist.ac.kr/p/EXT_LNK_BRD/?boardId=1')
    driver.switch_to.frame("body_frame")
    sleep(1)
    print(driver.current_url)

    html = driver.page_source
    f = open(f'/Users/yoon.jh/Desktop/MOP_project/project/crowling/example/exammple{i}.html', 'w')
    f.write(html)
    f.close
    
    # 각 항목 parsing 및 db화
    soup = bs(html, 'html.parser') # BeautifulSoup사용하기
    for j in range(20):
        _title = soup.select('tbody > tr > td.bc-s-txtval > div > span')[j].text
        _dept = soup.select('tbody > tr > td.bc-s-cre_user_dept_name')[j].text
        _writer = soup.select('tbody > tr > td.bc-s-cre_user_name')[j].text
        _date = soup.select('tbody > tr > td.bc-s-cre_dt')[j].text
        _pk = int(soup.select('tbody > tr')[j].attrs['data-url'].split('=')[-1])

        title.append(_title), dept.append(_dept), writer.append(_writer), date.append(_date), pk.append(_pk)
    
    print(pk)
    print(len(pk))
    # f = open(f'/Users/yoon.jh/Desktop/MOP_project/project/crowling/example/block{i}.html', 'w')
    # f.write(str(block))
    # f.close
    
    

    # 다음 페이지 탐색
    next = driver.find_elements_by_tag_name('a')
    next[i-1].click()
    i += 1
    
    if i == 3:
        break

