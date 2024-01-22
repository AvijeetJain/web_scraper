import requests
from bs4 import BeautifulSoup
import json
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def html_code(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def get_full_review(review_block, url):
    read_more_button = review_block.find('button', {'class': '_XVjZLG'})
    
    if read_more_button:
        # Use Selenium to click the 'Read More' button and wait for the content to load
        driver = webdriver.Chrome()  
        driver.get(url)
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, '_XVjZLG'))).click()
        
        full_review_elem = driver.find_element_by_css_selector('div[class^="ooJZfM"]')
        full_review = full_review_elem.text.strip()
        
        driver.quit()  # Close the browser
        
        return full_review

    return review_block.text.strip()

def cus_rev(soup, url):
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
            review = {
                'Rating': rating_elem.text,
                'Review': get_full_review(review_elem, url),
                'Name': name_elem.text.strip(),
                'Date': date_elem.text.strip(),
                'Review Description': sum_elem.text.strip(),
                'Location': location_text
            }
            reviews.append(review)
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

def main():
    # URL of the page to scrape
    url = "https://www.flipkart.com/harry-potter-philosopher-s-stone/product-reviews/itmfc5dhvrkh5jqp?pid=9781408855652&lid=LSTBOK9781408855652OQYZXT&marketplace=FLIPKART"

    reviews = []
    page = 1

    while True:
        page_url = url + "&page=" + str(page)
        print(page, "st page is scraping")
        soup = html_code(page_url)
        page_reviews = cus_rev(soup, url)
        
        if not page_reviews:
            print(f"No more pages to scrape.")
            break
        
        reviews.extend(page_reviews)
        
        next_button = soup.find('a', {'class': '_1LKTO3'})
        if not next_button:
            print(f"No more pages to scrape.")
            break

        page += 1

    print(reviews)

    # Save reviews to CSV
    save_reviews_to_csv(reviews, 'reviews.csv')

    # Save all reviews to JSON
    save_reviews_to_json(reviews, 'allReviews.json')

    print("Script completed successfully.")

if __name__ == "__main__":
    main()
