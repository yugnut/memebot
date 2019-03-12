import json
import configparser
import os
from watson_developer_cloud import VisualRecognitionV3

if (not os.path.isfile(os.path.join(os.path.dirname(__file__), "config.ini"))):
    print("No config file found, make sure you have one in the same directory as this python script\nexiting")
    quit()

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

TOKEN = config["DEFAULT"]["WATSON_KEY"]

visual_recognition = VisualRecognitionV3(
            "2018-03-19",
            iam_apikey=TOKEN)

def ReturnWatsonResults(urlInput):
    classes_result = visual_recognition.classify(url=urlInput).get_result()
    imageResults = dict()
    
    for images in classes_result["images"][0]["classifiers"][0]["classes"]:
        imageResults[images["class"]]="{0:.2f}".format(images["score"] * 100)

    return imageResults
