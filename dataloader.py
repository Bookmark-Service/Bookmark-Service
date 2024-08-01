from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import PlaywrightURLLoader , SeleniumURLLoader


def get_domain_from_url(url):
    
    parsed_url = urlparse(url)
    parser_url = str(parsed_url.netloc)
    return parser_url  # 도메인 부분을 반환

def get_webpage_title(url):
    try : 
        # URL을 통해 웹페이지 내용 가져오기
        response = requests.get(url)
        
        # 요청에 성공했는지 확인
        if response.status_code != 200:
            return get_domain_from_url(url)
            #return "URL 요청에 실패했습니다"
        
        # 웹 페이지의 인코딩 추출
        # 만약 웹 페이지의 HTML에서 메타 태그로 인코딩 정보를 제공하고 있으면
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_tag = soup.find('meta', attrs={'charset': True})
        
        if meta_tag:
            encoding = meta_tag['charset']
        else:
            # 인코딩을 기본값으로 설정 
            encoding = 'utf-8'
        
        # 응답의 인코딩을 수동으로 설정
        response.encoding = encoding
        
        # 다시 BeautifulSoup 객체 생성
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # title 태그를 찾고, 만일 있으면 반환
        title_tag = soup.find('title')
        if title_tag and title_tag.string:
            return title_tag.string.strip()
        
        # og:title 메타 태그 찾기
        og_title_tag = soup.find('meta', property='og:title')
        if og_title_tag and og_title_tag.get('content'):
            return og_title_tag['content'].strip()
        
        # title이 발견되지 않을 경우 도메인 주소 반환
        return get_domain_from_url(url)

    except Exception as e:
        # 기타 예외 발생 시 도메인 주소 반환 
        return get_domain_from_url(url)

# #page 내용 가져오기 
# async def page_content(urls) : 
    
#     urls = urls 
#     loader = PlaywrightURLLoader(urls = urls ,
#                                remove_selectors=["header", "footer", ".sidebar", 
#                                                 ".advertisement", ".comments",".another_category",
#                                                 ".tags",".related-posts",".tt_box_namecard"])
#     data = await loader.load()
#     return data

def page_content(urls) : 
    loader = SeleniumURLLoader(urls=urls)
    docs = loader.load()
    return docs 