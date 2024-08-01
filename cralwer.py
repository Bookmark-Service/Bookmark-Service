from bs4 import BeautifulSoup
from preprocessing import get_webpage_title

class UrlList() : 

    #초기값 설정 
    def __init__(self):
        self.url_list = []
        self.url_title_map = {}
        

    #txt input으로 받아올 경우 
    def url_input(self, url) :
        
        if url not in self.url_list :
            self.url_list.append(url)
        
        return self.url_list

    #html 파일을 업로드 할 경우 
    def html_input(self, file) :

        f_content = file.getvalue().decode('utf-8')
        soup  = BeautifulSoup(f_content , 'html.parser')
        
        #북마크 url 추출
        urls = [a['href'] for a in soup.find_all('a' , href = True)]
        https_url = [link for link in urls if link.startswith('https')]

        self.url_list.extend(https_url) #url_list에 html list 추가 
        self.url_list = list(set(self.url_list)) #중복 URL 제거 

        return self.url_list 
    
    #title에 url mappling 하는 코드
    #title이 같을 경우 어떻게 처리할지 추가 코드 작성해야함. 
    def url_title_mapping(self ) : 
        
        for url in self.url_list : 
            title = get_webpage_title(url)
            self.url_title_map[title] = url
        return self.url_title_map
