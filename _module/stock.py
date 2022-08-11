from urllib import parse
from bs4 import BeautifulSoup
import requests, json, pymongo, datetime

def get_search_url(name: str):
    base_url = "https://finance.naver.com"
    convert_name = parse.quote(name.encode("euc-kr"))
    
    return base_url + "/search/searchList.naver?query=" + convert_name

def get_stock_list(name: str):
    url = get_search_url(name=name)
    
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    selector = "#content > div.section_search > table > tbody > tr:nth-child"

    count, a_tag = 0, 0
    a_tag_list = []
    while a_tag != "None":
        count += 1
        a_tag = str(soup.select_one(selector + f"({count}) > td > a"))
        a_tag_list.append(a_tag)
    
    stock_list = [[a_tag[39:-4], a_tag[31:37]] for a_tag in a_tag_list[:-1]]

    return stock_list

class stock:
    def __init__(self, code: str):
        url = "https://finance.naver.com/item/main.naver?code=" + code
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        self.code = code
        self.soup = soup
        
    def get_name(self):
        selector = "#middle > div.h_company > div.wrap_company > h2 > a"
        name = self.soup.select_one(selector).text

        return name

    def get_price(self, comma=True):
        selector = "#chart_area > div.rate_info > div > p > em > span"
        price = self.soup.select_one(selector).text

        return price if comma else int(price.replace(",", ""))

class favorites:
    def __init__(self, user_id):
        with open("data.json", "r") as file: json_data = json.load(file)
        mongodb_url = json_data["mongo_db"]["url"]
        client = pymongo.MongoClient(mongodb_url)
        db = client["discord_bot"]

        self.collection = db["stock_favorites"]
        self.user_id = user_id

    def upload(self, code: str):
        self.collection.update_one(
            {"user_id": self.user_id},
            {"$set": {
                    "code": code,
                    "upload_time": str(datetime.date.today()) 
                }
            },
            upsert=True
        )
    
    def load(self):
        try:
            return self.collection.find_one({"user_id":self.user_id})["code"]
        except:
            return None
        
    def delete(self):
        self.collection.delete_one({"user_id":self.user_id})

if __name__ == "__main__":
    samsung = stock("005930")
    print(get_stock_list("카카오"))