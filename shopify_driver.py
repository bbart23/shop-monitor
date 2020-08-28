import requests
import pickle
import discord
import datetime
import time
import re
from discord import Webhook, RequestsWebhookAdapter
from siteItem import SiteItem
from os import path

jordanHook = 'https://discordapp.com/api/webhooks/739924749127516291/Q3rX5AenW1d9E7vB9BA8HBncLmk8u0Y2z3zHR9mMjKqpUZTI_sDqyRl4xM_HN9gatMJk'
yeezyHook = 'https://discordapp.com/api/webhooks/739927902786945105/TnD1CAjmWdJHj5AEiIsbq1SmEr1kD92z6l37qCdBKTuI67_YErcgFSM8buui2cSoMNo1'
nikesbHook = 'https://discordapp.com/api/webhooks/739927996391227493/oZdCOwhdb7uErLSiujwz452Cyja6Fg1lw_1li_25D190BmKrTuSsO0wdmW0uiG90Grip'

jordan = Webhook.from_url(jordanHook, adapter=RequestsWebhookAdapter())
yeezy = Webhook.from_url(yeezyHook, adapter=RequestsWebhookAdapter())
nikesb = Webhook.from_url(nikesbHook, adapter=RequestsWebhookAdapter())

def FileCheck(filename):
    global ItemList
    if path.exists(filename):
        filehandler = open(filename, 'rb')
        ItemList = pickle.load(filehandler)
    else:
        ItemList = []

def FileWrite(filename):
    #print(decodedJson['products'][0]['title'])
    file = open(filename, 'wb')
    pickle.dump(ItemList, file)
    file.close()


def ExistsInList(item):
    ind = -1
    for Item in ItemList:
        ind += 1
        if Item.Name == item.Name and Item.Color == item.Color:
            return ind
    return -1

def SendDiscordMessage(itemName, itemColor, price, availability, URL, imageURL, sizes, webhook, storeName, storeLink):
    Desc = '**Shop:** [' + storeName + '](' + storeLink + ')\n**Price:** ' + price + '\n**State:** ' + availability + '\n\n> QuickTask\n> [' + sizes + '](' + URL + ')';
    Color = 12726577
    Footer = '[SneakerAlpha]'
    embed = discord.Embed(title=itemName, description=Desc, url=URL, color=Color, timestamp=datetime.datetime.now())
    embed.set_thumbnail(url=imageURL)
    embed.set_footer(text=Footer)
    webhook.send(embed=embed, username='Sneaker Alphas')


#brands = ['adidas', 'jordan', 'play', 'butter', 'nike', 'y-3', 'yeezy', 'white']
pageNum = 0

