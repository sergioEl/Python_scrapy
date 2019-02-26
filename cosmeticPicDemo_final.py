## download pictures of products and information from ttps://cosmetic-love.com
## only images
## made by Sergio Han
## no commercial use
## if you have any question, email me shhan421@daum.net

import requests, os, bs4
import csv

pageNum = 1
noProdcuts = False

# make a folder
os.makedirs('Cosmetic_love', exist_ok=True)

# make a text file
file = open(os.path.join('Cosmetic_love', 'cosmetic_love_list.txt'), 'w')

while not noProdcuts:   
    url = "https://cosmetic-love.com/collections/the-face-shop?page="+ str(pageNum) +"&view=all"

    print("**********\nDownloading page %s\n**********" %url)

    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html5lib")

    # if there is no more prodcut, break the while loop
    if soup.find('p', attrs={'style':'text-align: center;'}):
        sorryMsg = soup.find('p', attrs={'style':'text-align: center;'}).get_text()
        print(sorryMsg)

        if sorryMsg == "Sorry, there are no products in this collection":
            noProducts = True
            print("no more page needed BYE")
            break


    # searching for the name and prices
    productNames = soup.find_all('a', 'product-title')
    priceBoxes = soup.find_all('div', 'price-box')

    # searching for the image files
    productImages = soup.find_all('a', "product-grid-image")
    
    ### start scraping product images 
    if productImages == []:
        print('Could not find product image')
    
    else:

        for links in productImages:
            links = links.img
            # get alt and save file names with it
            imgAlt = links.get('alt')
            imgAlt = imgAlt.replace(' - Cosmetic Love', '')
            imgAlt = imgAlt + '.png'

            
            imageUrl = links.get('src')
            imageUrl = 'https:' + imageUrl
            questionMark = imageUrl.find("?")
            imageUrl = imageUrl[:questionMark]
            
#            print(imageUrl)
#            print("downloading image %s..." % (imageUrl))
            res = requests.get(imageUrl)
            res.raise_for_status()

            # saving image files to the folder
##            imgName = os.path.basename(imageUrl)
##            imgName = imgName.replace('-', ' ')
##            imgName = imgName.replace('jpg', 'png')
            imageFile = open(os.path.join('Cosmetic_love', imgAlt), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
    ### complete scraping images 

    print(len(productNames))
    print('products saved**************\n')

 
 
    # print the results
    print('NAME'+"\t"+'Old price'+"\t"+'Discounted price')
    for i in range(len(priceBoxes)):
        productName = productNames[i].get_text().strip()
        #oldPrice = oldPrices[i].get_text().strip()
        if priceBoxes[i].find('p', 'regular-product'):
            nomalPrice = priceBoxes[i].p.span.span.get_text().strip()
            print(productName+' '+nomalPrice)
            file.write(productName + " " + nomalPrice)
            file.write('\n')
        else:
            oldPrice = priceBoxes[i].find('span', 'old-price').span.get_text().strip()
            discountedPrice = priceBoxes[i].find('span', 'special-price').span.get_text().strip()
            print(productName+"  "\
                  +oldPrice+'  ' \
                  +discountedPrice)
            file.write(productName + " " + oldPrice + ' ' + discountedPrice)
            file.write('\n')

    # increment    
    pageNum += 1

# close the file
file.close()

print('Done. Now, you can check "Cosmetic_love" folder and see pictures and a text file.')
