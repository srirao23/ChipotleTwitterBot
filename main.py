import os
from functions import get_latest_tweet, loop_twitter_page, send_text, countdown, title, download_image
import undetected_chromedriver as uc

if __name__ == "__main__":
    TWEET_XPATH = '//article[@data-testid="tweet"]'
    IMAGE_XPATH = './/img[contains(@src, "media")]'
    
    while True:
        title()
        print("Starting...")
        driver = uc.Chrome(headless=True)
        driver.get("https://twitter.com/ChipotleTweets")

        latest_tweet = get_latest_tweet(driver, TWEET_XPATH, "#FreeThrowsFreeCodes")
        os.system("clear")
        title()
        code = loop_twitter_page(driver, TWEET_XPATH, IMAGE_XPATH, latest_tweet, "#FreeThrowsFreeCodes")
        resp = send_text(code)
        driver.quit()

        print(resp)
        countdown()
