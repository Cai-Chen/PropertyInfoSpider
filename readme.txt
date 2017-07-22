# How to run the spider
scrapy crawl rentinfo_spider -a + arguments
# Defalut arguments
channel = 'rent' (single option: rent, buy, sold)
location = None
property_type = None (muliple options split by ,: House, unit apartment,
                      Townhouse, Villa, Land, Acreage, Rural, unitblock, retire)
minbeds = None (Single option: Studio,  1, 2, 3, 4, 5)
maxbeds = None (Single option: Studio,  1, 2, 3, 4, 5)

Eg.
scrapy crawl rentinfo_spider -a location="Box Hill, Vic 3128" -a property_type="House,unit apartment,Townhouse" -a minbeds="Studio" -a maxbeds="2"
