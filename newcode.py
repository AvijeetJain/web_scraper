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

def click_all_read_more_buttons(driver):
    read_more_buttons = driver.find_elements(By.CLASS_NAME, '_1BWGvX')

    for button in read_more_buttons:
        try:
            # Scroll into view using ActionChains
            actions = ActionChains(driver)
            actions.move_to_element(button).perform()
            
            # Click the element using Selenium
            button.click()
            print("-> Button CLICKED")
            
        except Exception as e:
            print(f"Error clicking 'READ MORE' button: {e}")

        # Wait for the expanded text to load (adjust the time accordingly)
        time.sleep(3)

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

def get_full_review(review_elem, driver, block):
    full_review_elem = block.find('div', {'class': 't-ZTKy'})
    print(full_review_elem.text.strip())
    return full_review_elem.text.strip() if full_review_elem else review_elem.text.strip()

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

# def main():
#     # URL of the page to scrape
#     url = "https://www.flipkart.com/harry-potter-philosopher-s-stone/product-reviews/itmfc5dhvrkh5jqp?pid=9781408855652&lid=LSTBOK9781408855652OQYZXT&marketplace=FLIPKART"

#     # Set the desired page number
#     desired_page = 2
#     page_url = url + "&page=" + str(desired_page)
    
#     # Open the browser and fetch the page
#     driver = webdriver.Chrome()  # Make sure to have the ChromeDriver installed
#     driver.get(page_url)

#     # Click all "Read More" buttons on the page
#     click_all_read_more_buttons(driver)

#     # Fetch the updated HTML content
#     soup = BeautifulSoup(driver.page_source, "html.parser")

#     # Scrape reviews from the desired page
#     page_reviews = cus_rev(soup, driver)
#     # print(page_reviews)

#     save_reviews_to_csv(page_reviews, 'reviews2.csv')
#     # Close the browser after scraping
#     driver.quit()
    
def main():
    # URL of the page to scrape
    url = "https://www.flipkart.com/harry-potter-philosopher-s-stone/product-reviews/itmfc5dhvrkh5jqp?pid=9781408855652&lid=LSTBOK9781408855652OQYZXT&marketplace=FLIPKART"

    reviews = []
    page = 1
    
    driver = webdriver.Chrome()

    while True:
        page_url = url + "&page=" + str(page)
        driver.get(page_url)
        print(page, "st page is scraping")
        click_all_read_more_buttons(driver)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        page_reviews = cus_rev(soup, driver)
        
        if not page_reviews:
            print(f"No more pages to scrape.")
            break
        
        reviews.extend(page_reviews)
        
        next_button = soup.find('a', {'class': '_1LKTO3'})
        if not next_button:
            print(f"No more pages to scrape.")
            break

        page += 1
        
    driver.quit()

    print(reviews)

    # Save reviews to CSV
    save_reviews_to_csv(reviews, 'reviews.csv')

    # Save all reviews to JSON
    save_reviews_to_json(reviews, 'allReviews.json')

    print("Script completed successfully.")

if __name__ == "__main__":
    main()