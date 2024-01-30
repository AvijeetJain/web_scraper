# Review Scraper 

## Overview
This web scraping project is designed to extract valuable insights from user reviews on a specific webpage. The target is to collect data related to product reviews, including ratings, textual reviews, reviewer names, dates, review descriptions, and locations (if available). The goal is to provide a comprehensive dataset that can be used for further analysis, sentiment analysis, or any other data-driven tasks related to user reviews.

## Key Objectives
1. **Data Extraction**: Utilize web scraping techniques to extract relevant information from user reviews on a designated webpage.

2. **Automation**: Implement automation using Selenium to interact with the webpage, click on "READ MORE" buttons, and scrape data from multiple pages.

3. **Data Storage**: Save the extracted data in structured formats, such as CSV and JSON, for easy analysis and future reference.

4. **Customization**: Allow for easy customization by providing parameters that users can modify, such as the URL of the target webpage, to adapt the script for different use cases.

## Prerequisites
- Python 3.x
- Libraries: `requests`, `BeautifulSoup`, `selenium`

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Download and install ChromeDriver for Selenium. Make sure to add the executable to your system's PATH. You can download the ChromeDriver using the link : https://chromedriver.chromium.org/downloads (Make sure that the version of the driver matches with your chromium version)
## Customization

- Adjust the url variable in the script to point to the desired product review page.
- Modify the scraping logic or data extraction functions as needed.
- Note that this review scaper is designed to work on flipkart you might need to change the logic to scrape reviews from some other website.

## Contributing

Feel free to open issues or contribute to the project. Pull requests are welcome.

