import pymongo, json, datetime

class uld:
    def __init__(self):
        with open("data.json", "r") as file:json_data = json.load(file)
        mongodb_url = json_data["mongo_db"]["url"]
        client = pymongo.MongoClient(mongodb_url)
        db = client["discord_bot"]

        self.collection = db["d_day"]

    def upload(self, user_id: str, date: str): # date format is "2022-01-01"
        self.collection.update_one(
            {
                "user_id": user_id
            },
            {
                "$set": {
                    "date": date,
                    "upload_time": str(datetime.date.today()) 
                }
            },
            upsert=True
        )
    
    def load(self, user_id):
        return self.collection.find_one({"user_id":user_id})
        
    def delete(self, user_id):
        self.collection.delete_one({"user_id":user_id})

def d_day(date: str):
    today = datetime.date.today()
    target_day = [int(d) for d in date.split("-")]
    target_day = datetime.date(target_day[0], target_day[1], target_day[2])

    return (today - target_day).days + 1
    
if __name__ == "__main__":
    print(d_day("2022-01-01"))