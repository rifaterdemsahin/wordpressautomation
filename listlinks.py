import requests
from requests.auth import HTTPBasicAuth
import logging

# Configuration
USERNAME = ''
PASSWORD = ''
KEYWORD = 'contractor'
OUTPUT_FILE = r'C:\Users\Pexabo\Desktop\wpautomate\post_links.txt'
WORDPRESS_URL = "https://public-api.wordpress.com/wp/v2/sites/rifaterdemsahin.com/posts"
POSTS_PER_PAGE = 100  # Adjust this according to the API limit, usually it's 10 or 100

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def fetch_all_posts_with_keyword(keyword, per_page):
    all_posts = []
    page = 1
    while True:
        try:
            url = f"{WORDPRESS_URL}?search={keyword}&per_page={per_page}&page={page}"
            logger.info(f"Request URL: {url}")
            response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
            logger.info(f"Response Status Code: {response.status_code}")

            if response.status_code != 200:
                logger.error(f"Request failed with status code: {response.status_code}")
                break

            # Check if the response content type is JSON
            if response.headers.get('Content-Type') != 'application/json; charset=UTF-8':
                logger.error(f"Unexpected Content-Type: {response.headers.get('Content-Type')}")
                logger.error(f"Response Content: {response.text}")
                break

            # Attempt to parse JSON
            posts = response.json()
            if not posts:
                break
            all_posts.extend(posts)
            logger.info(f"Fetched {len(posts)} posts from page {page}")
            page += 1
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            break
        except requests.exceptions.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            logger.error(f"Response Content: {response.text}")
            break
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            break
    return all_posts

def write_text_to_file(filename, text):
    try:
        with open(filename, 'w') as file:
            file.write(text)
        logger.info(f"Successfully wrote text to {filename}")
    except Exception as e:
        logger.error(f"Failed to write text to file: {e}")

def main():
    logger.info("Script started")
    posts = fetch_all_posts_with_keyword(KEYWORD, POSTS_PER_PAGE)
    if posts:
        logger.info(f"Successfully fetched {len(posts)} posts with keyword '{KEYWORD}'")
        post_links = "\n".join([post['link'] for post in posts])
        
        # Write post links to the file
        write_text_to_file(OUTPUT_FILE, post_links)
    else:
        logger.error("Failed to fetch posts")

if __name__ == "__main__":
    main()
