# USING DOC INTELLIGENCE AS TRANSCRIPTION TOOL

# A template for using Document Intelligence to transcribe Non-OCR PDFs 
# and perform post-transcription text-cleaning

# Developed by Neil Aitken, Digital Projects Specialist, DiSA
# Last update: 2025-03-31

import os
from doc_intel_analyze import *

# GLOBALS

SOURCE_DIR = './'
DATA_DIR = './data/'
CLEANED_DIR = './cleaned/'


# ==============================
# A. FILE PROCESSING
# ==============================
ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))

# Create system appropriate path string
def resource_path(relative_path):
    import sys
    if hasattr(sys,'_MEIPASS'):
        return os.path.join(sys._MEIPASS,os.path.join(ASSETS_DIR,relative_path))
    return os.path.join(ASSETS_DIR, relative_path)

# Change outputdir if you want to point to a different subfolder
sourcepath = SOURCE_DIR
outputdir = DATA_DIR

# Save text (txt) to a new file (filename)
def save_to_file(filename,txt):
    wfile = open(filename,"w")
    wfile.write(txt)
    wfile.close()

# Read/transcribe a pdf and save it to the data directory
def read_pdf_into_ocr(fname,sourcedir,outputdir):
    if fname.endswith('.pdf'):
            
        try:
            filename = sourcedir+fname
            result_text = analyze_read(sourcedir,fname)
            newfile = fname.split('.')
            newfileloc = outputdir+newfile[0]

            save_to_file(newfileloc+'_ocr.txt',result_text)

        except:
            print('Error while reading pdf')
    

# ==============================
# B. TEXT CLEANING
# ==============================

import re
import string

# In this section, you can add whatever text cleaning steps you need to take

# Remove paragraph markers introduced by Document Intelligence transcription
def remove_paragraph_markers(text):
    #Remove "Paragraph:" and "=======" using regular expressions
    text = re.sub(r'(Paragraph:)','',text)
    text = re.sub(r'===PARAGRAPH===','',text)
    text = re.sub(r'={10}','',text)
    text = re.sub(r'\n{2}','',text)
    return text

# Use if documents have hole punch marks that are being misinterpreted as 
def remove_hole_punch_marks(text):
    newtext = ''
    lines = text.split('\n')
    for line in lines:
        if len(line) == 1 and line[0] in ['O','0',':']:
            newtext = newtext+'\n'
        else:
            newtext = newtext+'\n'+line

    return newtext

# Use to run any cleaning steps required
def clean_text(text):
    # Add any other text cleaning steps as separate functions to simplify testing and debugging
    text = remove_paragraph_markers(text)
    text = remove_hole_punch_marks(text)
    return text

# ==============================
# C. FILE PROCESSING
# ==============================

# Process all the files in the source folder and output text files to data folder
def process_pdfs():
    files = [f for f in os.listdir(sourcepath) if os.path.isfile(os.path.join(sourcepath, f))]
    for f in files:
        read_pdf_into_ocr(f,sourcepath,outputdir)

# Process all data files (raw transcribed text) and perform text cleaning. Outputs cleaned text to outputdir
def clean_datafile(filename,datadir,outputdir):
    import os
    try:
        with open(datadir+filename,'r') as text:
            lines = text.read()
            cleaned = clean_text(lines)
            fname = filename.split('.')
            newfile = fname[0]+'_clean.txt'
            wfile = open('.'+outputdir+newfile,"w")
            wfile.write(cleaned)
            wfile.close()
            #print(cleaned)
            print(filename+' processed. Creating '+newfile)
    except:
        print('Configuration file read error')
        raise

def process_datafiles():
    datadir = DATA_DIR
    outputdir = CLEANED_DIR
    datafiles = [f for f in os.listdir(datadir) if os.path.isfile(os.path.join(datadir, f))]
    for f in datafiles:
        clean_datafile(f,datadir,outputdir)

# ==============================
# D. MAIN PROGRAM
# ==============================

process_pdfs()
process_datafiles()