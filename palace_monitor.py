import requests
import discord
import datetime
import pickle
from os import path
from discord import Webhook, RequestsWebhookAdapter
from bs4 import BeautifulSoup
from siteItem import SiteItem

if path.exists('palace_list.dat'):
    filehandler = open('palace_list.dat', 'rb')
    ItemList = pickle.load(filehandler)
else:
    ItemList = []

PalaceLinks = ['jackets', 'shirting', 'trousers', 'tracksuits', 'sweatshirts', 'tops', 't-shirts',
               'footwear', 'hats', 'accessories', 'hardware']
client = discord.Client()
URL = 'https://shop-usa.palaceskateboards.com/collections/'

jacketsHook = 'https://discordapp.com/api/webhooks/727938045571104890/SEXTWOh8oFHOmGYa-qmWpnLJZdGs9p8WhDHfqlOv' \
              '-ThHxmHg77ecttVCgIT-LXEBLkeN '
shirtingHook = 'https://discordapp.com/api/webhooks/727938271660998698' \
               '/WRiRqZq3109Abzz_cVG6tYAODDyT6du4zy0ib7kLH3Vqfhp8-Q-UwkIGy3HH3B64B1I7 '
trousersHook = 'https://discordapp.com/api/webhooks/727938909790535753' \
               '/J_rxuSEKvnTXcT0vbM74TkU8rB6lM3xbAXpTy1nXLnUiDCM03UjsYHFOznZLWwaheUL5 '
tracksuitsHook = 'https://discordapp.com/api/webhooks/727939691160272999/XBSkn09tkfeCEel' \
                 '-rBaTMhPbvFglP7O_vfbDP3iUzxnitK26xYhKzyKuJbckautdvZ29 '
sweatshirtsHook = 'https://discordapp.com/api/webhooks/727939809389314129' \
                  '/KYCwLCG9URvrc9opSHdIrQInFQBEoWJB7mez5e1gYM5D4GqNgafmnZDlXVPleTeYPwOd '
topsHook = 'https://discordapp.com/api/webhooks/727939903421415522/pE8ov-GL8BowBv9O27yI75YCvhmlyetqEQXbU1' \
           '-zSRTG30mXWbDl__Vpa-HmkvXjp_ve '
tshirtsHook = 'https://discordapp.com/api/webhooks/727939983674966057/NQH_9Jdi3emneC3HQv_Jpyg1kVuLhGKYHfJjbz_xVTjjQu' \
              '-SGrlU-0vxlYilRfaDFn2_ '
footwearHook = 'https://discordapp.com/api/webhooks/727940106018750466/fZxAI1EOLA' \
               '-WpJDQ2_EKMcNMKIrnPAF7sq6CPahlSECEBVACJI33ItPWcdXS-KaGsPys '
hatsHook = 'https://discordapp.com/api/webhooks/727940194262712381/meRKSAX9dod-4J_VvZk-EvhCI6JSdLH1J0k643U7n' \
           '-2WyCsFcD0ZuLmPMIOIyEIiucp0 '
accessoriesHook = 'https://discordapp.com/api/webhooks/727940284985376800' \
                  '/kkOiDXprDZ8pCTSlp7mRrZXq2B6QjMZu2UHtEm9X1d6346pxNmY3QsXfPOGS8_Nx9ymL '
hardwareHook = 'https://discordapp.com/api/webhooks/727940383383748692' \
               '/fFbVgvE7QBubnrwAhqrKbO6XQfCBR6FzYIb_bDbQsS59uJOQCmD7FDjG0pWHmiokLTTz '

jackets = Webhook.from_url(jacketsHook, adapter=RequestsWebhookAdapter())
shirting = Webhook.from_url(shirtingHook, adapter=RequestsWebhookAdapter())
trousers = Webhook.from_url(trousersHook, adapter=RequestsWebhookAdapter())
tracksuits = Webhook.from_url(tracksuitsHook, adapter=RequestsWebhookAdapter())
sweatshirts = Webhook.from_url(sweatshirtsHook, adapter=RequestsWebhookAdapter())
tops = Webhook.from_url(topsHook, adapter=RequestsWebhookAdapter())
tshirts = Webhook.from_url(tshirtsHook, adapter=RequestsWebhookAdapter())
footwear = Webhook.from_url(footwearHook, adapter=RequestsWebhookAdapter())
hats = Webhook.from_url(hatsHook, adapter=RequestsWebhookAdapter())
accessories = Webhook.from_url(accessoriesHook, adapter=RequestsWebhookAdapter())
hardware = Webhook.from_url(hardwareHook, adapter=RequestsWebhookAdapter())



