import streamlit as st 
from dataloader import UrlList
from preprocessing import get_webpage_title 
import pandas as pd 

st.set_page_config(page_title = "Search" , page_icon = "📌" , layout = 'wide')

#st.seesion_state에 저장되지 않으면, 매 페이지 새로고침마다 url_list 객체가 초기화
if "url_list" not in st.session_state :
    st.session_state.url_list = UrlList()
      
with st.sidebar : 
    
    def clear_text() :
        st.session_state['text'] = ""
    
    if "visibility" not in st.session_state :
        st.session_state.visibility = 'visible' 
        st.session_state.disabled = False 
        #st.session_state.placeholder = "URL 주소를 입력해주세요."
        
    text_input = st.text_input(
        "URL을 입력해주세요 👇🏻" , 
        label_visibility = st.session_state.visibility , 
        #placeholder = st.session_state.placeholder , 
        disabled = st.session_state.disabled,
        key = "text"
    )
    
    if text_input :
        #html로 url 받아오는 경우 url_list return
        url_li = st.session_state.url_list.url_input(text_input)
        
        url_title = get_webpage_title(text_input)
        st.write('입력된 URL : ', url_title)
        st.button("clear text input" , on_click = clear_text)
    
    uploaded_file = st.file_uploader('파일을 선택하세요 🗂️') 
    
    if uploaded_file is not None:
        
        #html로 url 받아오는 경우 url_list return
        url_li = st.session_state.url_list.html_input(uploaded_file)        
            
        st.write('업로드 파일명 :' , uploaded_file.name)
    
map = st.session_state.url_list.url_title_mapping()
# st.write(list(map.keys()))
# st.write(list(map.values()))
     
data_df = pd.DataFrame(
    {
        "title" : list(map.keys()),
        "url" : list(map.values()),
        "summary" : list(map.keys()),
    }
)

st.title("📌 BOOKMARK SUMMARY") 

st.data_editor(
    data_df,
    column_config={
        "title": st.column_config.TextColumn(
            "Title",
            disabled = True, #데이터를 읽기 전용으로 설정 
        ),
        "url": st.column_config.LinkColumn(
            "URL",
            display_text=None,
            disabled = True ),
        
        "summary" : st.column_config.TextColumn(
            'Summary' , 
            disabled = True,
        )
    },
    hide_index=False
)


