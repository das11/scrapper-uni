from textblob import TextBlob
from langdetect import detect


def validate_language(text):
    validated = False
    validated = isAssamese(handleNoFeature(text))

    return (True if validated else False)

def handleNoFeature(text):
    try:
        res_buffer = detect(text)
    except:
        res_buffer = "other"
    return res_buffer

def isAssamese(param):
    if param == "bn":
        return True
    else:
        return False

def processText(text):
    
    text_stg_1 = " ".join(substr for substr in text.split(" ") if validate_language(substr))
    text_stg_2 = processText_stg_2(text_stg_1)

    print("\n🟢 Procesed Data : " + text_stg_2)

    return text_stg_2

def processText_stg_2(text):
    # print(text)
    return text
    # if "র" in text:
    #     return False
    # else:
    #     return text