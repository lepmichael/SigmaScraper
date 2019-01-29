
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)

# @app.route("/")
# def home():
#     return "Hello, World!"

@app.route('/lookup')
def my_route():
    # page = request.args.get('page', default = 1, type = int)
    query = request.args.get('q', default = '*', type = str)

    properties = get_info(query)

    return jsonify(properties)

def get_info(term):
    # term = input('Chemical? ')

    url = 'https://www.sigmaaldrich.com/catalog/search'

    params = {
        'term':term,
        'interface':'All',
        'N':0,
        'mode':'match%20partialmax',
        'lang':'en',
        'region':'US',
        'focus':'product'
    }

    r = requests.get(url = url, params = params)

    soup = BeautifulSoup(r.content)

    pnvList = soup.find_all("li", class_="productNumberValue")

    firstProductURL = None
    for pnv in pnvList:
        if pnv.find('a') is not None:
            # print(pnv.find('a')['href'])

            firstProductURL = pnv.find('a')['href']
            break


    url = 'https://www.sigmaaldrich.com/' + firstProductURL

    r = requests.get(url)

    soup = BeautifulSoup(r.content)

    rgt = soup.find_all("td", class_="rgt")
    lft = soup.find_all("td", class_="lft")

    output = {}

    # So number of tags with rgt and lft should be the same
    for tag1, tag2 in zip(lft, rgt):
        # print(type(tag1.text))
        # print(tag2.text)
        label = tag1.text.replace('\n', '').replace('\t', '').replace('\xa0', ' ').strip()
        value = tag2.text.replace('\n', '').replace('\t', '').replace('\xa0', ' ').strip()
        # print(value)

        output[label] = value

    return output

if __name__ == "__main__":
    app.run(debug=True)
