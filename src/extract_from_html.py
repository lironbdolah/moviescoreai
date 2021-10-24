from datetime import datetime
import os
from bs4 import BeautifulSoup
from urllib import request
now = datetime.now()
years = range(1990,int(now.year))

def extract_movies_url(url):
    global image
    reviews_url_list = []
    names_list = []
    images_list = []
    try:
        html = request.urlopen(url).read()
        soup = BeautifulSoup(html, features='lxml')
        links = soup.find_all('a')
        for tag in links[50:]:
            link = tag.get('href', None)
            if link is not None:
                if '/title/tt' in link:  # finds each movie url
                    movie_url = 'https://www.imdb.com' + link
                    try:
                        html2 = request.urlopen(movie_url).read()
                    except:
                        break
                    soup2 = BeautifulSoup(html2, features='lxml')
                    reviews_url = soup2.find_all('a')
                    imgtag = soup2.find_all('img')
                    for tag in imgtag:
                        image = tag.get('src', None)
                        break
                    for tag in reviews_url:
                        link = tag.get('href', None)

                        if link is not None:
                            if '/reviews?ref_=tt_urv' in link :  # finds movie review url
                                if (movie_url + 'reviews?ref_=tt_urv') not in reviews_url_list:
                                    reviews_url_list.append(movie_url + 'reviews?ref_=tt_urv')
                                    name = soup2.title.string
                                    names_list.append(name[:-14])
                                    images_list.append(image)
                                    print(movie_url + 'reviews?ref_=tt_urv' + " " + name[:-14])


    except:
        print('404 not found')



    return (reviews_url_list ,names_list,images_list)

def extract_reviews(reviews_url_list,movies_names):
  reviews_list = []
  reviews_scores = []
  movie = []
  scores = ['0/10', '1/10', '2/10', '3/10', '4/10', '5/10', '6/10', '7/10', '8/10', '9/10']
  for review_url in reviews_url_list:
    html = request.urlopen(review_url).read().decode('utf8')
    raw = BeautifulSoup(html, 'html.parser').get_text()
    raw = raw[int(raw.find("10 Stars"))+len("10 Stars"):]
    raw = os.linesep.join([s for s in raw.splitlines() if s])
    reviews = raw.split("Permalink")
    reviews = reviews[:-1]

    for i in reviews:
        review = ''.join(i)
        for score in scores:
            if score in review:
                review = review[int(review.find(str(now.year)))+4: int(review.find('found this helpful')) - len('found this helpful')]
                review = os.linesep.join([s for s in review.splitlines() if s])
                if len(review) > 2:
                    reviews_list.append(review)
                    if score == '0/10':
                        reviews_scores.append(10)
                    else:
                        reviews_scores.append(int(score[0]))
                    movie.append(movies_names[reviews_url_list.index(review_url)])

  return (reviews_list,movie,reviews_scores)

def add_images(df,images,movies_names):
     i = 0
     images_list = []
     for index,row in df.iterrows():
            if row['movies'] == movies_names[i]:
                images_list.append(images[i])
            else:
                i+=1
                images_list.append(images[i])
     df['image_url'] = images_list
     return df





