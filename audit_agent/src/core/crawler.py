import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Set
import time

class WebsiteCrawler:
    def __init__(self, max_pages: int = 50, timeout: int = 10):
        self.max_pages = max_pages
        self.timeout = timeout
        self.visited_urls: Set[str] = set()
        self.to_visit: List[str] = []
        self.session = None
        
    async def init_session(self):
        self.session = aiohttp.ClientSession()
        
    async def close_session(self):
        if self.session:
            await self.session.close()
            
    async def fetch_page(self, url: str) -> str:
        try:
            async with self.session.get(url, timeout=self.timeout) as response:
                return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return ""
            
    def extract_links(self, html: str, base_url: str) -> List[str]:
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(base_url, href)
            
            # Only include links from the same domain
            if urlparse(absolute_url).netloc == urlparse(base_url).netloc:
                links.append(absolute_url)
                
        return links
        
    async def crawl(self, start_url: str) -> Dict[str, str]:
        if not self.session:
            await self.init_session()
            
        self.to_visit = [start_url]
        self.visited_urls = set()
        pages_content = {}
        
        while self.to_visit and len(pages_content) < self.max_pages:
            url = self.to_visit.pop(0)
            
            if url in self.visited_urls:
                continue
                
            print(f"Crawling: {url}")
            self.visited_urls.add(url)
            
            html = await self.fetch_page(url)
            if not html:
                continue
                
            pages_content[url] = html
            
            # Extract links from the page
            new_links = self.extract_links(html, url)
            for link in new_links:
                if link not in self.visited_urls and link not in self.to_visit:
                    self.to_visit.append(link)
            
            # Be polite with a small delay
            await asyncio.sleep(0.1)
            
        await self.close_session()
        return pages_content