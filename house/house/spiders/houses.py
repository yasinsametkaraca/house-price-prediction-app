import scrapy


class HouseItem(scrapy.Item):
    category = scrapy.Field()
    location = scrapy.Field()
    price = scrapy.Field()
    area = scrapy.Field()
    room = scrapy.Field()
    floor = scrapy.Field()
    heating = scrapy.Field()
    building_age = scrapy.Field()
    floor_number = scrapy.Field()
    number_of_floors = scrapy.Field()
    number_of_bathrooms = scrapy.Field()
    number_of_balconies = scrapy.Field()
    number_of_rooms = scrapy.Field()
    building_status = scrapy.Field()
    building_type = scrapy.Field()
    facade = scrapy.Field()
    deed_status = scrapy.Field()
    usage_status = scrapy.Field()
    credit = scrapy.Field()
    swap = scrapy.Field()
    student = scrapy.Field()
    parent = scrapy.Field()
    investment = scrapy.Field()
    site = scrapy.Field()
    front = scrapy.Field()
    rear = scrapy.Field()
    right = scrapy.Field()


class HousesSpider(scrapy.Spider):
    name = "houses"
    allowed_domains = ["emlakjet.com"]
    start_urls = ["https://emlakjet.com/satilik-konut/kayseri"]

    def parse_house_detail(self, response, house_category):
        house_details = response.xpath("//div[@class='_35T4WV']")
        house_data = {}
        for detail in house_details:
            label = detail.xpath(".//div[@class='_1bVOdb'][1]/text()").get()
            value = detail.xpath(".//div[@class='_1bVOdb'][2]/text()").get()
            if label and value:
                house_data[label.strip()] = value.strip()
        house_data["Kategori"] = house_category
        house_data['Konumu'] = response.xpath("//div[@class='_3VQ1JB']/p/text()").get()
        house_data['Fiyat'] = response.xpath("(//div[@class='_2TxNQv']/text())[1]").get()

        house_descriptions = response.xpath("//div[@class='_3JTw7f']/text()").getall()
        house_description = (', '.join(description.strip() for description in house_descriptions if description.strip())).replace('\xa0', '')
        house_data['İlan Açıklaması'] = house_description

        yield house_data

    def parse(self, response):
        houses = response.xpath("//div[@id='listing-search-wrapper']/div[@class='_3qUI9q']")
        for house in houses:
            house_category = house.xpath(".//div[@class='_2UELHn']/span/text()").get()
            house_detail = house.xpath(".//a/@href").get()
            if house_detail:
                full_url = response.urljoin(house_detail)
                yield scrapy.Request(url=full_url, callback=self.parse_house_detail, cb_kwargs={'house_category': house_category})

        next_page_div = response.xpath("//div[@class='_3au2n_']/a[contains(text(), 'Sonraki')]")
        if next_page_div:
            next_page = next_page_div.xpath("./@href").get()
            if next_page:
                next_page_url = response.urljoin(next_page)
                yield scrapy.Request(url=next_page_url, callback=self.parse)
