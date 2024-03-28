import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
import time
import psycopg2

class EarthquakeScrapeSpider(scrapy.Spider):
    name = 'earthquake_scrape'

    def start_requests(self):
        options = Options()
        options.add_argument("--headless")  # Run in headless mode, without a UI or display server dependencies
        
        self.driver = webdriver.Chrome(options=options)

        start_urls = ['https://scweb.cwa.gov.tw/zh-tw/earthquake/data/']

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        self.driver.get(response.url)
        selector = Selector(text=self.driver.page_source)
        
        table_button = self.driver.find_element(By.ID, "Search")
        
        for year in range(10):
            table_button.click()
            if year != 0:
                year_button = self.driver.find_element(By.XPATH, "//div[@class='datepicker datepicker-dropdown dropdown-menu datepicker-orient-left datepicker-orient-bottom']//div[@class='datepicker-months']//th[@class='prev']")
                year_button.click()
                time.sleep(1)

            for count in range(1,13):
                table_button.click()
                month_button = self.driver.find_element(By.XPATH, f"//div[@class='datepicker datepicker-dropdown dropdown-menu datepicker-orient-left datepicker-orient-bottom']//div[@class='datepicker-months']//td/span[{count}]")
                month_button.click()
                time.sleep(1)

                selector = Selector(text=self.driver.page_source)

                table_rows = selector.xpath('//table[@id="table"]/tbody/tr')
                for row in table_rows:
                    if row.xpath(".//td[2]/div/text()").get() == None:
                        continue
                    else:
                        yield{
                            'maximum': float(row.xpath(".//td[2]/div/text()").get()),
                            'date': row.xpath(".//td[@class=' d-lg-none']/text()").get().split(' ')[0],
                            'time': row.xpath(".//td[@class=' d-lg-none']/text()").get().split(' ')[1],
                            'scale': float(row.xpath(".//td[4]/text()").get()),
                            'depth': float(row.xpath(".//td[5]/text()").get()),
                            'place': row.xpath(".//td[6]/a[1]/text()").get(),
                        }

                while "disabled" not in selector.xpath("//li[@id='table_next']").get():
        
                    next_page = self.driver.find_element(By.XPATH, "//li[@id='table_next']/a")
                    next_page.click()
                    time.sleep(2)

                    selector = Selector(text=self.driver.page_source)

                    Date = selector.xpath("//input[@id='Search']/@value").get()
                    table_rows = selector.xpath('//table[@id="table"]/tbody/tr')
                    
                    for row in table_rows:
                        yield{
                            'maximum': float(row.xpath(".//td[2]/div/text()").get()),
                            'date': row.xpath(".//td[@class=' d-lg-none']/text()").get().split(' ')[0],
                            'time': row.xpath(".//td[@class=' d-lg-none']/text()").get().split(' ')[1],
                            'scale': float(row.xpath(".//td[4]/text()").get()),
                            'depth': float(row.xpath(".//td[5]/text()").get()),
                            'place': row.xpath(".//td[6]/a[1]/text()").get(),
                        }
                    continue
                else:
                    None


    
    


