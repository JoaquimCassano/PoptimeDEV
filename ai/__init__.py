import ocrspace, openai
from typing import Literal
from gradio_client import Client
import json ; secrets = json.load(open('secrets.json'))
api = ocrspace.API(api_key=secrets['ocrspace'])

openai.api_base = "https://api.naga.ac/v1"

def Describe(url:str) -> tuple[str, str, str]:
    """
    Generates a description of an image and performs OCR on the given URL.

    Args:
        url (str): The URL of the image to be described.

    Returns:
        tuple[str, str, str]: A tuple containing the generated caption for the image, the extracted text from OCR, and the URL of the image.
    """
    DESCRIBING_MODEL = "https://soumnerd-salesforce-blip-image-captioning-large.hf.space/"

    def describeIMG():

        client = Client(DESCRIBING_MODEL, verbose=False)
        result = client.predict(
                        url,	# str (filepath or URL to image) in '请选择一张图片' Image component
                        fn_index=0
        )
        return result
    caption = describeIMG()
    text = api.ocr_url(url)
    return (caption, text, url)

def AiResponse(messages:list, model:Literal["gpt-3.5-turbo-0613", "gpt-4", "SOLAR-0-70b-16bit", "gpt-3.5-turbo-16k"]) -> str: # type: ignore
    if model != "SOLAR-0-70b-16bit":
        openai.api_key = secrets["naga"]
        resp = openai.ChatCompletion.create(
            model=model,
            messages=messages,
        )
        return resp['choices'][0]['message']['content'] # type: ignore

    


if __name__ == "__main__":
    print(Describe('https://pbs.twimg.com/media/F64BSE7W8AABYON.jpg'))