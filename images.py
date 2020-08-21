import requests
from bs4 import BeautifulSoup
import bs4
import shutil
import cv2
from flask_restful import Resource
import os

class Image_Extractor(Resource):
    @classmethod
    def get(cls, article_URL):
        FOLDER_NAME = 'blog_details' #@param {type:"string"}
        try:
            os.mkdir(FOLDER_NAME)
        except:
            print("file already exist")

        os.chdir(FOLDER_NAME)
        #@title Enter Medium Story URL
        article_URL = article_URL #@param {type:"string"}
        # article_URL = 'https://www.tmz.com/2020/07/29/dr-dre-answers-wife-divorce-petition-prenup/'
        response = requests.get(article_URL)
        soup = bs4.BeautifulSoup(response.text,'html.parser')
        images = soup.find('body').find_all('img')
        # --- loop --- 

        data = []
        i = 0

        for img in images:
        #     print('HTML:', img)

            url = img.get('src')

            if url:  # skip `url` with `None`
        #         print('Downloading:', url) 
                try:
                    response = requests.get(url, stream=True)

                    i += 1
                    url = url.rsplit('?', 1)[0]  # remove ?opt=20 after filename
                    ext = url.rsplit('.', 1)[-1] # .png, .jpg, .jpeg
                    filename = f'{i}.{ext}' 
        #             print('Filename:', filename)

                    with open(filename, 'wb') as out_file:
                        shutil.copyfileobj(response.raw, out_file)

                    image = cv2.imread(filename)
                    height, width = image.shape[:2]

                    data.append({
                        'url': url,
                        'path': filename,
                        'width': width,
                        'height': height,
                    })

                except Exception as ex:
                    pass
        #             print('Could not download: ')
        #             print('Exception:', ex)

        #     print('---')

        # --- after loop ---
        # print('max:', max(data, key=lambda x:x['width']))
        max_img = sorted(data, key=lambda x:x['width'], reverse=True)[:3]
        # top_images = { i : max_img[i] for i in range(0, len(max_img) ) }
        return max_img

