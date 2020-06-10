# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 09:35:39 2020

@author: Abul Hasanat Sekh
"""

# Import libraries 
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import glob
import re
import json

# Path of the pdf 
tesseract_loc=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
poppler_path=r'D:/Python_Workspace/poppler-0.68.0/bin'

#Recognizing text from the images using OCR 
def pdf2txt(PDF_file):
    pytesseract.pytesseract.tesseract_cmd = r"full path to the exe file"
    pytesseract.pytesseract.tesseract_cmd = tesseract_loc
    PDF_file=PDF_file
    pdfs = glob.glob(PDF_file)
    text=''
    for pdf_path in pdfs:
        pages = convert_from_path(pdf_path, 500,poppler_path=poppler_path)
    
        for pageNum,imgBlob in enumerate(pages):
            filename = pdf_path[:-4]+'_page'+str(pageNum)+'.jpg'
            # Save the image of the page in system 
            imgBlob.save(filename, 'JPEG')
            text = text+pytesseract.image_to_string(filename,lang='eng',config='--psm 6')
    return(text)


# =============================================================================
# This function will extract the information from the text generated from the pdf. 
# I'm using a corrosponding regex which is save with the same name of the pdf file. 
# In future we can create template mapping for the same structured pdf files.
# =============================================================================
    
def extract_info(PDF_file,text):
    try:
        with open (PDF_file.split('/')[-1:][0][:-4]+".txt", "r") as myfile:
            data=myfile.readlines()
    except FileNotFoundError:
        print("Wrong file or template missing")
        return
        
    values_dict={}
    
    if (re.findall('REFORAWING|REFDRAWING',text)):
        print('Document Type: Engineering Drawing')
        try:
            values_dict['Job Number']=re.findall(data[0][:-1], text)[0]
        except:
            values_dict['Job  Number']=re.findall(data[0][:-1], text)
        try:
            values_dict['Pipe Class']=re.findall(data[1][:-1], text)[0]
        except:
            values_dict['Pipe Class']=re.findall(data[1][:-1], text)
            
    elif ((re.findall('Invoice',text))):
        print('Document Type: Invoice')
        try:
            values_dict['Invoice Number']=re.findall(data[0][:-1], text)[0]
        except:
            values_dict['Invoice Number']=re.findall(data[0][:-1], text)
        try:
            values_dict['Invoice Date']=re.findall(data[1][:-1], text)[0]
        except:
            values_dict['Invoice Date']=re.findall(data[1][:-1], text)
        try:    
            values_dict['Invoice Amount']=re.findall(data[2], text)[0]
        except:
            values_dict['Invoice Amount']=re.findall(data[2], text)
    else:
        print('Unknown')

#Writing json file       
    print(values_dict)
    with open (PDF_file.split('/')[-1:][0][:-4]+".json", "w") as myfile:
        myfile.write(json.dumps(values_dict))
        
def main(args=None):
    try:
        #pdf2txt('BD1-1421.pdf')
        print(args[0])
        text=pdf2txt(args[0])
        extract_info(args[0],text)
    except:
        print('Usage: pdf_extract.py <pdf file name>')
    
    
if __name__ == "__main__":
    main(sys.argv[1:])
    