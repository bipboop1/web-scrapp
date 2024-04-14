import requests
from bs4 import BeautifulSoup

def get_text_from_url(url):
	# Sending a request to the URL
	response = requests.get(url)
	if response.status_code == 200:
		# Parsing the HTML content of the page with BeautifulSoup
		soup = BeautifulSoup(response.text, 'html.parser')
		# Extracting all text from the page
		text = soup.get_text(separator='\n', strip=True)
		return text
	else:
		return "Failed to retrieve the webpage"

# Example usage
url = 'http://example.com'  # Replace with the URL of the site you want to scrape
text = get_text_from_url(url)
print(text)

with open("Output.txt", "w") as text_file:
	print(f"scrapped text:\n{text}", file=text_file)
