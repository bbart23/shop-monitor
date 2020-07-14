import requests
import discord
import datetime
import pickle
import time
from os import path
from discord import Webhook, RequestsWebhookAdapter
from bs4 import BeautifulSoup
from siteItem import SiteItem

if path.exists('vlone_list.dat'):
    filehandler = open('vlone_list.dat', 'rb')
    ItemList = pickle.load(filehandler)
else:
    ItemList = []

VloneLinks = ['t-shirts', 'long-sleeves', 'jackets', 'hoodies', 'pants', 'jackets-1']
client = discord.Client()
URL = 'https://livevlonedievlone.myshopify.com/collections/'

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


def IsElementPresent(element):
    soldOut = element.find(class_='product-item__sold-out')
    if soldOut is None:
        return False
    return True


switcher = {
    't-shirts': tshirts,
    'long-sleeves': longSleeves,
    'jackets': crewnecks,
    'hoodies': hoodies,
    'pants': pants,
    'jackets-1': jackets
}

while True:
    for vlonelink in VloneLinks:
        webhook = switcher.get(vlonelink)
        page = requests.get(URL + vlonelink)
        print(URL + vlonelink)
        print('Looking at ' + vlonelink)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(class_='main-content')

        item_elems = results.find_all(class_='product-item__link-wrapper')
        for article in item_elems:
            ItemTitle = article.find(class_='product-item__title').text
            if ' (' in ItemTitle:
                ItemName, ItemColor = ItemTitle.split(' (')
                ItemColor = ItemColor[:-1]
            else:
                ItemName = ItemTitle
                ItemColor = ''
            print(ItemName)
            SoldOut = IsElementPresent(article)
            ItemLink = 'https://livevlonedievlone.myshopify.com' + article.find(class_='product-item__link').get('href')
            ItemPicture = 'https:' + article.find('img').get('src')
            ItemPrice = article.find(class_='product-item__price-wrapper').text
            #print(ItemPicture)

            temp = SiteItem(ItemName, ItemColor, SoldOut)
            index = ExistsInList(temp)
            if index != -1:
                oldSoldOut = ItemList[index].SoldOut
                oldPrice = ItemList[index].Price
                oldSizes = ItemList[index].Sizes

                if SoldOut != oldSoldOut:
                    if not SoldOut:
                        page2 = requests.get(ItemLink)
                        print(ItemLink)
                        soup2 = BeautifulSoup(page2.content, 'html.parser')
                        temp.Price = ItemPrice
                        sizeString = ''
                        if not SoldOut:
                            sizes = soup2.find(id='ProductSelect-product-template').find_all('option')
                            for size in sizes:
                                if 'Sold out' not in size.text:
                                    sizeText, price = str(size.text).split(' -')
                                    if sizeString == '':
                                        sizeString += sizeText
                                    else:
                                        sizeString += '|' + sizeText
                        temp.Sizes = sizeString
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
                if not SoldOut:
                    sizes = soup2.find(id='ProductSelect-product-template').find_all('option')
                    for size in sizes:
                        if 'Sold out' not in size.text:
                            sizeText, price = str(size.text).split(' -')
                            if sizeString == '':
                                sizeString += sizeText
                            else:
                                sizeString += '|' + sizeText
                temp.Sizes = sizeString
                ItemList.append(temp)
                if not SoldOut:
                    SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'In Stock', ItemLink, ItemPicture,
                                       sizeString, webhook)

    file = open('vlone_list.dat', 'wb')
    pickle.dump(ItemList, file)
    file.close()
    time.sleep(10)