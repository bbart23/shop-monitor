import requests
import discord
import datetime
from discord import Webhook, RequestsWebhookAdapter
from bs4 import BeautifulSoup
from siteItem import SiteItem

ItemList = []
SupremeLinks = ['jackets', 'shirts', 'tops_sweaters', 'pants', 'shorts', 'bags', 'hats', 'accessories', 'shoes',
                'skate']
client = discord.Client()
URL = 'https://www.supremenewyork.com/shop/all/'

jacketsHook = 'https://discordapp.com/api/webhooks/720718856334737461' \
              '/QY7tsbDCROQsJbmJKHSpYo8cZkHd6A8xwKGY1r1mFLFzboxCatATfM23ivHSF5Dxtf3l '
shirtsHook = 'https://discordapp.com/api/webhooks/720718993509449841' \
             '/g1MM58AwvkDAM1DTQKwc0CA4X_NIjbdTm7qDyJsNgdwUFsuHDq4Fc2QPwK-xd-zjPnX_ '
topsHook = 'https://discordapp.com/api/webhooks/720719064850366545/02kPtBhlKNzeZIloPPf3qp4A-leg' \
           '-EE45PGHvDtN8p7noZd27yCq28XXkqAlzmuTbFhB '
sweatshirtsHook = 'https://discordapp.com/api/webhooks/720719283348439111/h_6peoDUdU9qTavCpANm4tLh4V' \
                  '-s_2bH4fGhMQEGQm6BgxmLgK_ZWjClmwKbx7aX0uEE '
pantsHook = 'https://discordapp.com/api/webhooks/720719348490174575' \
            '/qdLqBGZHA0XpdAm0bSxjuy0txqbrNPsm1t9uvQAmfhmxsD4TSp-Y6gzI5xcqz4__HBK7 '
shortsHook = 'https://discordapp.com/api/webhooks/720719480820334684' \
             '/OTAxO0gj4v6lpaV7Ws_aWT4dnYVBrQrnHSHXsSk_XoAMX2Q93r81FnhGpLPwNtRne804 '
hatsHook = 'https://discordapp.com/api/webhooks/720719572373864478' \
           '/mndahLkPYwZ3YtUW94dSNVmqZ9uwEoykbJsgbvtyMighEIolw_n6edOGEbQtnJanIvuF '
bagsHook = 'https://discordapp.com/api/webhooks/720719634474598552' \
           '/HM86d8z9H1WhBiK4RLRvAZ11Hcq5BPIrKfoT2ZKFoltcmdON2nKpArWbEb_mkOZjbx0h '
accessoriesHook = 'https://discordapp.com/api/webhooks/720719983390359693' \
                  '/w68pRsUksEpEXArI2fj4GxRjL3IypM0SfUVDzN024lGxY1HJiIMknOF_BNq640CmhcMQ '
shoesHook = 'https://discordapp.com/api/webhooks/720720113371840534/XA-1s3t1ynsq-1FW9WLylvgHIOk' \
            '-QbK21qJUBWfitvwauuaRFYkQ5Q54bNnZs_2zFhGi '
skateHook = 'https://discordapp.com/api/webhooks/720720159333023815' \
            '/IuZzeFJgK0gc2bjKMjTTkRe9ZlEZmLeGfdJLzCs1lAEbTEKlsOqJDj7gNe8EeVR2z9ae '

jackets = Webhook.from_url(jacketsHook, adapter=RequestsWebhookAdapter())
shirts = Webhook.from_url(shirtsHook, adapter=RequestsWebhookAdapter())
tops = Webhook.from_url(topsHook, adapter=RequestsWebhookAdapter())
sweatshirts = Webhook.from_url(sweatshirtsHook, adapter=RequestsWebhookAdapter())
pants = Webhook.from_url(pantsHook, adapter=RequestsWebhookAdapter())
shorts = Webhook.from_url(shortsHook, adapter=RequestsWebhookAdapter())
hats = Webhook.from_url(hatsHook, adapter=RequestsWebhookAdapter())
bags = Webhook.from_url(bagsHook, adapter=RequestsWebhookAdapter())
accessories = Webhook.from_url(accessoriesHook, adapter=RequestsWebhookAdapter())
shoes = Webhook.from_url(shoesHook, adapter=RequestsWebhookAdapter())
skate = Webhook.from_url(skateHook, adapter=RequestsWebhookAdapter())


