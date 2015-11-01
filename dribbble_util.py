from bs4 import BeautifulSoup as bs
import requests
import time
import json
import util
from sklearn.cluster import KMeans

API = "https://api.dribbble.com/v1/"
WEBSITE = 'https://dribbble.com'
TOKEN = "79d39c60c91a0f68fc98085efb6a12878e9d9b8d8d4d7176836c8fc2dca5b131"


class Dribbble:

    def __init__(self):
        pass

    def shot(self, id):
        url = API + "shots/{id}".format(id=id)
        params = {
            "access_token": TOKEN
        }
        r = requests.get(url, params=params)
        response = r.json()
        return response

    def shotPalette(self, url):
        palette = []
        r = requests.get(url)
        response = r.text
        soup = bs(response, 'html.parser')
        chips = soup.find_all('ul', {"class": "color-chips"})

        if len(chips) == 0:
            print str(chips) + "----->" + url
            return palette

        chips = chips[0]
        chips = chips.find_all('li')

        for chip in chips:
            palette.append(chip.find('a').contents[0])

        return palette

    def search(self, keyword, page=1, per_page=12, limit=10):

        api = WEBSITE + '/search'
        results = []

        while True:
            params = {
                "q": keyword,
                "page": page,
                "per_page": per_page,
                "_": int(time.time())
            }
            print params
            r = requests.get(api, params=params)
            response = r.text

            # No results? STOP
            if response.find("newShots") == -1:
                print "All pages fetched"
                return results

            soup = bs(response, 'html.parser')
            scripts = soup('script')

            shotJSON = scripts[2].contents[0]

            # Strip down to json string in <script>
            jsonValue = shotJSON.split('if (')[0].split("= ")[1].strip()[:-1]
            jsonValue = util.fixLazyJson(jsonValue)
            value = json.loads(jsonValue)

            # Results fetched, append to list
            results.extend(value)

            # Stop if no results fetched
            if len(results) >= limit or len(value) == 0:
                print "Limit reached"
                return results

            else:
                # Increment Page
                page += 1
                time.sleep(2)

        return results


def search(keyword, limit=50):
    d = Dribbble()
    results = d.search(keyword, page=1, limit=limit)
    print "{0} results found".format(len(results))
    return results


def extractPalette(results):
    d = Dribbble()
    colors = []
    for result in results:
        # shot = d.shot(result["id"])
        # if "html_url" in shot:
        if True:
            # palette = d.shotPalette(shot["html_url"])
            palette = d.shotPalette(WEBSITE + result["path"])
            time.sleep(1)
            # shot["palette"] = palette
            # result["shot"] = shot
            colors.extend(palette)
        else:
            print "----- No shot url -----"
            # print shot

    with open('data.txt', 'w') as outfile:
        json.dump(results, outfile)

    colors.sort(key=util.get_hsv)

    return results, colors  # results, palette


def cluster(colors):
    # Create cluster
    rgb_colors = [util.get_rgb(color) for color in colors]
    cluster = KMeans(n_clusters=7, random_state=10, tol=0.001)
    cluster.fit_predict(rgb_colors)
    centers = cluster.cluster_centers_
    labels = cluster.labels_.tolist()
    labels = [[x, labels.count(x)] for x in set(labels)]
    print labels

    # hex_centers = [{'color': '#%02x%02x%02x'} % tuple(i) for i in centers]
    hex_centers = []
    for index, value in enumerate(centers):
        hex_centers.append({
            'color': '#%02x%02x%02x' % tuple(value),
            'count': labels[index][1]
            })
    print hex_centers
    return hex_centers
