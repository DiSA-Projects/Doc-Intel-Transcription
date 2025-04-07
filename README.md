# Doc-Intel-Transcription
Template for using Document Intelligence to extract text from non-OCR PDFs (aka AI-aided transcription). 

_Original code by Neil Aitken, UBC Digital Scholarship in the Arts_

## Summary
Sometimes we want to extract text from a PDF (or a group of PDFs) that contains scans of text that are currently in a non-machine readable form (eg. non-OCR PDF). 
Using Azure Document Intelligence (a Microsoft Azure cloud service), we can now extract this text, automating a transcription process that previously would 
have taken hundreds of hours to do manually.

## Features
The provided files include:
1. _doc_intel_analyze_py_: a simplified version of the example code Microsoft offers for calling Document Intelligence; and,
2. _di_transcription_template.py_: a sample main file that includes both the transcription call and a framework with some example functions for post-extraction text-cleaning. 

## Instructions
1. [Set up Document Intelligence](SetupDocIntel.md) on Microsoft Azure
2. Download _doc_intel_analyze.py_ and _di_transcription_template.py_
3. In _doc_intel_analyze.py_, update ENDPOINT and API_KEY to use the Endpoint and Key values located in your Document Intelligence resource on Microsoft Azure (refer to [step 1](SetupDocIntel.md))
4. Place any PDFs you wish to transcribe into the main folder (or another folder, but you will need to change 'SOURCE_DIR' below) where you've installed this project on your machine.
5. Create folders for the transcribed text files and the cleaned text files (data and cleaned respectively). If you use other directory names (or if you have the original PDFs stored elsewhere), update the SOURCE_DIR, DATA_DIR, and CLEANED_DIR entries in _di_transcription_template.py_
```
md data
```
```
md cleaned
```   
6. Run the following from the command line (or compile and run _di_transcription_template.py_ -- or whatever you have renamed this file)
```
python di_transcription_template.py
```



