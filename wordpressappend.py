import requests
from requests.auth import HTTPBasicAuth
import logging

# Configuration
WORDPRESS_URL = "https://public-api.wordpress.com/wp/v2/sites/rifaterdemsahin.com/posts"
USERNAME = ''
PASSWORD = ''
KEYWORD = 'canon'
TEXT_TO_APPEND = """
🚀 **Unlock Your Potential with Our New Course: "Mastering DevAIOps: Transform from Solo Expert to Multi-Skilled Contractor"!** 🚀

👩‍💻 Are you a skilled employee looking to elevate your career?  
📈 Do you want to expand your expertise and become a sought-after multi-skilled contractor?  
🌟 Join our **comprehensive course** designed to equip you with the knowledge and tools needed to excel in the rapidly evolving field of IT Contracting.

👉 [**Mastering DevAIOps Course**](https://courses.devops.engineering/courses/oneperson-team-devops) 👈
"""

# Set up logging to console only
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def fetch_posts_with_keyword(keyword):
    try:
        url = f"{WORDPRESS_URL}?search={keyword}"
        logger.info(f"Request URL: {url}")
        response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        logger.info(f"Response Status Code: {response.status_code}")

        # Check if the response content type is JSON
        if response.headers.get('Content-Type') != 'application/json; charset=UTF-8':
            logger.error(f"Unexpected Content-Type: {response.headers.get('Content-Type')}")
            logger.error(f"Response Content: {response.text}")
            return None

        # Attempt to parse JSON
        posts = response.json()
        return posts
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
    except requests.exceptions.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        logger.error(f"Response Content: {response.text}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

    return None

def update_wordpress_post(post_id, updated_content):
    try:
        url = f"{WORDPRESS_URL}/{post_id}"
        logger.info(f"Request URL for updating post: {url}")
        data = {
            'content': updated_content
        }
        response = requests.post(url, json=data, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        logger.info(f"Response Status Code: {response.status_code}")

        if response.status_code == 200:
            logger.info(f"Successfully updated post with ID {post_id}")
        else:
            logger.error(f"Failed to update post: {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

def main():
    logger.info("Script started")
    posts = fetch_posts_with_keyword(KEYWORD)
    if posts:
        logger.info(f"Successfully fetched posts with keyword '{KEYWORD}'")
        
        # Define the content to append
        updated_content = TEXT_TO_APPEND
        
        # Assume you are updating the first post with the fetched content
        if posts:
            post_id = posts[0]['id']
            update_wordpress_post(post_id, updated_content)
    else:
        logger.error("Failed to fetch posts")

if __name__ == "__main__":
    main()
