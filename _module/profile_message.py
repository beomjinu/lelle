import pymongo, datetime, json

class uld:
    def __init__(self):
        with open("data.json", "r") as file: json_data = json.load(file)
        mongodb_url = json_data["mongo_db"]["url"]
        client = pymongo.MongoClient(mongodb_url)
        db = client["discord_bot"]

        self.collection = db["profile_message"]

    def upload(self, user_id: str, message: str):
        self.collection.update_one(
            {
                "user_id": user_id
            },
            {
                "$set": {
                    "message": message,
                    "upload_time": str(datetime.date.today()) 
                }
            },
            upsert=True
        )

    def load(self, user_id):
        try:
            return self.collection.find_one({"user_id":user_id})["message"]
        except:
            return None
        
    def delete(self, user_id):
        self.collection.delete_one({"user_id":user_id})

if __name__ == "__main__":
    pm = uld()
    print(pm.load("beomjinu"))