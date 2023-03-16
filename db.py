from pymongo import MongoClient
import ssl

connection_string=f"mongodb+srv://RishiPV:<password>@cluster0.9gqsnr8.mongodb.net/?retryWrites=true&w=majority"
client=MongoClient(connection_string,ssl.CERT_NONE)
dataSeesaws=client.CropDoctor
collection=dataSeesaws.Users