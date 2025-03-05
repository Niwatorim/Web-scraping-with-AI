#Tried originally doing this with streamlit but had problems with event loop, so I did not use it
import streamlit as st
from singlepage import scrape, splitter
from AI_response import sort
import asyncio

async def main_async_workflow():
    """Handle all async operations"""
    st.write('Finding Hadith')
    content = await scrape()  # Scrape content
    chunks = splitter(content)  # Split into chunks
    return await sort(prompt, chunks)  # Process with AI

# Streamlit app title
st.title('Sunnah Scraper')

# User input for the topic
prompt = st.text_input('What topic do you want a hadith for')

# Button to trigger the search
if st.button('Find'):
    if prompt:
        # Run async workflow
        result = asyncio.run(main_async_workflow())
        st.write(result)  # Display the result
    else:
        st.warning("Please enter a topic.")  # Warn if no topic is entered