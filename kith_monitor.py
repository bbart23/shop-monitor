import requests
import pickle
import discord
import datetime
import time
import re
from discord import Webhook, RequestsWebhookAdapter
from siteItem import SiteItem
from os import path

if path.exists('kith_list.dat'):
    filehandler = open('kith_list.dat', 'rb')
    ItemList = pickle.load(filehandler)
else:
    ItemList = []

teesHook = 'https://discordapp.com/api/webhooks/735546285670793286/L-xeCHvD3cVAJcmKT3tY02VmRn8tdC7yKHUzcbgFGw-fOA4mn3m2tIeZoSYd7LtNTRzk'
crewnecksHook = 'https://discordapp.com/api/webhooks/735546415572320318/tSJyCVZIfUhzUqlUkH_RVn1kQdSwsXvUREJe6rP1grF_c4qSB3MG0chJlz9irat-1aNV'
headwearHook = 'https://discordapp.com/api/webhooks/735546525035397181/7qtY0IQ772olXqrGkvXsjvwPAW3o4k0St68M30MHYjeo-dhOtnZogMjXCEDi1PvmR5zW'
hoodiesHook = 'https://discordapp.com/api/webhooks/735546643075825745/w6p9jK_b5V8tlT43V7Jl-jrJQpu-jXASoDA3COy4JYlL05P1_AypbY6lVIi8gh8lV6qc'
outerwearHook = 'https://discordapp.com/api/webhooks/735546768749756570/ku87ASQtE3zjodReKiWsJrHUu__A2gmsC92ezh1wZMvZys9CuxhK6-zEycm8ACgsD7kq'
pantsHook = 'https://discordapp.com/api/webhooks/735546846545576038/mDH30yvrYH7QUzZgi3lGdEfIBYC6490rnHWYMiv61lzff-BIfaPhOjRZoZUGwNQ0wsvL'
shortsHook =  'https://discordapp.com/api/webhooks/735546928590356534/r4P0-WH7Or-k4giqu7Gqh1vN_Hm23PsYZGHFv-sRYQw3sllcYLa-O1zfDS6ejewNw27a'
sneakersHook = 'https://discordapp.com/api/webhooks/735547061201535009/qkQ3Zlf2aLRafaNI6qUR4SF8_qdE4sOGboKTZx9wJGTWaqhpMFYdGxm0V9xJ-rMYA2Qo'
socksHook = 'https://discordapp.com/api/webhooks/735547216629989408/ACqfDINlt-jeBus89zUa7-SQxhAX-VspzdZNUDHdzoROe_gXsakAFRI9chRQZOu30mCf'
lifestyleHook = 'https://discordapp.com/api/webhooks/735547299027091598/-IEBz93lzehLn-Dz-mUThTeSqG4fotpXnmzaepggnGB7P_S2505XzzyQhDyh-mqDsa8G'
accessoriesHook = 'https://discordapp.com/api/webhooks/735547411354746921/PWR76VpUXTL9UqcubEHV6cZspUijmosZrF8IgwbKniN0F7d2dkxJeajNoMPncoykCwHb'
buttonupsHook = 'https://discordapp.com/api/webhooks/735547485103063084/ScptREN_rv8JFoOLDDtBEi_SicAxjNR3uvJ8Nj_JAn2lfwFpNVv9wqTlqi4RTwOe-HaK'
onesiesHook = 'https://discordapp.com/api/webhooks/735547580338929666/MVttJsiwzzb8kT4-1dhMjp1fhbkOHwqzTvdobQDjVnhCCRnh1MjEdObi3MO0pvtxTbdw'

tees = Webhook.from_url(teesHook, adapter=RequestsWebhookAdapter())
crewnecks = Webhook.from_url(crewnecksHook, adapter=RequestsWebhookAdapter())
headwear = Webhook.from_url(headwearHook, adapter=RequestsWebhookAdapter())
hoodies = Webhook.from_url(hoodiesHook, adapter=RequestsWebhookAdapter())
outerwear = Webhook.from_url(outerwearHook, adapter=RequestsWebhookAdapter())
pants = Webhook.from_url(pantsHook, adapter=RequestsWebhookAdapter())
shorts = Webhook.from_url(shortsHook, adapter=RequestsWebhookAdapter())
sneakers = Webhook.from_url(sneakersHook, adapter=RequestsWebhookAdapter())
socks = Webhook.from_url(socksHook, adapter=RequestsWebhookAdapter())
lifestyle = Webhook.from_url(lifestyleHook, adapter=RequestsWebhookAdapter())
accessories = Webhook.from_url(accessoriesHook, adapter=RequestsWebhookAdapter())
buttonups = Webhook.from_url(buttonupsHook, adapter=RequestsWebhookAdapter())
onesies = Webhook.from_url(onesiesHook, adapter=RequestsWebhookAdapter())