def ScanStore(filename, collectionLink, webhook, sizeOption, productLink, storeName):
    global pageNum
    print('Scanning Store: ' + storeName)
    while True:
        time.sleep(2)
        pageNum += 1

        FileCheck(filename)

        request = requests.get(collectionLink + 'products.json?limit=250&page=' + str(pageNum))
        try:
            decodedJson = request.json()
        except Exception:
            print('[ERROR] Unable to parse JSON!!')
            return

        if len(decodedJson['products']) == 0:
            pageNum = 0
            return

        for product in decodedJson['products']:

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
                    size = variant[sizeOption]
                    if sizeOption == 'option2':
                        if size is None:
                            size = variant['option1']
                    if size is None:
                        size = 'F'
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
            ItemLink = productLink + product['handle']
            temp = SiteItem(ItemName, ItemColor, SoldOut)


            index = ExistsInList(temp)

            # If item already exists in list
            if index != -1:
                oldSoldOut = ItemList[index].SoldOut

                if SoldOut != oldSoldOut:
                    if not SoldOut:
                        try:
                            SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'RESTOCK', ItemLink, ItemPicture, sizeString, webhook, storeName, collectionLink)
                            print('[RESTOCK]' + ItemName)
                            if 'jordan' in ItemName.lower():
                                SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'RESTOCK', ItemLink, ItemPicture,
                                                   sizeString, jordan, storeName, collectionLink)
                            if 'yeezy' in ItemName.lower():
                                SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'RESTOCK', ItemLink, ItemPicture,
                                                   sizeString, yeezy, storeName, collectionLink)
                            if 'nike' in ItemName.lower() and ('sb' in ItemName.lower() or 'dunk' in ItemName.lower()):
                                SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'RESTOCK', ItemLink, ItemPicture,
                                                   sizeString, nikesb, storeName, collectionLink)
                        except:
                            print('ERROR: Couldn\'t send message. Product Type: '+ product['product_type'].lower())
                    else:
                        try:
                            SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'Sold Out', ItemLink, ItemPicture, sizeString, webhook, storeName, collectionLink)
                            print('[SOLD OUT]' + ItemName)
                            if 'jordan' in ItemName.lower():
                                SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'Sold Out', ItemLink, ItemPicture,
                                                   sizeString, jordan, storeName, collectionLink)
                            if 'yeezy' in ItemName.lower():
                                SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'Sold Out', ItemLink, ItemPicture,
                                                   sizeString, yeezy, storeName, collectionLink)
                            if 'nike' in ItemName.lower() and ('sb' in ItemName.lower() or 'dunk' in ItemName.lower()):
                                SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'Sold Out', ItemLink, ItemPicture,
                                                   sizeString, nikesb, storeName, collectionLink)
                        except:
                            print('ERROR: Couldn\'t send message. Product Type: '+ product['product_type'].lower())
                    ItemList.pop(index)
                    ItemList.append(temp)
            else:
                if not SoldOut:
                    try:
                        SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'In Stock', ItemLink, ItemPicture, sizeString, webhook, storeName, collectionLink)
                        print('[IN STOCK]' + ItemName)
                        if 'jordan' in ItemName.lower():
                            SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'In Stock', ItemLink, ItemPicture,
                                               sizeString, jordan, storeName, collectionLink)
                        if 'yeezy' in ItemName.lower():
                            SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'In Stock', ItemLink, ItemPicture,
                                               sizeString, yeezy, storeName, collectionLink)
                        if 'nike' in ItemName.lower() and ('sb' in ItemName.lower() or 'dunk' in ItemName.lower()):
                            SendDiscordMessage(ItemName, ItemColor, ItemPrice, 'In Stock', ItemLink, ItemPicture,
                                               sizeString, nikesb, storeName, collectionLink)
                    except:
                        print('ERROR: Couldn\'t send message. Product Type: ' + product['product_type'].lower())
                ItemList.append(temp)

        FileWrite(filename)

