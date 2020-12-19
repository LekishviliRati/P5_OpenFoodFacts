import json
import requests

"Get data from API"

request = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0"
                       "=contains&sort_by=unique_scans_n&page_size=100&json=true&fields=product_name_fr,"
                       "generic_name_fr,categories,nutrition_grade_fr,brands,stores,url")   # get data from API


request_text = request.text     # request data as text format
data = json.loads(request_text)     # data as json format (dictionary)

# json.dump(data, open('data.json', "w"), indent=4)   # save data temporary in data.json to visualise it

# products = data["products"]
# print(products)