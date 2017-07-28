# How to run the Realestate spider
scrapy crawl realestate_spider -a + arguments
# Defalut arguments
channel = 'rent' (single option: rent, buy, sold)
location = None
property_type = None (muliple options split by ,: House, unit apartment,
                      Townhouse, Villa, Land, Acreage, Rural, unitblock, retire)
minbeds = None (Single option: Studio,  1, 2, 3, 4, 5)
maxbeds = None (Single option: Studio,  1, 2, 3, 4, 5)
# Output log file
-s LOG_FILE=log.log

Eg.
scrapy crawl realestate_spider -a location="Box Hill, Vic, 3128" -a property_type="House" -a minbeds="2" -a maxbeds="2"




# How to run the Domain spider
scrapy crawl realestate_spider -a + arguments
# Defalut arguments
channel = 'rent' (single option: rent, buy, sold, newdev, share)
location = None
property_type = None (muliple options split by ,: House, Apartment, Rural, Land)
bedrooms = None (Single option: >1, >2, >3, >4, >5)
bathrooms = None (Single option: >1, >2, >3, >4, >5)
# Output log file
-s LOG_FILE=log.log

Eg.
scrapy crawl domain_spider -a location="Box Hill, Vic, 3128" -a property_type="House,Apartment" -a bedrooms=">4" -a bathrooms=">2"
