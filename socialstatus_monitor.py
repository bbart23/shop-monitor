import requests
import pickle
import discord
import datetime
import time
import re
from discord import Webhook, RequestsWebhookAdapter
from siteItem import SiteItem
from os import path

if path.exists('socialstatus_list.dat'):
    filehandler = open('socialstatus_list.dat', 'rb')
    ItemList = pickle.load(filehandler)
else:
    ItemList = []

socialstatusHook = 'https://discordapp.com/api/webhooks/738127814171164713/QdUyGB9w27UYnsSlsdsy1_RmDMBM07rWIB4yRwqYQ-6LLBanFR-JYdswyYVnI6O_kKte'
socialstatus = Webhook.from_url(socialstatusHook, adapter=RequestsWebhookAdapter())

def ExistsInList(item):
    ind = -1
    for Item in ItemList:
        ind += 1
        if Item.Name == item.Name and Item.Color == item.Color:
            return ind
    return -1

def SendDiscordMessage(itemName, itemColor, price, availability, URL, imageURL, sizes, webhook):
    Desc = '**Shop:** [Social Status (US)](https://www.socialstatuspgh.com/collections/sneakers/)\n**Color:** ' + itemColor + '\n**Price:** ' + price + '\n**State:** ' + availability + '\n\n> QuickTask\n> [' + sizes + '](' + URL + ')';
    Color = 12726577
    Footer = '[SneakerAlpha]'
    embed = discord.Embed(title=itemName, description=Desc, url=URL, color=Color, timestamp=datetime.datetime.now())
    embed.set_thumbnail(url=imageURL)
    embed.set_footer(text=Footer)
    webhook.send(embed=embed, username='Sneaker Alphas')

pageNum = 0

while True:
    time.sleep(10)
    pageNum += 1
    request = requests.get('https://www.socialstatuspgh.com/collections/sneakers/products.json?limit=250&page=' + str(pageNum))

    decodedJson = request.json()

    if len(decodedJson['products']) == 0:
        pageNum = 0
        continue

    for product in decodedJson['products']:
        webhook = socialstatus

        if '[' in product['title']:
            ItemName, ItemColor = product['title'].split('[')
            ItemColor = ItemColor[:-1]
        else:
            ItemName = product['title']
            ItemColor = ''
        SoldOut = True
        sizeString = ''
        for variant in product['variants']:
            #print(variant['available'])
            if variant['available'] == True:
                SoldOut = False
                size = variant['option2']
                if size is None:
                    size = variant['option1']
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
        ItemLink = 'https://www.socialstatuspgh.com/collections/sneakers/products/' + product['handle']
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
    file = open('socialstatus_list.dat', 'wb')
    pickle.dump(ItemList, file)
    file.close()