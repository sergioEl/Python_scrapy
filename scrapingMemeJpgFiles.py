#download memes from ttps://www.memecenter.com/page
#only images not gif or mp4
import requests, os, bs4

url = 'https://www.memecenter.com/page/24838'
# start with this page
urlNumber = 24838
# make a folder
os.makedirs('MEME', exist_ok=True)
while not url.endswith('24835'):# set the page number that you want to reach
    print("**********\nDownloading page %s...\n**********" %url)
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html5lib")
    # searching for the image files
    comicElem = soup.find_all("img", class_="rrcont")


    if comicElem == []:
        print('Could not find comic image')
    else:

        for links in comicElem:
            comicUrl = links.get('src')
            print(comicUrl)
            print("downloading image %s..." % (comicUrl))

            res = requests.get(comicUrl)
            res.raise_for_status()

            # saving image files to MEME folder
            imageFile = open(os.path.join('MEME', os.path.basename(comicUrl)), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()

    # decrement of page number
    urlNumber -= 1
    #set a new page
    url = 'https://www.memecenter.com/page/' + str(urlNumber)
    
#end
print('Done')
