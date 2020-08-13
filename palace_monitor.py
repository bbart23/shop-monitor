import requests
import pickle
import discord
import datetime
import time
import re
from discord import Webhook, RequestsWebhookAdapter
from siteItem import SiteItem
from os import path

if path.exists('palace_list.dat'):
    filehandler = open('palace_list.dat', 'rb')
    ItemList = pickle.load(filehandler)
else:
    ItemList = []

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


switcher = {
    'Jackets': jackets,
    'Shirting': shirting,
    'Trousers': trousers,
    'Track Bottoms': trousers,
    'Shorts': trousers,
    'Bottoms': trousers,
    'Tracksuits': tracksuits,
    'Track Tops': tracksuits,
    'Sweatshirts': sweatshirts,
    'Longsleeves': sweatshirts,
    'Custom Sweatshirts': sweatshirts,
    'Tops': tops,
    'Knitwear': tops,
    'T-Shirts': tshirts,
    'Custom Jersey': tshirts,
    'Footwear': footwear,
    'Hats': hats,
    'Accessories': accessories,
    'Luggage': accessories,
    'Socks': accessories,
    'Skateboard Hardware': hardware,
    'Hardware': hardware
}

pageNum = 0

while True:
    time.sleep(10)
    pageNum += 1
    request = requests.get('https://shop-usa.palaceskateboards.com/products.json?limit=250&page=' + str(pageNum))

    decodedJson = request.json()

    if len(decodedJson['products']) == 0:
        pageNum = 0
        continue

    for product in decodedJson['products']:
        webhook = switcher.get(product['product_type'])

        ItemName = product['title']

        print(ItemName)

        SoldOut = True
        sizeString = ''
        for variant in product['variants']:
            #print(variant['available'])
            if variant['available'] == True:
                SoldOut = False
                size = variant['title']
                if size not in sizeString:
                    if sizeString == '':
                        sizeString += size
                    else:
                        sizeString += '|' + size
        try:
            ItemPicture = product['images'][0]['src']
        except IndexError:
            ItemPicture = ''

        ItemPrice = '$' + product['variants'][0]['price']
        ItemLink = 'https://shop-usa.palaceskateboards.com/products/' + product['handle']
        temp = SiteItem(ItemName, '', SoldOut)


        index = ExistsInList(temp)

        # If item already exists in list
        if index != -1:
            oldSoldOut = ItemList[index].SoldOut

            if SoldOut != oldSoldOut:
                if not SoldOut:
                    SendDiscordMessage(ItemName, ItemPrice, 'RESTOCK', ItemLink, ItemPicture, sizeString, webhook)
                else:
                    SendDiscordMessage(ItemName, ItemPrice, 'Sold Out', ItemLink, ItemPicture, sizeString, webhook)
                ItemList.pop(index)
                ItemList.append(temp)
        else:
            if not SoldOut:
                SendDiscordMessage(ItemName, ItemPrice, 'In Stock', ItemLink, ItemPicture, sizeString, webhook)
            ItemList.append(temp)



    #print(decodedJson['products'][0]['title'])
    file = open('palace_list.dat', 'wb')
    pickle.dump(ItemList, file)
    file.close()