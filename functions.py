import sys
import time
import os
from termcolor import colored
import undetected_chromedriver as uc
from py_imessage import imessage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
import pytesseract
import requests
from io import BytesIO
from selenium.common.exceptions import TimeoutException

def clean_text(text: str) -> str:
    """
    Extracts the code from the text that starts with 'FREE4FREE'
    """
    for word in text.split():
        if word.startswith("FREE4FREE"):
            return word
    return ""

def get_current_time() -> str:
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time

def get_latest_tweet(driver: uc.Chrome, TWEET_XPATH: str, hashtag: str) -> str:
    try:
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, TWEET_XPATH)))
        tweets = driver.find_elements(By.XPATH, TWEET_XPATH)
        for tweet in tweets:
            if hashtag.lower() in tweet.text.lower():
                return tweet.text
    except TimeoutException:
        print("Failed to find tweet within the timeout period.")
    return ""

def download_image(driver: uc.Chrome, tweet_element) -> Image:
    img_element = tweet_element.find_element(By.XPATH, './/img[contains(@src, "media")]')
    img_url = img_element.get_attribute("src")
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    return img

def extract_code_from_image(image: Image) -> str:
    text = pytesseract.image_to_string(image)
    code = clean_text(text)
    return code

def loop_twitter_page(driver: uc.Chrome, TWEET_XPATH: str, IMAGE_XPATH: str, last_tweet: str, hashtag: str) -> str:
    i = 1
    while True:
        driver.refresh()
        WebDriverWait(driver, 25).until(EC.visibility_of_element_located((By.XPATH, TWEET_XPATH)))
        tweets = driver.find_elements(By.XPATH, TWEET_XPATH)
        print(f"DRIVER IS RUNNING, TIMES REFRESHED: {i}", end='\r')
        sys.stdout.flush()
        i += 1
        
        for tweet in tweets:
            tweet_text = tweet.text
            if tweet_text != last_tweet and hashtag.lower() in tweet_text.lower():
                print("")
                last_tweet = tweet_text
                image = download_image(driver, tweet)
                code = extract_code_from_image(image)

                if code:
                    print(f"Code found at {get_current_time()} ({code})")
                    return code
                else:
                    print("No code found")

def countdown(i = 25):
    for _ in range(i):
        print(f"Restarting in {i} seconds, CTRL + C to cancel ", end='\r')
        sys.stdout.flush()
        i -= 1
        time.sleep(1)
    os.system("clear")

def send_text(code: str) -> str:
    imessage.send("888222", code)
    return f"Text sent at {get_current_time()}! ({code})\nPlease check your phone"

def title():
    title_ascii = ''' 
Waiting for tweet in the next 60 seconds
'''
    print(colored(title_ascii, "green"))