maniereHook = 'https://discordapp.com/api/webhooks/738121189905531081/w9-I5CM8-MLLd-TZVhMC2osILd0zNq7lMSKZ8vWGdCeTRKag0IFsUNSV5Nz9YjDCbHxz'
maniere = Webhook.from_url(maniereHook, adapter=RequestsWebhookAdapter())
antiSocialHook = 'https://discordapp.com/api/webhooks/737764108216041592/tJFSnD-eEE14WvMMJU4l2vOmfPBSlKXv2C0-xoT-vTwqu4JDrc8eY0ezQq2jwmuN3YXI'
antiSocial = Webhook.from_url(antiSocialHook, adapter=RequestsWebhookAdapter())
chinatownHook = 'https://discordapp.com/api/webhooks/740627195931918438/D1Yro9O842AxsZWeOtxRlwdveG6mY4skcZX7zafHGXDCRsaEmFQB4pWxwD3QmJB7xOqG'
chinatown = Webhook.from_url(chinatownHook, adapter=RequestsWebhookAdapter())
darksideHook = 'https://discordapp.com/api/webhooks/739913765440585860/rmy8esWS3S4vRI8AmnMi-GYoRCClSpZ5Ri3Ugyui2TUoGTOQiEZDNnJR-1vbr3viMuV5'
darkside = Webhook.from_url(darksideHook, adapter=RequestsWebhookAdapter())
dopefactoryHook = 'https://discordapp.com/api/webhooks/743207984930488380/pI3rF0NJfJribAYwBzESqWntwQFTtfsfB06y63a99h8L2WBdIX8rWmxA9saZqaSeJI1W'
dopefactory = Webhook.from_url(dopefactoryHook, adapter=RequestsWebhookAdapter())
extrabutterHook = 'https://discordapp.com/api/webhooks/738473993438363789/QFRvfT1BbVsFcrcLhmfn_YYTbjparZ3TWqx4N0zkX9upwEYZmhiO3pStOaiQKqa0mjDJ'
extrabutter = Webhook.from_url(extrabutterHook, adapter=RequestsWebhookAdapter())
limitededtHook = 'https://discordapp.com/api/webhooks/739179663645212704/1WjlOarQ9hivXVZBE06Ff1E4nrFJKfr-BuYuoI00wlLncavLYa6djeO42mFhshqYbjFX'
limitededt = Webhook.from_url(limitededtHook, adapter=RequestsWebhookAdapter())
nrmlHook = 'https://discordapp.com/api/webhooks/739904371415842816/hmusKhBpaSFHkqoJonT07E5uI6eB5PKylF1sGziIoVgCJDTEk3XLh4yl3AYjE6otmwVp'
nrml = Webhook.from_url(nrmlHook, adapter=RequestsWebhookAdapter())
ricchezzaHook = 'https://discordapp.com/api/webhooks/739885942470344874/OMffBbI7ibHqXR9WS0tTo2jLoCvhAJ_IiPqy5Bzx6CArutDj500Hv528xpK99Nsjz6p5'
ricchezza = Webhook.from_url(ricchezzaHook, adapter=RequestsWebhookAdapter())
rockcityHook = 'https://discordapp.com/api/webhooks/740655074300133476/stU5T1rOAg03_lWCWIDMnpClv53k7WoBHdkIkGe2e4tVGjeEBkSfQLBtNr_d6x-H-chs'
rockcity = Webhook.from_url(rockcityHook, adapter=RequestsWebhookAdapter())
rsvpHook = 'https://discordapp.com/api/webhooks/739902068973895700/zsNjxBOZEgPxA3pFElyIMq6X8CPeCnLSzoywaTQuSuDYsoouWpTx4iT2nDD5SlCdOJNh'
rsvp = Webhook.from_url(rsvpHook, adapter=RequestsWebhookAdapter())
saintalfredHook = 'https://discordapp.com/api/webhooks/739909910577414247/OGqr4QpMKSQqfXITpJ6MP76XN8Q-PNW_Jyr1clai_kjfJpfOGW3MWN92kDdCFzskzqox'
saintalfred = Webhook.from_url(saintalfredHook, adapter=RequestsWebhookAdapter())
shoegalleryHook = 'https://discordapp.com/api/webhooks/742804665275514970/LBvodsAs6B724HUt6aSHVR3IZL4jXcMteUfmNdIsK3zgaqMq8ClPQJuGzpDUbxm28aos'
shoegallery = Webhook.from_url(shoegalleryHook, adapter=RequestsWebhookAdapter())
sneakerpoliticsHook = 'https://discordapp.com/api/webhooks/742829381562662943/KPXKinvET4LW6by4i_qi3iO_ijhSV4Cwzw3BDsxT59oKYvzZ1OeCE93M7JgNFL3C_32L'
sneakerpolitics = Webhook.from_url(sneakerpoliticsHook, adapter=RequestsWebhookAdapter())
socialstatusHook = 'https://discordapp.com/api/webhooks/738127814171164713/QdUyGB9w27UYnsSlsdsy1_RmDMBM07rWIB4yRwqYQ-6LLBanFR-JYdswyYVnI6O_kKte'
socialstatus = Webhook.from_url(socialstatusHook, adapter=RequestsWebhookAdapter())
soleclassicsHook = 'https://discordapp.com/api/webhooks/738518545939562527/2Rn8iQiQDiTF5NGhseUCmlgrmG69SXxjoCkGBLSpOS3hL2bzmf0XZUVX88rdfLUled42'
soleclassics = Webhook.from_url(soleclassicsHook, adapter=RequestsWebhookAdapter())
closetHook = 'https://discordapp.com/api/webhooks/739907399355334727/tCNa2sT13rnoIu7fXexFq6aQCsJX6Zes3X519KT4y_0lx0ynohitiX9bl-NmAT0GswGX'
closet = Webhook.from_url(closetHook, adapter=RequestsWebhookAdapter())
travisscottHook = 'https://discordapp.com/api/webhooks/738459296471318639/0iQPrN6fK9L6Q3tAZfysk1s5aTjMPHBbBoI49A65QpqgQscshrVUbNycQvAhsxrBNauQ'
travisscott = Webhook.from_url(travisscottHook, adapter=RequestsWebhookAdapter())
undefeatedHook = 'https://discordapp.com/api/webhooks/739893659197112340/Kp0QOzLZdlxE0cxnA3Qxq3SVf2PWZPh9-xRmUzlck2_1rH1Ttwf6-SO7RG6aolmjyV1v'
undefeated = Webhook.from_url(undefeatedHook, adapter=RequestsWebhookAdapter())
unknwnHook = 'https://discordapp.com/api/webhooks/739897838485504062/gl8nmURdIqG_M8FUQ_eWTCgmzujuXPxcoR1jE8rrVGjomnp2rORMydmLDTY0B7KD1bf7'
unknwn = Webhook.from_url(unknwnHook, adapter=RequestsWebhookAdapter())
westnycHook = 'https://discordapp.com/api/webhooks/739919591328841798/s4ynbBbgY_N2rGXffv__V5GVJ7M0DDd9HkzrdP2nI200d9q0NycAd2CT3B9v9PAbNV7y'
westnyc = Webhook.from_url(westnycHook, adapter=RequestsWebhookAdapter())
nicekicksHook = 'https://discordapp.com/api/webhooks/746775193065619488/ACBqChtw6fbtPQMg0hcZZAo8wd8W-2vlDlyAD2QLnWPrk1l66tH-t0rdv6xfIho1sYJJ'
nicekicks = Webhook.from_url(nicekicksHook, adapter=RequestsWebhookAdapter())
unionlosangelesHook = 'https://discordapp.com/api/webhooks/748980041962225674/4IhrElPMYVgj1DGNXNuI6WpKqlNhIl2B9NJA8bWn4n1_tm6ifKGUNTv0u6w3deYWHt3g'
unionlosangeles = Webhook.from_url(unionlosangelesHook, adapter=RequestsWebhookAdapter())

