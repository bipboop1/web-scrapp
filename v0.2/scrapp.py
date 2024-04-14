import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import random

def is_valid_url(url):
	# Check if URL is valid and not an internal link or a javascript link
	parsed = urlparse(url)
	return bool(parsed.netloc) and bool(parsed.scheme) and not url.startswith("javascript:")

def fetch_html(url, retries=3, backoff_factor=0.5):
    """Attempt to get HTML content of a page with retries and exponential backoff."""
    for i in range(retries):
        try:
            response = requests.get(url, timeout=10)  # 10 seconds timeout
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response
        except (requests.RequestException, requests.HTTPError) as e:
            print(f"Request failed: {e}, retrying ({i+1}/{retries})...")
            time.sleep(backoff_factor * (2 ** i))  # Exponential backoff
    print("Failed to fetch page after several retries.")
    return None

def get_all_website_links(url, domain_name, visited):
	# Fetch the HTML content
	response = fetch_html(url)
	if not response:
		return visited

	# Initialize BeautifulSoup
	soup = BeautifulSoup(response.text, 'html.parser')
	
	# Get all HTML <a> tags
	for a_tag in soup.findAll("a"):
		href = a_tag.get('href')
		if href:
			# Join relative URLs with the base URL
			href = urljoin(url, href)
			if domain_name in href and href not in visited and is_valid_url(href):
				visited.add(href)
				print("Visiting:", href)
				time.sleep(random.randint(8, 12))
				# Recursively visit all links
				get_all_website_links(href, domain_name, visited)
	return visited

def scrape_text_from_urls(urls):
	all_text = []
	for url in urls:
		response = fetch_html(url)
		if response:
			soup = BeautifulSoup(response.text, 'html.parser')
			text = soup.get_text(separator='\n', strip=True)
			all_text.append(text)
		time.sleep(random.randint(10, 20))
	return all_text

# Starting URL
start_url = 'http://example.com'  # Replace with the actual URL
domain_name = urlparse(start_url).netloc  # Extracts domain to stay within the same site

# Collect all unique URLs from the website
visited_urls = get_all_website_links(start_url, domain_name, set())

# Extract text from each URL
texts = scrape_text_from_urls(visited_urls)
for text in texts:
	print(text[:1000])  # Print the first 1000 characters of text from each page