def ExistsInList(item):
    ind = -1
    for Item in ItemList:
        ind += 1
        if Item.Name == item.Name and Item.Color == item.Color:
            return ind
    return -1

def SendDiscordMessage(itemName, itemColor, price, availability, URL, imageURL, sizes, webhook):
    Desc = '**Shop:** [Kith Monday Program (US)](https://kith.com/collections/kith-monday-program/)\n**Color:** ' + itemColor + '\n**Price:** ' + price + '\n**State:** ' + availability + '\n\n> QuickTask\n> [' + sizes + '](' + URL + ')';
    Color = 12726577
    Footer = '[SneakerAlpha]'
    embed = discord.Embed(title=itemName, description=Desc, url=URL, color=Color, timestamp=datetime.datetime.now())
    embed.set_thumbnail(url=imageURL)
    embed.set_footer(text=Footer)
    webhook.send(embed=embed, username='Sneaker Alphas')

switcher = {
    'tees': tees,
    'tops': tees,
    'dresses': tees,
    'tank tops': tees,
    'crewnecks': crewnecks,
    'headwear': headwear,
    'hoodies': hoodies,
    'outerwear': outerwear,
    'pants': pants,
    'bottoms': pants,
    'shorts': shorts,
    'swim': shorts,
    'sneakers': sneakers,
    'sneaker': sneakers,
    'boots': sneakers,
    'sandals': sneakers,
    'socks': socks,
    'lifestyle': lifestyle,
    'accessories': accessories,
    'jewelry': accessories,
    'bags': accessories,
    'button ups': buttonups,
    'onesies': onesies,
    'one piece': onesies,
    'bodysuit': onesies
}

pageNum = 0
collectionLink = 'https://kith.com/'

while True:
    time.sleep(10)

    pageNum += 1

    request = requests.get(collectionLink + 'products.json?limit=250&page=' + str(pageNum))

    decodedJson = request.json()

    if len(decodedJson['products']) == 0:
        pageNum = 0
        continue

    for product in decodedJson['products']:
        webhook = switcher.get(product['product_type'].lower())

        ItemName = product['title']
        ItemColor = product['handle']
        #print(ItemName)
        SoldOut = True
        sizeString = ''
        for variant in product['variants']:
            #print(variant['available'])
            if variant['available'] == True:
                SoldOut = False
                if sizeString == '':
                    sizeString += variant['title']
                else:
                    sizeString += '|' + variant['title']

        ItemPicture = product['images'][0]['src']
        ItemPrice = '$' + product['variants'][0]['price']
        ItemLink = 'https://kith.com/products/' + product['handle']
        temp = SiteItem(ItemName, ItemColor, SoldOut)


        index = ExistsInList(temp)

        # If item already exists in list
        if index != -1:
            oldSoldOut = ItemList[index].SoldOut

            if SoldOut != oldSoldOut:
                if not SoldOut:
                    try:
                        SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'RESTOCK', ItemLink, ItemPicture, sizeString,
                                           webhook)
                        print('[RESTOCK]' + ItemName)
                    except:
                        print('ERROR: Couldn\'t send message. Product Type: ' + product['product_type'].lower())
                else:
                    try:
                        SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'Sold Out', ItemLink, ItemPicture,
                                           sizeString, webhook)
                        print('[SOLD OUT]' + ItemName)
                    except:
                        print('ERROR: Couldn\'t send message. Product Type: ' + product['product_type'].lower())
                ItemList.pop(index)
                ItemList.append(temp)
        else:
            if not SoldOut:
                try:
                    SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'In Stock', ItemLink, ItemPicture, sizeString,
                                       webhook)
                    print('[IN STOCK]' + ItemName)
                except:
                    print('ERROR: Couldn\'t send message. Product Type: ' + product['product_type'].lower())
            ItemList.append(temp)



    #print(decodedJson['products'][0]['title'])
    file = open('kith_list.dat', 'wb')
    pickle.dump(ItemList, file)
    file.close()