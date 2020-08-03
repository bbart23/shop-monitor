import requests
import pickle
import discord
import datetime
import time
import re
from discord import Webhook, RequestsWebhookAdapter
from siteItem import SiteItem
from os import path

if path.exists('westnyc_list.dat'):
    filehandler = open('westnyc_list.dat', 'rb')
    ItemList = pickle.load(filehandler)
else:
    ItemList = []

westnycHook = 'https://discordapp.com/api/webhooks/739919591328841798/s4ynbBbgY_N2rGXffv__V5GVJ7M0DDd9HkzrdP2nI200d9q0NycAd2CT3B9v9PAbNV7y'
westnyc = Webhook.from_url(westnycHook, adapter=RequestsWebhookAdapter())

jordanHook = 'https://discordapp.com/api/webhooks/739924749127516291/Q3rX5AenW1d9E7vB9BA8HBncLmk8u0Y2z3zHR9mMjKqpUZTI_sDqyRl4xM_HN9gatMJk'
yeezyHook = 'https://discordapp.com/api/webhooks/739927902786945105/TnD1CAjmWdJHj5AEiIsbq1SmEr1kD92z6l37qCdBKTuI67_YErcgFSM8buui2cSoMNo1'
nikesbHook = 'https://discordapp.com/api/webhooks/739927996391227493/oZdCOwhdb7uErLSiujwz452Cyja6Fg1lw_1li_25D190BmKrTuSsO0wdmW0uiG90Grip'

jordan = Webhook.from_url(jordanHook, adapter=RequestsWebhookAdapter())
yeezy = Webhook.from_url(yeezyHook, adapter=RequestsWebhookAdapter())
nikesb = Webhook.from_url(nikesbHook, adapter=RequestsWebhookAdapter())

def ExistsInList(item):
    ind = -1
    for Item in ItemList:
        ind += 1
        if Item.Name == item.Name and Item.Color == item.Color:
            return ind
    return -1

def SendDiscordMessage(itemName, itemColor, price, availability, URL, imageURL, sizes, webhook):
    Desc = '**Shop:** [West NYC (US)](https://www.westnyc.com/collections/footwear/)\n**Price:** ' + price + '\n**State:** ' + availability + '\n\n> QuickTask\n> [' + sizes + '](' + URL + ')';
    Color = 12726577
    Footer = '[SneakerAlpha]'
    embed = discord.Embed(title=itemName, description=Desc, url=URL, color=Color, timestamp=datetime.datetime.now())
    embed.set_thumbnail(url=imageURL)
    embed.set_footer(text=Footer)
    webhook.send(embed=embed, username='Sneaker Alphas')


#brands = ['adidas', 'jordan', 'play', 'butter', 'nike', 'y-3', 'yeezy', 'white']
pageNum = 0

while True:
    time.sleep(10)
    pageNum += 1
    request = requests.get('https://www.westnyc.com/collections/footwear/products.json?limit=250&page=' + str(pageNum))

    decodedJson = request.json()

    if len(decodedJson['products']) == 0:
        pageNum = 0
        continue

    for product in decodedJson['products']:
        webhook = westnyc

        #if all(x not in product['vendor'].lower() for x in brands):
        #    continue

        ItemName = product['title']
        ItemColor = product['handle']
        SoldOut = True
        sizeString = ''
        for variant in product['variants']:
            #print(variant['available'])
            if variant['available'] == True:
                SoldOut = False
                size = variant['option1']
                if size is None:
                    size = ''
                if size not in sizeString:
                    if sizeString == '':
                        sizeString += size
                    else:
                        sizeString += '|' + size

        if product['variants'][0]['featured_image'] is not None:
            ItemPicture = product['variants'][0]['featured_image']['src']
        else:
            try:
                ItemPicture = product['images'][0]['src']
            except IndexError:
                ItemPicture = ''
        ItemPrice = '$' + product['variants'][0]['price']
        ItemLink = 'https://www.westnyc.com/collections/footwear/products/' + product['handle']
        temp = SiteItem(ItemName, ItemColor, SoldOut)


        index = ExistsInList(temp)

        # If item already exists in list
        if index != -1:
            oldSoldOut = ItemList[index].SoldOut

            if SoldOut != oldSoldOut:
                if not SoldOut:
                    try:
                        SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'RESTOCK', ItemLink, ItemPicture, sizeString, webhook)
                        print('[RESTOCK]' + ItemName)
                        if 'jordan' in ItemName.lower():
                            SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'RESTOCK', ItemLink, ItemPicture,
                                               sizeString, jordan)
                        if 'yeezy' in ItemName.lower():
                            SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'RESTOCK', ItemLink, ItemPicture,
                                               sizeString, yeezy)
                        if 'nike' in ItemName.lower() and 'sb' in ItemName.lower():
                            SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'RESTOCK', ItemLink, ItemPicture,
                                               sizeString, nikesb)
                    except:
                        print('ERROR: Couldn\'t send message. Product Type: '+ product['product_type'].lower())
                else:
                    try:
                        SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'Sold Out', ItemLink, ItemPicture, sizeString, webhook)
                        print('[SOLD OUT]' + ItemName)
                        if 'jordan' in ItemName.lower():
                            SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'Sold Out', ItemLink, ItemPicture,
                                               sizeString, jordan)
                        if 'yeezy' in ItemName.lower():
                            SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'Sold Out', ItemLink, ItemPicture,
                                               sizeString, yeezy)
                        if 'nike' in ItemName.lower() and 'sb' in ItemName.lower():
                            SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'Sold Out', ItemLink, ItemPicture,
                                               sizeString, nikesb)
                    except:
                        print('ERROR: Couldn\'t send message. Product Type: '+ product['product_type'].lower())
                ItemList.pop(index)
                ItemList.append(temp)
        else:
            if not SoldOut:
                try:
                    SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'In Stock', ItemLink, ItemPicture, sizeString, webhook)
                    print('[IN STOCK]' + ItemName)
                    if 'jordan' in ItemName.lower():
                        SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'In Stock', ItemLink, ItemPicture,
                                           sizeString, jordan)
                    if 'yeezy' in ItemName.lower():
                        SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'In Stock', ItemLink, ItemPicture,
                                           sizeString, yeezy)
                    if 'nike' in ItemName.lower() and 'sb' in ItemName.lower():
                        SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'In Stock', ItemLink, ItemPicture,
                                           sizeString, nikesb)
                except:
                    print('ERROR: Couldn\'t send message. Product Type: ' + product['product_type'].lower())
            ItemList.append(temp)



    #print(decodedJson['products'][0]['title'])
    file = open('westnyc_list.dat', 'wb')
    pickle.dump(ItemList, file)
    file.close()