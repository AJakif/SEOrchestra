import pytest
from unittest.mock import AsyncMock, patch
from audit_agent.src.core.crawler import WebsiteCrawler

@pytest.mark.asyncio
async def test_crawler_initialization():
    """Test that the crawler initializes with correct defaults"""
    crawler = WebsiteCrawler()
    assert crawler.max_pages == 50
    assert crawler.timeout == 10
    assert crawler.visited_urls == set()
    assert crawler.to_visit == []

@pytest.mark.asyncio
async def test_extract_links():
    """Test link extraction from HTML content"""
    crawler = WebsiteCrawler()
    html = """
    <html>
        <body>
            <a href="/page1">Page 1</a>
            <a href="/page2">Page 2</a>
            <a href="https://external.com">External</a>
        </body>
    </html>
    """
    
    base_url = "https://example.com"
    links = crawler.extract_links(html, base_url)
    
    assert len(links) == 2  # Only internal links
    assert "https://example.com/page1" in links
    assert "https://example.com/page2" in links
    assert "https://external.com" not in links

@pytest.mark.asyncio
@patch('aiohttp.ClientSession.get')
async def test_fetch_page_success(mock_get):
    """Test successful page fetch"""
    mock_get.return_value.__aenter__.return_value.text = AsyncMock(return_value="<html>test</html>")
    
    crawler = WebsiteCrawler()
    await crawler.init_session()
    
    result = await crawler.fetch_page("https://example.com")
    assert result == "<html>test</html>"
    
    await crawler.close_session()

@pytest.mark.asyncio
@patch('aiohttp.ClientSession.get')
async def test_fetch_page_failure(mock_get):
    """Test page fetch failure"""
    mock_get.side_effect = Exception("Connection error")
    
    crawler = WebsiteCrawler()
    await crawler.init_session()
    
    result = await crawler.fetch_page("https://example.com")
    assert result == ""
    
    await crawler.close_session()