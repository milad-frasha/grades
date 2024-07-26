import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Your Telegram bot token
bot_token = '7320885745:AAHkjCwjHR7bzFST6O_hNgxPaulWo2Uyolc'
# Your chat ID
chat_id = '1311416362'

# Function to send message to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message}
    try:
        response = requests.post(url, data=payload)
        logging.info(f"Telegram API status code: {response.status_code}")
        if response.status_code == 200:
            logging.info("Message sent successfully.")
        else:
            logging.error(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
            try:
                response_data = response.json()
                logging.error(f"Error code: {response_data.get('error_code')}")
                logging.error(f"Description: {response_data.get('description')}")
            except ValueError:
                logging.error("Failed to parse response as JSON.")
    except Exception as e:
        logging.error(f"Exception occurred while sending message: {e}")

# Function to fetch and parse the page
def fetch_and_parse_page(url):
    try:
        response = requests.get(url)
        logging.info(f"Fetching page status code: {response.status_code}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        else:
            logging.warning(f"Failed to fetch the page. Status code: {response.status_code}")
    except Exception as e:
        logging.error(f"Exception occurred while fetching the page: {e}")
    return None

# Function to extract the required information from the parsed page
def extract_information(soup):
    try:
        info = soup.find('span', class_="bottom").text.strip()
        return info
    except AttributeError:
        logging.warning("Required information not found on the page.")
        return None

# Main execution flow
base_url = "http://app.hama-univ.edu.sy/StdMark/Student/"
college_id = "?college=1"
base_id = "81907"

# Iterate over all possible combinations for 'xxxx' (0000 to 9999)
for i in range(5000,10000):
    student_id = f"{base_id}{i:04d}"  # Generate student ID with leading zeros
    url = f"{base_url}{student_id}{college_id}"
    logging.info(f"Checking URL: {url}")
    
    soup = fetch_and_parse_page(url)
    if soup:
        info = extract_information(soup)
        if info:
            message = f"Student ID: {student_id}\nInfo: {info}"
            logging.info(f"Message to be sent: {message}")
            send_telegram_message(message)
        else:
            logging.info(f"No relevant information found for student ID: {student_id}")
    else:
        logging.info(f"No page found for student ID: {student_id}")