import scrapy


class AllHousesSpider(scrapy.Spider):
    name = "all_houses"
    allowed_domains = ["hepsiemlak.com"]
    start_urls = ["https://hepsiemlak.com/en/kayseri-satilik?page=2"]
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        # 'DOWNLOAD_DELAY': 2,  # 1 second delay
        # 'CONCURRENT_REQUESTS': 1,  # 1 request at a time
    }

    def parse_house_detail(self, response):
        house_details = response.xpath("//li[@class='spec-item']")
        house_data = {}
        for detail in house_details:
            label = detail.xpath(".//span[1]/text()").get()
            value = detail.xpath(".//span[2]/text()").get()
            if label and value:
                house_data[label.strip()] = value.strip()
        house_data['City'] = response.xpath("(//ul[@class='short-info-list']/li/text())[1]").get().strip()
        house_data['District'] = response.xpath("(//ul[@class='short-info-list']/li/text())[2]").get().strip()
        house_data['Town'] = response.xpath("(//ul[@class='short-info-list']/li/text())[3]").get().strip()
        house_data['Price'] = response.xpath("//div[@class='right']/p/text()").get()

        yield house_data

    def parse(self, response):
        houses = response.xpath("//li[@class='listing-item']")
        for house in houses:
            house_detail = house.xpath(".//div[@class='links']/a/@href").get()
            if house_detail:
                full_url = response.urljoin(house_detail)
                yield scrapy.Request(url=full_url, callback=self.parse_house_detail)

        next_page_div = response.xpath("//div[@class='he-pagination']/a[contains(text(), 'Next Page')]")
        if next_page_div:
            next_page = next_page_div.xpath("./@href").get()
            print(next_page)
            if next_page:
                next_page_url = response.urljoin(next_page)
                yield scrapy.Request(url=next_page_url, callback=self.parse, dont_filter=True)
        else:
            print("Last Page")
