import pandas as pd
from pymongo import MongoClient, InsertOne
from tqdm import tqdm
import os
from dotenv import load_dotenv

load_dotenv()

def check_collection_has_data(db, collection_name):
    collection = db[collection_name]
    return collection.count_documents({}) > 0

def main():
    client = MongoClient(os.getenv("MONGO_URL"))
    db = client["retail_analysis"]
    
   
    collections_with_data = [
        check_collection_has_data(db, "households"),
        check_collection_has_data(db, "transactions"),
        check_collection_has_data(db, "products")
    ]
    
    if all(collections_with_data):
        print("✅ Data uploaded succesfully in all collections")
        return
    
    
    print("Starting data upload for empty collections...")
    
   
    if not collections_with_data[0]:
        print("Uploading households data...")
        households = pd.read_csv("data/households.csv")
        db.households.insert_many(households.to_dict('records'))
        print("✅ Households data uploaded successfully")
    
   
    if not collections_with_data[1]:
        print("Uploading transactions data with bulk write...")
        transactions_chunks = pd.read_csv("data/transactions.csv", chunksize=1000)
        
        for chunk in tqdm(transactions_chunks, desc="Transactions Upload Progress"):
            ops = [InsertOne(record) for record in chunk.to_dict('records')]
            db.transactions.bulk_write(ops)
        print("✅ Transactions data uploaded successfully")
    
    
    if not collections_with_data[2]:
        print("Uploading products data...")
        products = pd.read_csv("data/products.csv")
        db.products.insert_many(products.to_dict('records'))
        print("✅ Products data uploaded successfully")
    
    print("✅ All data uploads completed successfully!")

if __name__ == "__main__":
    main()