while True:
    try:
        ScanStore('amamaniere_list.dat', 'https://www.a-ma-maniere.com/collections/sneakers/', maniere, 'option2',
                'https://www.a-ma-maniere.com/products/', 'A Ma Maniere (US)')
    except Exception as e:
        print('Failed: ' + e)
    try:
        ScanStore('antisocial_list.dat', 'https://www.antisocialsocialclub.com/', antiSocial, 'option1',
                  'https://www.antisocialsocialclub.com/products/', 'Anti Social Social Club (US)')
    except Exception as e:
        print('Failed: ' + e)
    try:
        ScanStore('chinatown_list.dat', 'https://thechinatownmarket.com/', chinatown, 'option2',
                  'https://thechinatownmarket.com/products/', 'Chinatown Market (US)')
    except Exception as e:
        print('Failed: ' + e)
    try:
        ScanStore('darkside_list.dat', 'https://www.thedarksideinitiative.com/collections/footwear/', darkside, 'option1',
                  'https://www.thedarksideinitiative.com/collections/footwear/products/', 'The Darkside Initiative (US)')
    except Exception as e:
        print('Failed: ' + e)
    try:
        ScanStore('dopefactory_list.dat', 'https://www.dope-factory.com/collections/sneakers/', dopefactory, 'option1',
                  'https://www.dope-factory.com/products/', 'Dope Factory (US)')
    except Exception as e:
        print('Failed: ' + e)
    try:
        ScanStore('extrabutter_list.dat', 'https://extrabutterny.com/collections/footwear/', extrabutter, 'option1',
                  'https://extrabutterny.com/collections/footwear/products/', 'Extra Butter (US)')
    except Exception as e:
        print('Failed: ' + e)
    try:
        ScanStore('limitededt_list.dat', 'https://limitededt.com/collections/mens/', limitededt, 'option1',
                  'https://limitededt.com/collections/mens/products/', 'Limited Edt (US)')
    except Exception as e:
        print('Failed: ' + e)
    try:
        ScanStore('nrml_list.dat', 'https://nrml.ca/collections/mens-footwear/', nrml, 'option1',
                  'https://nrml.ca/collections/mens-footwear/products/', 'NRML (CA)')
    except Exception as e:
        print('Failed: ' + e)
    try:
        ScanStore('ricchezza_list.dat', 'https://ricchezzaforever.com/collections/all/', ricchezza, 'option1',
                  'https://ricchezzaforever.com/collections/all/products/', 'Ricchezza (US)')
    except Exception as e:
        print('Failed: ' + e)
    try:
        ScanStore('rockcity_list.dat', 'https://rockcitykicks.com/collections/sn/', rockcity, 'option1',
                  'https://rockcitykicks.com/collections/sn/products/', 'Rock City Kicks (US)')
    except Exception as e:
        print('Failed: ' + e)
    try:
        ScanStore('rsvpgallery_list.dat', 'https://rsvpgallery.com/collections/footwear/', rsvp, 'option1',
                  'https://rsvpgallery.com/collections/footwear/products/', 'RSVP Gallery (US)')
    except Exception as e:
        print('Failed: ' + e)
    try:
        ScanStore('saintalfred_list.dat', 'https://www.saintalfred.com/collections/footwear/', saintalfred, 'option1',
                  'https://www.saintalfred.com/collections/footwear/products/', 'Saint Alfred (US)')
    except Exception as e:
        print('Failed: ' + e)
    try:
        ScanStore('shoegallery_list.dat', 'https://shoegallerymiami.com/', shoegallery, 'option1',
                  'https://shoegallerymiami.com/products/', 'Shoe Gallery Miami (US)')
    except Exception as e:
        print('Failed: ' + e)
    try:
        ScanStore('sneakerpolitics_list.dat', 'https://sneakerpolitics.com/', sneakerpolitics, 'option1',
                  'https://sneakerpolitics.com/products/', 'Sneaker Politics (US)')
    except Exception as e:
        print('Failed: ' + e)
    try:
        ScanStore('socialstatus_list.dat', 'https://www.socialstatuspgh.com/collections/sneakers/', socialstatus, 'option2',
                  'https://www.socialstatuspgh.com/collections/sneakers/products/', 'Social Status (US)')
    except Exception as e:
        print('Failed: ' + e)
    try:
        ScanStore('soleclassics_list.dat', 'https://soleclassics.com/collections/shoes/', soleclassics, 'option1',
                  'https://soleclassics.com/collections/shoes/products/', 'Sole Classics (US)')
    except Exception as e:
        print('Failed: ' + e)
    try:
        ScanStore('thecloset_list.dat', 'https://www.theclosetinc.com/collections/mens-footwear/', closet, 'option1',
                  'https://www.theclosetinc.com/collections/mens-footwear/products/', 'The Closet Inc (CA)')
    except Exception as e:
        print('Failed: ' + e)
    try:
        ScanStore('travisscott_list.dat', 'https://shop.travisscott.com/', travisscott, 'option2',
                  'https://shop.travisscott.com/products/', 'Travis Scott (US)')
    except Exception as e:
        print('Failed: ' + e)
    try:
        ScanStore('undefeated_list.dat', 'https://undefeated.com/collections/mens-footwear/', undefeated, 'option2',
                  'https://undefeated.com/collections/mens-footwear/products/', 'Undefeated Footwear (US)')
    except Exception as e:
        print('Failed: ' + e)
    try:
        ScanStore('unknwn_list.dat', 'https://www.unknwn.com/collections/footwear/', unknwn, 'option2',
                  'https://www.unknwn.com/collections/footwear/products/', 'UNKNWN Footwear (US)')
    except Exception as e:
        print('Failed: ' + e)
    try:
        ScanStore('westnyc_list.dat', 'https://www.westnyc.com/collections/footwear/', westnyc, 'option1',
                  'https://www.westnyc.com/collections/footwear/products/', 'West NYC (US)')
    except Exception as e:
        print('Failed: ' + e)
    try:
        ScanStore('nicekicks_list.dat', 'https://shopnicekicks.com/collections/mens-kicks/', nicekicks, 'option1',
                  'https://shopnicekicks.com/collections/mens-kicks/products/', 'Nice Kicks (US)')
    except Exception as e:
        print('Failed: ' + e)
    try:
        ScanStore('unionlosangeles_list.dat', 'https://store.unionlosangeles.com/collections/footwear/', unionlosangeles, 'option1',
                  'https://store.unionlosangeles.com/products/', 'Union (US)')
    except Exception as e:
        print('Failed: ' + e)
