import requests
import pickle
import discord
import datetime
import time
import re
from discord import Webhook, RequestsWebhookAdapter
from siteItem import SiteItem
from os import path

if path.exists('vlone_list.dat'):
    filehandler = open('vlone_list.dat', 'rb')
    ItemList = pickle.load(filehandler)
else:
    ItemList = []

tshirtsHook = 'https://discordapp.com/api/webhooks/732716854006644739/TUusTbn5szYGrQ9Hm54ABGuKSD0Y80QdZ0Ta6yijKgeVS2F4pVXMVY1Nwfa2q8I7qgyA'
longSleevesHook = 'https://discordapp.com/api/webhooks/732717110169567345/865ylGA6ae1ya2yOKCZI3Xm8T1kIe2MjeCHCqITXAYFomz8uOkp8dAgSFSIf8gXeBHUd'
crewnecksHook = 'https://discordapp.com/api/webhooks/732717284824580156/ut4z-G-quKtSjX4OC-kFVp5UJCkAY6ABy1KTue7J1UDsOGLI6t7w87gfvoJYUToJBGAp'
hoodiesHook = 'https://discordapp.com/api/webhooks/732717424130130041/gAnuiPqN1Wk89w9PPrVmQAA6LiURcGP5Squ84y1SnL1kRA7e2aLCV35X5LwFlNJ4gncM'
pantsHook = 'https://discordapp.com/api/webhooks/732717545936650291/GtlO-7Er8nfNMUOh4PS4HTNRZGozHlTg7qY8aBjupeIIfW0Xv_EwnYBkdBPZW7EfOeYm'
jacketsHook ='https://discordapp.com/api/webhooks/732717617688739911/D_Bk6xF66m4sTJkaNVMxIVmNfi0Hm1QVhdinvqCFXRhn5BY5Nf_NN3CHa7PX7hzC60As'

tshirts = Webhook.from_url(tshirtsHook, adapter=RequestsWebhookAdapter())
longSleeves = Webhook.from_url(longSleevesHook, adapter=RequestsWebhookAdapter())
crewnecks = Webhook.from_url(crewnecksHook, adapter=RequestsWebhookAdapter())
hoodies = Webhook.from_url(hoodiesHook, adapter=RequestsWebhookAdapter())
pants = Webhook.from_url(pantsHook, adapter=RequestsWebhookAdapter())
jackets = Webhook.from_url(jacketsHook, adapter=RequestsWebhookAdapter())

def ExistsInList(item):
    ind = -1
    for Item in ItemList:
        ind += 1
        if Item.Name == item.Name and Item.Color == item.Color:
            return ind
    return -1

def SendDiscordMessage(itemName, itemColor, price, availability, URL, imageURL, sizes, webhook):
    Desc = '**Shop:** [VLone (US)](https://livevlonedievlone.myshopify.com/)\n**Color:** ' + itemColor + '\n**Price:** ' + price + '\n**State:** ' + availability + '\n\n> QuickTask\n> [' + sizes + '](' + URL + ')';
    Color = 12726577
    Footer = '[SneakerAlpha]'
    embed = discord.Embed(title=itemName, description=Desc, url=URL, color=Color, timestamp=datetime.datetime.now())
    embed.set_thumbnail(url=imageURL)
    embed.set_footer(text=Footer)
    webhook.send(embed=embed, username='Sneaker Alphas')

switcher = {
    'T-Shirt': tshirts,
    'longsleeve': longSleeves,
    'Crewneck': crewnecks,
    'Hoodies': hoodies,
    'Pants': pants,
    'Jacket': jackets
}

pageNum = 0

while True:
    time.sleep(10)
    pageNum += 1
    request = requests.get('https://livevlonedievlone.myshopify.com/collections/all/products.json?limit=250&page=' + str(pageNum))

    decodedJson = request.json()

    if len(decodedJson['products']) == 0:
        pageNum = 0
        continue

    for product in decodedJson['products']:
        webhook = switcher.get(product['product_type'])

        try:
            ItemName, ItemColor = product['title'].split(' (')
        except ValueError:
            ItemName = product['title']
            ItemColor = ' '

        ItemColor = ItemColor[:-1]
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

        ItemPicture = product['images'][0]['src']
        ItemPrice = '$' + product['variants'][0]['price']
        ItemLink = 'https://livevlonedievlone.myshopify.com/products/' + product['handle']
        temp = SiteItem(ItemName, ItemColor, SoldOut)


        index = ExistsInList(temp)

        # If item already exists in list
        if index != -1:
            oldSoldOut = ItemList[index].SoldOut

            if SoldOut != oldSoldOut:
                if not SoldOut:
                    SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'RESTOCK', ItemLink, ItemPicture, sizeString, webhook)
                else:
                    SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'Sold Out', ItemLink, ItemPicture, sizeString, webhook)
                ItemList.pop(index)
                ItemList.append(temp)
        else:
            if not SoldOut:
                SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'In Stock', ItemLink, ItemPicture, sizeString, webhook)
            ItemList.append(temp)



    #print(decodedJson['products'][0]['title'])
    file = open('vlone_list.dat', 'wb')
    pickle.dump(ItemList, file)
    file.close()