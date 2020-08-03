import requests
import pickle
import discord
import datetime
import time
import re
from discord import Webhook, RequestsWebhookAdapter
from siteItem import SiteItem
from os import path

if path.exists('undefeated_list.dat'):
    filehandler = open('undefeated_list.dat', 'rb')
    ItemList = pickle.load(filehandler)
else:
    ItemList = []

undefeatedHook = 'https://discordapp.com/api/webhooks/739893659197112340/Kp0QOzLZdlxE0cxnA3Qxq3SVf2PWZPh9-xRmUzlck2_1rH1Ttwf6-SO7RG6aolmjyV1v'
undefeated = Webhook.from_url(undefeatedHook, adapter=RequestsWebhookAdapter())

def ExistsInList(item):
    ind = -1
    for Item in ItemList:
        ind += 1
        if Item.Name == item.Name and Item.Color == item.Color:
            return ind
    return -1

def SendDiscordMessage(itemName, itemColor, price, availability, URL, imageURL, sizes, webhook):
    Desc = '**Shop:** [Undefeated Footwear (US)](https://undefeated.com/collections/mens-footwear/)\n**Price:** ' + price + '\n**State:** ' + availability + '\n\n> QuickTask\n> [' + sizes + '](' + URL + ')';
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
    request = requests.get('https://undefeated.com/collections/mens-footwear/products.json?limit=250&page=' + str(pageNum))

    decodedJson = request.json()

    if len(decodedJson['products']) == 0:
        pageNum = 0
        continue

    for product in decodedJson['products']:
        webhook = undefeated

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
                size = variant['option2']
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
        ItemLink = 'https://undefeated.com/collections/mens-footwear/products/' + product['handle']
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
                    except:
                        print('ERROR: Couldn\'t send message. Product Type: '+ product['product_type'].lower())
                else:
                    try:
                        SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'Sold Out', ItemLink, ItemPicture, sizeString, webhook)
                        print('[SOLD OUT]' + ItemName)
                    except:
                        print('ERROR: Couldn\'t send message. Product Type: '+ product['product_type'].lower())
                ItemList.pop(index)
                ItemList.append(temp)
        else:
            if not SoldOut:
                try:
                    SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'In Stock', ItemLink, ItemPicture, sizeString, webhook)
                    print('[IN STOCK]' + ItemName)
                except:
                    print('ERROR: Couldn\'t send message. Product Type: ' + product['product_type'].lower())
            ItemList.append(temp)



    #print(decodedJson['products'][0]['title'])
    file = open('undefeated_list.dat', 'wb')
    pickle.dump(ItemList, file)
    file.close()