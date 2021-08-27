from bs4 import BeautifulSoup as soup
from bs4.element import PageElement, ResultSet
import urllib.request


class ScraperURLopener(urllib.request.URLopener):
    """A class used to change the User Agent of the URLopener during the request"""
    version = 'Mozilla/5.0'


def getContainers(opener: ScraperURLopener, url: str) -> ResultSet[PageElement]:
    """Returns containers representing parsed HTML data for Sweetwater synthesizer products"""
    uClient = opener.open(url)
    pageHTML = uClient.read()
    uClient.close()
    pageSoup = soup(pageHTML, 'html.parser') 
    containers = pageSoup.findAll('div', {'class': 'product-card'})
    return containers
    
#################################################################################

# creates a file to store scraped data
filename = 'products.csv'
f = (open(filename, 'w'))
headers = "product_name, price, finance_offer_months, finance_offer_price, rating\n"
f.write(headers)

# creating request object and string containing a URL to Sweetwater website
opener = ScraperURLopener()
SweetwaterURL = 'https://www.sweetwater.com/c510--Synthesizers?ost=&pn='

# loops through webpages containing synthesizer keyboard products
for i in range(5):
    currWebpage = SweetwaterURL + str(i + 1)
    
    # opens up a connection to the URL and grabs each product on the current webpage
    containers = getContainers(opener, currWebpage)

    # parses the webpage HTML
    for container in containers:
        # "if" conditional handles ignoring containers that are used for advertisement
        if len(container['class']) == 1:   
            nameContainer = container.findAll('h2', {'class': 'product-card__name'})
            productName = nameContainer[0].a.text.strip()

            priceContainer = container.findAll('em', {'class': 'product-card__price'})
            price = priceContainer[0].div.strong.text.strip()

            financeMonthsContainer = container.findAll('em', {'class': 'product-card__finance-months'})
            if len(financeMonthsContainer) == 0:
                financeMonths = '0'
                financePrice = '$0'
            else:
                financeMonths = financeMonthsContainer[0].text.strip()
                financePriceContainer = container.findAll('em', {'class': 'product-card__finance-amount'})
                financePrice = financePriceContainer[0].text.strip()

            ratingContainer = container.findAll('span', {'class': 'rating__stars'})
            if len(ratingContainer) == 0:
                rating = '0'
            else:
                rating = ratingContainer[0]['data-rated']

            # Writes the data to the products.csv file; removes commas and dollar signs from variables
            f.write(productName.replace(',', '|') + ',' + price[1:].replace(',', '') + ',' + financeMonths + ',' + financePrice[1:].replace(',', '') + ',' + rating + '\n')

f.close()