import requests
import csv
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def html_code(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

# def get_full_review(review_block, driver):
#     read_more_button = review_block.find('button', {'class': '_1BWGvX'})

#     if read_more_button:
#         # Use WebDriverWait to wait for the element to be clickable
#         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, '_1BWGvX'))).click()

#         # Extract the full review content after clicking 'Read More'
#         # full_review_elem = review_block.find('div', {'class': 't-ZTKy'})
#         full_review_elem = driver.find_element_by_css_selector('div[class^="t-ZTKy"]')
#         full_review = full_review_elem.text.strip() if full_review_elem else None

#         return full_review

#     return review_block.text.strip()

def get_full_review(review_elem, driver, block):
    read_more_elem = review_elem.find('span', {'class': '_1BWGvX'})
    print("---------------")
    print(read_more_elem)
    print("---------------")
    if read_more_elem:
        print("READ MORE BUTTON FOUND")
        
        try:
            # Convert the BeautifulSoup element to a Selenium WebElement
            read_more_elem_selenium = driver.find_element(By.CLASS_NAME, '_1BWGvX')
            
            # Scroll into view using ActionChains
            actions = ActionChains(driver)
            actions.move_to_element(read_more_elem_selenium).perform()
            
            # Click the element using Selenium
            read_more_elem_selenium.click()
            print("-> Button CLICKED")
            
        except Exception as e:
            print(f"Error clicking 'READ MORE' button: {e}")
    
        # Wait for the expanded text to load (adjust the time accordingly)
        time.sleep(10)
        
        # Find the element containing the full review text
        # full_review_elem = driver.find_element_by_xpath('//div[@class="t-ZTKy"]/div/div')
        # full_review_elem = block.find('div', {'class': 't-ZTKy'})
        # print(full_review_elem.text.strip())
        
        # full_review_elem = WebDriverWait(block, 10).until(
        #     EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class^="t-ZTKy"]'))
        # )
        # print(full_review_elem.text.strip())
        
        # block_updated = BeautifulSoup(driver.page_source, 'html.parser')
        
        full_review_elem = block.find('div', {'class': 't-ZTKy'})
        # print(full_review_elem.text.strip())
        
        
        # full_review_elem = WebDriverWait(driver, 10).until(
        #     EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class^="t-ZTKy"]'))
        # )
        print(full_review_elem.text.strip())
        
        # TODO: Click all 'READ MORE' buttons on the page and then apply bs4 to extract the full review text
        
        return full_review_elem.text if full_review_elem else review_elem.text


    print("-> READ MORE button not found.")
    return review_elem.text.strip()


def cus_rev(soup, driver):
    reviews = []
    review_blocks = soup.find_all('div', {'class': '_27M-vq'})
    for block in review_blocks:
        rating_elem = block.find('div', {'class': '_3LWZlK'})
        review_elem = block.find('p', {'class': '_2-N8zT'})
        sum_elem = block.find('div', {'class': 't-ZTKy'})
        name_elem = block.find_all('p', {'class': '_2sc7ZR'})[0]
        date_elem = block.find_all('p', {'class': '_2sc7ZR'})[1]
        location_elem = block.find('p', {'class': '_2mcZGG'})
        
        location_text = location_elem.text if location_elem else None

        if rating_elem and review_elem and name_elem and date_elem:
            review_text = get_full_review(sum_elem, driver, block)
            print(review_text)
            review = {
                'Rating': rating_elem.text,
                'Review': review_elem.text.strip(),
                'Name': name_elem.text.strip(),
                'Date': date_elem.text.strip(),
                'Review Description': sum_elem.text.strip(),
                'Location': location_text
            }
            reviews.append(review)
            
        print("---------------------------------------------------------------------")
        print("---------------------------------------------------------------------")
    return reviews


def save_reviews_to_csv(reviews, filename):
    fields = ['Rating', 'Review', 'Name', 'Date', 'Review Description', 'Location']

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
        csvwriter.writeheader()
        csvwriter.writerows(reviews)

    print(f"Reviews written to CSV: {filename}")

def save_reviews_to_json(reviews, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(reviews, json_file, ensure_ascii=False, indent=2)

    print(f"Reviews written to JSON: {filename}")
    
# URL of the page to scrape
url = "https://www.flipkart.com/harry-potter-philosopher-s-stone/product-reviews/itmfc5dhvrkh5jqp?pid=9781408855652&lid=LSTBOK9781408855652OQYZXT&marketplace=FLIPKART"

# Set the desired page number
desired_page = 2
page_url = url + "&page=" + str(desired_page)

# Open the browser and fetch the page
driver = webdriver.Chrome()  # Make sure to have the ChromeDriver installed
driver.get(page_url)

# Fetch the HTML content
soup = BeautifulSoup(driver.page_source, "html.parser")

# Scrape reviews from the desired page
page_reviews = cus_rev(soup, driver)
# print(page_reviews)

save_reviews_to_csv(page_reviews, 'reviews2.csv')
# Close the browser after scraping
driver.quit()
