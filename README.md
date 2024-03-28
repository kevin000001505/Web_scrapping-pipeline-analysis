# Web Scrapping
### Website: https://scweb.cwa.gov.tw/zh-tw/earthquake/data/

### Website
 <img src="Images/截圖 2024-03-28 下午4.53.35.png" alt="Example Image" title="An example image" width="700" height="400" />


### Motivation

### My goal is to create a machine that can:

- Automatically scrape all the data (including past 10 years) from websites.
- Stored data into PostgreSQL
### PostgreSQL 
  <img src="Images/截圖 2024-03-28 下午5.15.36.png" alt="Example Image" title="An example image" width="550" height="450" />

## **Why Scrapy and Selenium?**

- **Selenium:** The target website relies on JavaScript for its content, presenting a challenge for conventional scraping tools to effectively extract data. This is where Selenium excels. It simulates a real user's interaction with the webpage, and also can transform the website for Scrapy to scrape.
  
- **Scrapy:** Known for its efficiency with large datasets, Scrapy is used to handle the volume of data more effectively than Selenium.

## Next Goal
**Analysis the data by PostgreSQL and Python**
**Make the code run at airflow and transform the data into Azure and perform the data visualization by PowerBI**
