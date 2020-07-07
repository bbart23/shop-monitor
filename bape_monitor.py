import requests
import discord
import datetime
import pickle
from os import path
from discord import Webhook, RequestsWebhookAdapter
from bs4 import BeautifulSoup
from siteItem import SiteItem

if path.exists('bape_list.dat'):
    filehandler = open('bape_list.dat', 'rb')
    ItemList = pickle.load(filehandler)
else:
    ItemList = []

BapeLinks = ['t-shirts', 'cutandsewn', 'shirts', 'knit', 'jacket', 'pants', 'footwear', 'goods']
client = discord.Client()
URL = 'https://us.bape.com/collections/all/'

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

tshirts = Webhook.from_url(tshirtsHook, adapter=RequestsWebhookAdapter())
cutandsewn = Webhook.from_url(cutandsewnHook, adapter=RequestsWebhookAdapter())
shirts = Webhook.from_url(shirtsHook, adapter=RequestsWebhookAdapter())
knit = Webhook.from_url(knitHook, adapter=RequestsWebhookAdapter())
jacket = Webhook.from_url(jacketHook, adapter=RequestsWebhookAdapter())
pants = Webhook.from_url(pantsHook, adapter=RequestsWebhookAdapter())
footwear = Webhook.from_url(footwearHook, adapter=RequestsWebhookAdapter())
goods = Webhook.from_url(goodsHook, adapter=RequestsWebhookAdapter())

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


def IsElementPresent(element):
    soldOut = element.find(class_='SoldOut')
    if soldOut is None:
        return False
    return True


switcher = {
    't-shirts': tshirts,
    'cutandsewn': cutandsewn,
    'shirts': shirts,
    'knit': knit,
    'jacket': jacket,
    'pants': pants,
    'footwear': footwear,
    'goods': goods
}

while True:
    for bapelink in BapeLinks:
        pageNum = 1
        webhook = switcher.get(bapelink)
        page = requests.get(URL + bapelink)
        print(URL + bapelink)
        while(True):
            print('Looking at ' + bapelink + ' Page ' + str(pageNum))
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find(class_='row product-row')

            item_elems = results.find_all(class_='thumb col-xs-6 col-sm-4')
            for article in item_elems:
                ItemName = article.find(class_='product-name').text
                #print(ItemName)
                #ItemColor = article.find(class_='product-style').find(class_='name-link').text
                SoldOut = IsElementPresent(article)
                ItemLink = 'https://us.bape.com/' + article.get('href')
                ItemPicture = 'https:' + article.find('img').get('src')
                ItemPrice = article.find(class_='money').get('aria-label')
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
                            temp.Price = ItemPrice
                            sizeString = ''
                            colorString = ''
                            variants = soup2.find(id='variants').find_all('li')
                            for variant in variants:
                                if variant.find(class_='sold_out') is None:
                                    label = variant.find('label').text
                                    id, color, size = label.split(' / ')
                                    if sizeString == '':
                                        sizeString += size
                                    else:
                                        sizeString += '|' + size
                                    if colorString == '':
                                        colorString += color
                                    else:
                                        colorString += '|' + color
                            temp.Sizes = sizeString
                            temp.Color = colorString
                            ItemColor = colorString
                            SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'RESTOCK', ItemLink, ItemPicture, sizeString,
                                               webhook)
                        else:
                            SendDiscordMessage(ItemName, ItemColor, oldPrice, 'Sold Out', ItemLink, ItemPicture, '',
                                               webhook)
                        ItemList.pop(index)
                        ItemList.append(temp)
                else:
                    page2 = requests.get(ItemLink)
                    soup2 = BeautifulSoup(page2.content, 'html.parser')
                    temp.Price = ItemPrice
                    sizeString = ''
                    colorString = ''
                    if not SoldOut:
                        variants = soup2.find(id='variants').find_all('li')
                        for variant in variants:
                            if variant.find(class_='sold_out') is None:
                                label = variant.find('label').text
                                id, color, size = label.split(' / ')
                                if size not in sizeString:
                                    if sizeString == '':
                                        sizeString += size
                                    else:
                                        sizeString += '|' + size
                                if color not in colorString:
                                    if colorString == '':
                                        colorString += color
                                    else:
                                        colorString += '|' + color
                    temp.Sizes = sizeString
                    temp.Color = colorString
                    ItemColor = colorString
                    ItemList.append(temp)
                    if not SoldOut:
                        SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'In Stock', ItemLink, ItemPicture,
                                           sizeString, webhook)
            nextLinkDisabled = soup.find(class_='next disabled')
            nextLinkEnabled = soup.find(class_='next')
            if nextLinkDisabled is None and nextLinkEnabled is not None:
                nextLink = soup.find(class_='next').find('a').get('href')
                page = requests.get('https://us.bape.com' + nextLink)
                pageNum += 1
            else:
                break
    file = open('bape_list.dat', 'wb')
    pickle.dump(ItemList, file)
    file.close()