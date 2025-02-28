import streamlit as st
from scrape import scrape, extract_body, cleaning, splittingcontent
from parse import parse_ollama

st.title('Webscraper') 
url = st.text_input('Enter Website URL: ')


if st.button('Scrape Site'):
    st.write('scraping the website')
    result = scrape(url) #runs scrape website as per scrape.py (via selenium)
    #result has just the html
    #the above will open the website for 10 seconds then return all the html
    

    #cleaning the html:
    body = extract_body(result)
    cleaned = cleaning(body)

    st.session_state.dom_content = cleaned

    with st.expander('View DOM Content'):
        st.text_area('DOM CONTENT', cleaned, height=300)


if 'dom_content' in st.session_state: #if any content saved in the session
    description = st.text_area('Describe what you want to parse') # prompt appears
    
    if st.button('parse content'): #if the button clicked
        if description:
            st.write('parsing content')

            chunks = splittingcontent(st.session_state.dom_content)
            result = parse_ollama(chunks, description)
            st.write(result)

            

