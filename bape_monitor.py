import requests
import pickle
import discord
import datetime
import time
import re
from discord import Webhook, RequestsWebhookAdapter
from siteItem import SiteItem
from os import path

if path.exists('bape_list.dat'):
    filehandler = open('bape_list.dat', 'rb')
    ItemList = pickle.load(filehandler)
else:
    ItemList = []

tshirtsHook = 'https://discordapp.com/api/webhooks/730133226634608672' \
              '/kyq30fQu7dXBatftLKQk94uaeTDzmEgz2Jig0trNQxv_SAlVPIjefMbgrw9-EWEOLkrT '
cutandsewnHook = 'https://discordapp.com/api/webhooks/730133674674356254' \
                 '/NQy2HeUaSt6cNrmRgFiWLJzBrIZmNppSPvuMYsaKJH99GikZfIx5vYQuAE_DvfMenCQm '
shirtsHook = 'https://discordapp.com/api/webhooks/730133804202721291/MjaHqd4R-2AD9521X8dFPvn7NtYd2ZBtVgIrkQRFQzOFWP3' \
             '-VPzuNQXmi5di6ZyAtPaY '
knitHook = 'https://discordapp.com/api/webhooks/730133876776763584/lbIWiCS7DMxFM2_Dz72bt7748vy4KOYsLAE2BYV4w' \
           '-CamT1w_UT-HxrJxpARN8U4k_Fv '
jacketHook = 'https://discordapp.com/api/webhooks/730134013406085201' \
             '/xezEAr2tOx3qIs1_pzhbxqM9JNMaEOo9nsaI76oLGmRmkxhwk4Fx6NgsV3aOS911IM-O '
pantsHook = 'https://discordapp.com/api/webhooks/730134145237254165/uPU3XqsHUfeTQlcO8qW7UuQtpx' \
            '-Al3_D7NSxbCGeigcKabUBWhWQUs06LodyGW1ivBGq '
footwearHook = 'https://discordapp.com/api/webhooks/730134207908675695' \
               '/ewz_1F91xXWGoul_f2WTlEdp0iIB76ObljFLaCCvohHUvkPhddIX3Apa-9s1T1_oAz6R '
goodsHook = 'https://discordapp.com/api/webhooks/730134284735610941/nAxh8tn9QJuobsaOaC-NKFYlX_Uyns3iQF5nq5AXBRAZojqj8' \
            '-yCX80LP6Sxa-lMeLQv '
ladiesHook = 'https://discordapp.com/api/webhooks/735653385453174887' \
             '/Nh3cigGkVQwtViKIsaexnQ7BntrrMfY08m75GQWszCjHRbHje63lNLKNoECULwHbD9fd '
kidsHook = 'https://discordapp.com/api/webhooks/735653499726987347' \
           '/-shAm1Tv73af3ybU2A5IKm5LU4aVLlBJG_UdL1cyeRo5eBpWhEKtu7q89b6mqxtf1gQJ '

tshirts = Webhook.from_url(tshirtsHook, adapter=RequestsWebhookAdapter())
cutandsewn = Webhook.from_url(cutandsewnHook, adapter=RequestsWebhookAdapter())
shirts = Webhook.from_url(shirtsHook, adapter=RequestsWebhookAdapter())
knit = Webhook.from_url(knitHook, adapter=RequestsWebhookAdapter())
jacket = Webhook.from_url(jacketHook, adapter=RequestsWebhookAdapter())
pants = Webhook.from_url(pantsHook, adapter=RequestsWebhookAdapter())
footwear = Webhook.from_url(footwearHook, adapter=RequestsWebhookAdapter())
goods = Webhook.from_url(goodsHook, adapter=RequestsWebhookAdapter())
ladies = Webhook.from_url(ladiesHook, adapter=RequestsWebhookAdapter())
kids = Webhook.from_url(kidsHook, adapter=RequestsWebhookAdapter())

def ExistsInList(item):
    ind = -1
    for Item in ItemList:
        ind += 1
        if Item.Name == item.Name:
            return ind
    return -1

def SendDiscordMessage(itemName, itemColor, price, availability, URL, imageURL, sizes, webhook):
    Desc = '**Shop:** [Bape (US)](https://us.bape.com/collections/all)\n**Color:** ' + itemColor + '\n**Price:** ' + price + '\n**State:** ' + availability + '\n\n> QuickTask\n> [' + sizes + '](' + URL + ')';
    Color = 12726577
    Footer = '[SneakerAlpha]'
    embed = discord.Embed(title=itemName, description=Desc, url=URL, color=Color, timestamp=datetime.datetime.now())
    embed.set_thumbnail(url=imageURL)
    embed.set_footer(text=Footer)
    webhook.send(embed=embed, username='Sneaker Alphas')

switcher = {
    'T-SHIRTS': tshirts,
    'CUT AND SEWN': cutandsewn,
    'SHIRTS': shirts,
    'KNIT': knit,
    'JACKETS': jacket,
    'PANTS': pants,
    'SHOES': footwear,
    'FOOTWEAR': footwear,
    'Footwear': footwear,
    "LADIES'": ladies,
    'KIDS': kids,
    'MENS': goods,
    'GOODS': goods
}

pageNum = 0

while True:
    time.sleep(2)
    pageNum += 1
    request = requests.get('https://us.bape.com/collections/all/products.json?limit=250&page=' + str(pageNum))

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
        colorString = ''
        for variant in product['variants']:
            #print(variant['available'])
            if variant['available'] == True:
                SoldOut = False
                color = variant['option2']
                size = variant['option3']
                if color not in colorString:
                    if colorString == '':
                        colorString += color
                    else:
                        colorString += '|' + color
                if size not in sizeString:
                    if sizeString == '':
                        sizeString += size
                    else:
                        sizeString += '|' + size

        ItemColor = colorString
        if product['variants'][0]['featured_image'] is not None:
            ItemPicture = product['variants'][0]['featured_image']['src']
        else:
            ItemPicture = product['images'][0]['src']
        ItemPrice = '$' + product['variants'][0]['price']
        ItemLink = 'https://us.bape.com/collections/all/products/' + product['handle']
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
    file = open('bape_list.dat', 'wb')
    pickle.dump(ItemList, file)
    file.close()