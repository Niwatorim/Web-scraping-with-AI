import asyncio
from crawl4ai import *
from bs4 import BeautifulSoup

async def scrape():
    """Scrape the website for hadiths"""
    browser_config = BrowserConfig(verbose=True)
    run_config = CrawlerRunConfig(
        excluded_tags=['form', 'header', 'footer'],  # Filter out unnecessary tags
        exclude_external_links=True,  # Exclude external links
        process_iframes=True,  # Process iframes
        remove_overlay_elements=True,  # Remove overlay elements
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://sunnah.com/bukhari/1",  # URL to scrape
            config=run_config
        )
        
        if result.success:
            # Parse the HTML content
            soup = BeautifulSoup(result.html, 'html.parser')
            # Extract all English hadiths
            hadiths = [h.get_text(" ", strip=True) for h in soup.find_all('div', class_='english_hadith_full')]
            print('Page scraped')  # Dev message
            return hadiths  # Return list of hadith texts
        else:
            print('Error: Scraping failed')
            return []  # Return empty list if scraping fails

def splitter(content, max_length=6000):
    """Split content into chunks of max_length characters"""
    chunks = []
    current_chunk = []
    current_length = 0

    for hadith in content:
        hadith_length = len(hadith)
        if current_length + hadith_length > max_length:
            # Add the current chunk to the list
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(hadith)
        current_length += hadith_length

    if current_chunk:
        # Add the last chunk if it exists
        chunks.append(" ".join(current_chunk))
    
    return chunks