def ExistsInList(item):
    ind = -1
    for Item in ItemList:
        ind += 1
        if Item.Name == item.Name:
            return ind
    return -1


def SendDiscordMessage(itemName, price, availability, URL, imageURL, sizes, webhook):
    Desc = '**Shop:** [Palace (US)](https://shop-usa.palaceskateboards.com/)\n**Price:** ' + price + '\n**State:** ' + availability + '\n\n> QuickTask\n> [' + sizes + '](' + URL + ')';
    Color = 12726577
    Footer = '[SneakerAlpha]'
    embed = discord.Embed(title=itemName, description=Desc, url=URL, color=Color, timestamp=datetime.datetime.now())
    embed.set_thumbnail(url=imageURL)
    embed.set_footer(text=Footer)
    webhook.send(embed=embed, username='Sneaker Alphas')


def IsElementPresent(element):
    soldOut = element.find(class_='price').text
    if 'SOLD' in soldOut:
        return True
    return False


switcher = {
    'jackets': jackets,
    'shirting': shirting,
    'trousers': trousers,
    'tracksuits': tracksuits,
    'sweatshirts': sweatshirts,
    'tops': tops,
    't-shirts': tshirts,
    'footwear': footwear,
    'hats': hats,
    'accessories': accessories,
    'hardware': hardware
}

while True:
    for palacelink in PalaceLinks:
        print('Looking at ' + palacelink)
        webhook = switcher.get(palacelink)
        page = requests.get(URL + palacelink)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id='product-loop')

        item_elems = results.find_all(class_='product-grid-item clearfix')
        for article in item_elems:
            ItemName = article.find(class_='product-info').find(class_='title').text
            #print(ItemName)
            #ItemColor = article.find(class_='product-style').find(class_='name-link').text
            SoldOut = IsElementPresent(article)
            ItemLink = 'https://shop-usa.palaceskateboards.com/' + article.find('a').get('href')
            ItemPicture = 'https:' + article.find('img').get('src')
            #print(ItemPicture)

            temp = SiteItem(ItemName, '', SoldOut)
            index = ExistsInList(temp)
            if index != -1:
                oldSoldOut = ItemList[index].SoldOut
                oldPrice = ItemList[index].Price
                oldSizes = ItemList[index].Sizes

                if SoldOut != oldSoldOut:
                    if not SoldOut:
                        page2 = requests.get(ItemLink)
                        soup2 = BeautifulSoup(page2.content, 'html.parser')
                        ItemPrice = soup2.find('span', class_='prod-price').text
                        temp.Price = ItemPrice
                        sizeString = ""
                        sizes = soup2.find(id='product-select').find_all('option')
                        for size in sizes:
                            if sizeString == "":
                                sizeString += size.text
                            else:
                                sizeString += '|' + size.text
                        temp.Sizes = sizeString
                        SendDiscordMessage(ItemName, ItemPrice, 'RESTOCK', ItemLink, ItemPicture, sizeString,
                                           webhook)
                    else:
                        SendDiscordMessage(ItemName, oldPrice, 'Sold Out', ItemLink, ItemPicture, '',
                                           webhook)
                    ItemList.pop(index)
                    ItemList.append(temp)
            else:
                if not SoldOut:
                    page2 = requests.get(ItemLink)
                    soup2 = BeautifulSoup(page2.content, 'html.parser')
                    ItemPrice = soup2.find('span', class_='prod-price').text
                    temp.Price = ItemPrice
                    sizeString = ""
                    sizes = soup2.find(id='product-select').find_all('option')
                    for size in sizes:
                        if sizeString == "":
                            sizeString += size.text
                        else:
                            sizeString += '|' + size.text
                    temp.Sizes = sizeString
                    if not SoldOut:
                        SendDiscordMessage(ItemName, ItemPrice, 'In Stock', ItemLink, ItemPicture, sizeString,
                                           webhook)
                ItemList.append(temp)
    file = open('palace_list.dat', 'wb')
    pickle.dump(ItemList, file)
    file.close()