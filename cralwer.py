from bs4 import BeautifulSoup
# from preprocessing import get_webpage_title
from db import get_db
from models import Bookmark
from sqlalchemy.orm import Session
from datetime import datetime

class UrlList() : 

    #초기값 설정 
    def __init__(self):
        self.url_list = []
        self.url_title_map = {}
        

    #txt input으로 받아올 경우 
    # def url_input(self, url) :
        
    #     if url not in self.url_list :
    #         self.url_list.append(url)
        
    #     return self.url_list
    
    def url_input(self, url, db: Session):
        if url not in self.url_list:
            self.url_list.append(url)
            # DB에 URL이 존재하는지 확인
            bookmark = db.query(Bookmark).filter(Bookmark.url == url).first()
            if not bookmark:
                # DB에 추가
                new_bookmark = Bookmark(
                    url=url,
                    bookmark_name=url.split("//")[-1],  # 의미 있는 이름 또는 타이틀 사용
                    registrant="system",
                    registration_date=datetime.now(),
                    update_date=datetime.now()
                )
                db.add(new_bookmark)
                db.commit()
            else:
                self.url_list.append(bookmark.url)
        return self.url_list

    #html 파일을 업로드 할 경우 
    def html_input(self, file, db: Session) :

        f_content = file.getvalue().decode('utf-8')
        soup  = BeautifulSoup(f_content , 'html.parser')
        
        #북마크 url 추출
        urls = [a['href'] for a in soup.find_all('a' , href = True)]
        https_url = [link for link in urls if link.startswith('https')]

        self.url_list.extend(https_url) #url_list에 html list 추가 
        self.url_list = list(set(self.url_list)) #중복 URL 제거 

        for url in self.url_list:
            bookmark = db.query(Bookmark).filter(Bookmark.url == url).first()
            if not bookmark:
                new_bookmark = Bookmark(
                    url=url,
                    bookmark_name=url.split("//")[-1],
                    registrant="system",
                    registration_date=datetime.now(),
                    update_date=datetime.now()
                )
                db.add(new_bookmark)
        db.commit()

        return self.url_list 
    
    #title에 url mappling 하는 코드
    #title이 같을 경우 어떻게 처리할지 추가 코드 작성해야함. 
    # def url_title_mapping(self ) : 
        
    #     for url in self.url_list : 
    #         title = get_webpage_title(url)
    #         self.url_title_map[title] = url
    #     return self.url_title_map
    
    def url_title_mapping(self, db: Session):
        for url in self.url_list:
            bookmark = db.query(Bookmark).filter(Bookmark.url == url).first()
            if bookmark and bookmark.summary:
                title = bookmark.summary
            else:
                title = get_webpage_title(url)
                if bookmark:
                    bookmark.summary = title
                    db.commit()
            self.url_title_map[title] = url
        return self.url_title_map