def ExistsInList(item):
    ind = -1
    for Item in ItemList:
        ind += 1
        if Item.Name == item.Name and Item.Color == item.Color:
            return ind
    return -1


def SendDiscordMessage(itemName, itemColor, price, availability, URL, imageURL, sizes, webhook):
    Desc = '**Shop:** [Supreme (US)](https://www.supremenewyork.com/shop/)\n**Color:** ' + itemColor + '\n**Price:** ' + price + '\n**State:** ' + availability + '\n\n> QuickTask\n> [' + sizes + '](' + URL + ')';
    Color = 12726577
    Footer = '[SneakerAlpha]'
    embed = discord.Embed(title=itemName, description=Desc, url=URL, color=Color, timestamp=datetime.datetime.now())
    embed.set_thumbnail(url=imageURL)
    embed.set_footer(text=Footer)
    webhook.send(embed=embed, username='Sneaker Alphas')


def IsElementPresent(element):
    soldOut = element.find(class_='sold_out_tag')
    if soldOut is None:
        return False
    return True


switcher = {
    'jackets': jackets,
    'shirts': shirts,
    'tops_sweaters': tops,
    'sweatshirts': sweatshirts,
    'pants': pants,
    'shorts': shorts,
    'hats': hats,
    'bags': bags,
    'accessories': accessories,
    'shoes': shoes,
    'skate': skate
}
# webhook = switcher.get('jackets')
# webhook.send('Bruh',username = 'Sneaker Alphas')

# SendDiscordMessage('Big Letter Track Jacket', 'Black', '$150', 'Sold Out', 'https://www.supremenewyork.com/shop/jackets/p7z6mv4ur/dcpah7svl', 'https://assets.supremenewyork.com/184948/vi/Pwdr-0riLL8.jpg', 'Medium|Small', webhook)

while True:
    for supremelink in SupremeLinks:
        print('Looking at' + supremelink)
        webhook = switcher.get(supremelink)
        page = requests.get(URL + supremelink)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id='container')

        item_elems = results.find_all(class_='inner-article')
        for article in item_elems:
            ItemName = article.find(class_='product-name').find(class_='name-link').text
            print(ItemName)
            ItemColor = article.find(class_='product-style').find(class_='name-link').text
            SoldOut = IsElementPresent(article)
            ItemLink = 'https://www.supremenewyork.com/' + article.find('a').get('href')
            ItemPicture = 'https:' + article.find('img').get('src')
            print(ItemPicture)

            temp = SiteItem(ItemName, ItemColor, SoldOut)
            index = ExistsInList(temp)
            if index != -1:
                oldSoldOut = ItemList[index].SoldOut
                oldPrice = ItemList[index].Price
                oldSizes = ItemList[index].Sizes

                if SoldOut != oldSoldOut:
                    if not SoldOut:
                        page2 = requests.get(ItemLink)
                        soup2 = BeautifulSoup(page2.content, 'html.parser')
                        ItemPrice = soup2.find(class_='price').text
                        temp.Price = ItemPrice
                        sizeString = ""
                        sizes = soup2.find(id='cctrl').find_all('option')
                        for size in sizes:
                            if sizeString == "":
                                sizeString += size.text
                            else:
                                sizeString += '|' + size.text
                        temp.Sizes = sizeString
                        SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'RESTOCK', ItemLink, ItemPicture, sizeString,
                                           webhook)
                    else:
                        SendDiscordMessage(ItemName, ItemColor, oldPrice, 'Sold Out', ItemLink, ItemPicture, oldSizes,
                                           webhook)
                    ItemList.pop(index)
                    ItemList.append(temp)
            else:
                page2 = requests.get(ItemLink)
                soup2 = BeautifulSoup(page2.content, 'html.parser')
                ItemPrice = soup2.find(class_='price').text
                temp.Price = ItemPrice
                sizeString = ""
                sizes = soup2.find(id='cctrl').find_all('option')
                for size in sizes:
                    if sizeString == "":
                        sizeString += size.text
                    else:
                        sizeString += '|' + size.text
                temp.Sizes = sizeString
                if not SoldOut:
                    SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'In Stock', ItemLink, ItemPicture, sizeString,
                                       webhook)
                ItemList.append(temp)
