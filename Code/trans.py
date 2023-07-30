from googletrans import Translator
from PIL import Image
import pytesseract
import sys
import string
import textract

def lang_trans(get_sentence,to_lang):
    translator = Translator()
    try:
        text_to_translate = translator.translate(get_sentence,dest= to_lang)
        text = text_to_translate.text
        return text
    except Exception as e:
        return e

def pdf_trans(pdf_org,to_lang):
    text = textract.process(pdf_org,method='pdftotext')
    print(text)
    decoded = text.decode("utf-8")
    print(decoded)
    ret = lang_trans(decoded,to_lang)
    return ret

def ocr_core(filename,targetlang):
# Edit this path to tesseract.exe on your system. On windows its by default in the following:
    # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    # Opens image
    im = Image.open(filename)
    # Gets the image and translates it to Czech. You can specify own lang if you want.
    text = pytesseract.image_to_string(im)
    text_translated = lang_trans(text,targetlang)
    return text_translated
