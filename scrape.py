from bs4 import BeautifulSoup
import requests
import os


def download_image(img_url, filename):
    response = requests.get(img_url, stream=True)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(8192):
            file.write(chunk)

# Check if 'images' folder exists. If not, create it.
if not os.path.exists('images'):
    os.makedirs('images')

# Read URLs from urls.txt file
with open('urls.txt', 'r') as file:
    urls = file.readlines()

# Loop over each URL and scrape images
for url in urls:
    url = url.strip()  # Remove any extra spaces and newline characters
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image tags
    images = soup.find_all('img')

    # Loop over each image, get the image source URL, and download it.
    for img in images:
        img_url = img['src']
        
        # Some image URLs might be relative. Handle those cases by joining with the base URL.
        if not img_url.startswith(("data:image", "http", "https")):
            img_url = "https:" + img_url  # Add https: to start if it's missing
            
        # Create filename from the image URL
        filename = os.path.join('images', os.path.basename(img_url))
        download_image(img_url, filename)
