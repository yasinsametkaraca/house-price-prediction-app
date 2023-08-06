# house-price-prediction

scrapy startproject house  # to create a project
cd house

scrapy genspider houses site.com/satilik-konut/kayseri  # to create a spider

scrapy crawl houses  # to run a spider

scrapy crawl houses -o houses.csv  # to save the output to a csv file

scrapy crawl houses -o houses.json  # to save the output to a json file

scrapy crawl houses -o houses.xml  # to save the output to a xml file

scrapy crawl houses -o houses.jsonlines  # to save the output to a jsonlines file

scrapy crawl houses -o houses.pickle  # to save the output to a pickle file

scrapy crawl houses -o houses.yml  # to save the output to a yaml file

scrapy crawl houses -o houses.msgpack  # to save the output to a msgpack file
