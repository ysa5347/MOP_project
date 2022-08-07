from datetime import datetime
from re import M
from .models import Portal, Dept, Staff, Keyword
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

def PortalCrowling():

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
    
    title, dept, writer, date, pk, kwd = [], [], [], [], [], []
    driver.execute_script('window.open("https://portal.gist.ac.kr/p/EXT_LNK_BRD/?boardId=1");')

    while(i):
        print(f'_____________for {i} in 10_______________')
        driver.switch_to.window(driver.window_handles[-1])
        driver.switch_to.frame("body_frame")
        sleep(1)
        print(driver.current_url)

        html = driver.page_source
        f = open(f'/Users/yoon.jh/Desktop/MOP_project/project/crowling/example/exammple{i}.html', 'w')
        f.write(html) 
        f.close
        
        # 각 항목 parsing 및 Data화
        soup = bs(html, 'html.parser') # BeautifulSoup사용하기
        for j in range(20):
            _title = soup.select('tbody > tr > td.bc-s-txtval > div > span')[j].text
            _dept = soup.select('tbody > tr > td.bc-s-cre_user_dept_name')[j].text
            _writer = soup.select('tbody > tr > td.bc-s-cre_user_name')[j].text
            _date = soup.select('tbody > tr > td.bc-s-cre_dt')[j].text
            _pk = int(soup.select('tbody > tr')[j].attrs['data-url'].split('=')[-1])
            print(f'-------for {j + 1} in 20 --------')
            if not Portal.objects.filter(pk=_pk).exists():
                print("---------------Post is not in DB------------------")
                title.append(_title)
                dept.append(_dept)
                writer.append(_writer)
                date.append(_date)
                pk.append(_pk)

                # dept 존재 유무 판별
                if not Dept.objects.filter(name=_dept).exists():
                    print('_______in if______')
                    newDept = Dept(name=_dept)
                    newDept.save()
                # writer 존재 유무 판별
                if not Staff.objects.filter(dept=_dept, name=_writer).exists():
                    driver.switch_to.window(driver.window_handles[-2])
                    driver.switch_to.frame('portletIframe')
                    search_box = driver.find_element_by_css_selector('#AjaxPtlBodyeXPortal_PtlPe041Portlet__9rt5ab_3_ > div > div > div.eXPortal_PtlPe041Portlet__9rt5ab_3_InputArea > ul > li:nth-child(1) > input')

                    search_box.clear()
                    search_box.send_keys(_writer)
                    sleep(0.5)
                    search_box.send_keys(Keys.ENTER)

                    # driver.find_element_by_css_selector('div.portlet-body > div > #AjaxPtlBodyeXPortal_PtlPe041Portlet__9rt5ab_3_ > div > div > div.eXPortal_PtlPe041Portlet__9rt5ab_3_InputArea > ul > li:nth-child(2) > input[type=image]').click()

                    # tempStaffInfo list 접근 다시 보기
                    html2 = driver.page_source
                    soup2 = bs(html2, 'html.parser')
                    tempStaffInfo = soup2.select('#AjaxPtlBodyeXPortal_PtlPe041Portlet__9rt5ab_3_ > div > div > div.board_area3 > table > tbody > tr > td')
                    
                    if len(tempStaffInfo) == 0:         # 만약 검색되지 않는다면 -> 퇴사
                        newStaff = Staff(name=_writer, dept=Dept.objects.get(name=_dept), exNum=None, stat='퇴사', email=None)
                        newStaff.save()
                    else:                               # 교직원 검색
                        # case report: 작성자 소속과, 게시글 소속이 다른 경우가 있음.(_dept는 게시글 소속, tempStaffInfo[0]은 작성자 소속.) 
                        # 그러나 동명이인이 존재할 수 있고, 이 경우 동명이인 중 게시글 소속과 동일한 소속을 우선하고, 동명이인이 있더라도 게시글과 동일한 소속이 없다면, 사실관계 확인 후 수동 부여를 위해 None로 설정한다.
                        for k in range(len(tempStaffInfo) // 5):
                            _exNum = tempStaffInfo[5*k+2]
                            _email = tempStaffInfo[5*k+3]
                            if tempStaffInfo[5*k] == _dept:
                                newStaff = Staff(name=_writer, dept=Dept.objects.get(name=_dept), exNum=_exNum, email=_email)
                                newStaff.save()
                                break
                                # 게시글과 동일한 소속인 사람이 없다. -> 사람은 공란으로 둔다.

                _dept = Dept.objects.get(name=_dept)
                try:
                    _writer = Staff.objects.get(name=_writer)
                except:
                    _writer = None

                portalPost = Portal(title=_title, dept=_dept, writer=_writer, date=_date, pk=_pk)
                portalPost.save()

            driver.switch_to.window(driver.window_handles[-1])
            driver.switch_to.frame("body_frame")

        
        
        # 다음 페이지 탐색
        driver.switch_to.window(driver.window_handles[-1])
        driver.switch_to.frame("body_frame")
        sleep(1)
        next = driver.find_elements_by_css_selector(f'#bi_cont_middle > div:nth-child(6) > div > div > div > a:nth-child({i+3})')
        
        next[0].click()

        # driver.switch_to.window(driver.window_handles[-1])
        # driver.switch_to.frame("body_frame")
        i += 1
        
        if i == 10:
            break
    
    
    if len(pk) != 0:
        msg = f'{datetime.now().strftime("%Y/%m/%d - %H/%M/%S")} 기준, 새로운 게시글은 아래와 같습니다.\n---------------------------------------------\n'
        for l in range(len(pk)):
            msg += f'{title[l]} | {dept[l]} | {writer[l]} [{pk[l]}]\n'
        msg += '---------------------------------------------'
    else:
        msg = 'No update!'

    print(msg)
    file = open(f'/Users/yoon.jh/Desktop/MOP_project/project/crowling/example/{datetime.now().strftime("%Y%m%d")}output_textfile.txt','w')
    file.write(msg)
    file.close

    return msg
    # 키워드 구현 필요
    # 유효성 검사 필요


# 교직원 db 갱신
def checkStaff():
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


    driver.switch_to.frame('portletIframe')
    sleep(1)
    print(driver.current_url)

    staffObjects = Staff.objects.all()
    n = len(staffObjects)
    for obj in staffObjects:
        search_box = driver.find_element_by_css_selector('#AjaxPtlBodyeXPortal_PtlPe041Portlet__9rt5ab_3_ > div > div > div.eXPortal_PtlPe041Portlet__9rt5ab_3_InputArea > ul > li:nth-child(1) > input')

        search_box.clear()
        search_box.send_keys(obj.name)
        sleep(0.5)
        search_box.send_keys(Keys.ENTER)

        # tempStaffInfo list 접근 다시 보기
        html = driver.page_source
        soup = bs(html, 'html.parser')
        tempStaffInfo = soup.select('#AjaxPtlBodyeXPortal_PtlPe041Portlet__9rt5ab_3_ > div > div > div.board_area3 > table > tbody > tr > td')

        if len(tempStaffInfo) == 0:         # 만약 검색되지 않는다면 -> 퇴사
            obj.stat, obj.email, obj.exNum = '퇴사', None, None
            
        else:
            obj.stat = '재직'

        obj.save()


        
