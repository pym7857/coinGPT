import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
#options.add_argument("user-data-dir=C:\\Users\\yourusername\\AppData\\Local\\Google\\Chrome Beta\\User Data")
options.add_argument("profile-directory=Default")

driver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=driver_service, options=options)

results_txt = ''

try:
    link = 'https://twitter.com/elonmusk'
    driver.get(link)

    tweet_text_elements = []

    # Scroll 5 times to load more tweets
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2) 

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all elements with 'tweetText'
        tweet_text_elements.extend(soup.find_all('div', {'data-testid': 'tweetText'}))

    # first 10 tweet
    for i, tweet_text_element in enumerate(tweet_text_elements[:10]):
        tweet_text = tweet_text_element.text.strip().replace("\n", "")
        print(f"Tweet {i+1}: {tweet_text}")
        results_txt += f"✅ Tweet {i+1}: {tweet_text} \n"

finally:
    with open(os.path.join('outputs', f'twitter_test.txt'), 'w') as file:
        file.write(str(results_txt))
    # driver.Quit()