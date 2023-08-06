import scrapy


class AllHousesSpider(scrapy.Spider):
    name = "all_houses"
    allowed_domains = ["hepsiemlak.com"]
    start_urls = ["https://hepsiemlak.com/en/kayseri?page=2"]

    def parse_house_detail(self, response):
        house_details = response.xpath("//div[@class='_35T4WV']")
        house_data = {}
        for detail in house_details:
            label = detail.xpath(".//div[@class='_1bVOdb'][1]/text()").get()
            value = detail.xpath(".//div[@class='_1bVOdb'][2]/text()").get()
            if label and value:
                house_data[label.strip()] = value.strip()
        house_data['Konumu'] = response.xpath("//div[@class='_3VQ1JB']/p/text()").get()
        house_data['Fiyat'] = response.xpath("(//div[@class='_2TxNQv']/text())[1]").get()

        house_descriptions = response.xpath("//div[@class='_3JTw7f']/text()").getall()
        house_description = (
            ', '.join(description.strip() for description in house_descriptions if description.strip())).replace('\xa0',
                                                                                                                 '')
        house_data['İlan Açıklaması'] = house_description

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
                yield scrapy.Request(url=next_page_url, callback=self.parse)
        else:
            print("Last Page")
