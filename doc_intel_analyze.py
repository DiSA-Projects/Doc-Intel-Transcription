import os

# =========================================================================================================
# DOCUMENT INTELLIGENCE SECTION (Based on the code snippet provided by MS Azure)
# =========================================================================================================

# These key credentials are from your paid account and should not be shared publicly.
# Remember to remove the key from your code when you're done, and never post it publicly. For production, use secure methods to store and access your credentials.

# Replace "YOUR_FORM_RECOGNIZER_ENDPOINT" and "YOUR_FORM_RECOGNIZER_KEY" with your credentials (endpoint and api key from Document Intelligence)
ENDPOINT = "YOUR_FORM_RECOGNIZER_ENDPOINT" 
API_KEY = "YOUR_FORM_RECOGNIZER_KEY"

# For more information, see https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-security?tabs=command-line%2Ccsharp#environment-variables-and-application-configuration

# Get words
def get_words(page, line):
    result = []
    for word in page.words:
        if _in_span(word, line.spans):
            result.append(word)
    return result

# To learn the detailed concept of "span" in the following codes, visit: https://aka.ms/spans
def _in_span(word, spans):
    for span in spans:
        if word.span.offset >= span.offset and (word.span.offset + word.span.length) <= (span.offset + span.length):
            return True
    return False

# USED TO INTERACT WITH FILES

# Save text (txt) to a new file (filename)
def save_to_file(filename,txt):
    wfile = open(filename,"w")
    wfile.write(txt)
    wfile.close()

# Modified version of Analyze_Read function provided as a template by Microsoft Azure Document Intelligence
# * Instead of printing output to the terminal, the analytical notes are saved in a separate text file in notes.

def analyze_read(sourcepath,fname):
    filetext = ''
    filenotes = ''
    filename = sourcepath+fname

    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.ai.documentintelligence.models import DocumentAnalysisFeature, AnalyzeResult, AnalyzeDocumentRequest

    # If you're using ENDPOINT and API_KEY defined earlier in the environment (more secure), you can access them here.
    #endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
    #key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]

    # For most users, it may be easier to define the endpoint and key globally (see above)
    
    document_intelligence_client = DocumentIntelligenceClient(endpoint=ENDPOINT, credential=AzureKeyCredential(API_KEY))

    # Analyze a document at a URL:
    # formUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/read.png"
    # Replace with your actual formUrl:
    # If you use the URL of a public website, to find more URLs, please visit: https://aka.ms/more-URLs
    # If you analyze a document in Blob Storage, you need to generate Public SAS URL, please visit: https://aka.ms/create-sas-tokens
    # poller = document_intelligence_client.begin_analyze_document(
    #    "prebuilt-read",
    #    AnalyzeDocumentRequest(url_source=formUrl),
    #    features=[DocumentAnalysisFeature.LANGUAGES]
    # )

    # # If analyzing a local document, remove the comment markers (#) at the beginning of these 11 lines.
    # Delete or comment out the part of "Analyze a document at a URL" above.
    # Replace <path to your sample file>  with your actual file path.
    path_to_sample_document = filename
    print(f'Filename {filename}')
    with open(path_to_sample_document, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-read",
            analyze_request=f,
            features=[DocumentAnalysisFeature.LANGUAGES],
            content_type="application/octet-stream",
        )
    result: AnalyzeResult = poller.result()

    # [START analyze_read]
    # Detect languages.
    print("----Languages detected in the document----")
    if result.languages is not None:
        for language in result.languages:
            filenotes = filenotes + '/n'+'Language code: '+language.locale+' with confidence '+str(language.confidence)
            #print(f"Language code: '{language.locale}' with confidence {language.confidence}")

    # To learn the detailed concept of "bounding polygon" in the following content, visit: https://aka.ms/bounding-region
    # Analyze pages.
    for page in result.pages:
        #print(f"----Analyzing document from page #{page.page_number}----")
        filenotes = filenotes+'/n'+'----Analyzing document from page #'+str(page.page_number)+'----'
        filenotes = filenotes+'/n'+'Page has width: '+str(page.width)+' and height: '+str(page.height)+', measured with unit: '+page.unit
        #print(f"Page has width: {page.width} and height: {page.height}, measured with unit: {page.unit}")

        # Analyze lines.
        if page.lines:
            for line_idx, line in enumerate(page.lines):
                words = get_words(page, line)
                #print(
                #    f"...Line # {line_idx} has {len(words)} words and text '{line.content}' within bounding polygon '{line.polygon}'"
                #)
                filenotes = filenotes+'\n'+'...Line # '+str(line_idx)+' has '+str(len(words))+ ' words and text '+line.content+' within bounding polygon '+str(line.polygon)

                # Analyze words.
                for word in words:
                    #print(f"......Word '{word.content}' has a confidence of {word.confidence}")
                    filenotes = filenotes+'\n'+'......Word '+ word.content+' has a confidence of '+str(word.confidence)

    # Analyze paragraphs.
    if result.paragraphs:
        print(f"----Detected #{len(result.paragraphs)} paragraphs in the document: {fname}----")
        for paragraph in result.paragraphs:
            #print(f"Found paragraph within {paragraph.bounding_regions} bounding region")
            #print(f"...with content: '{paragraph.content}'")
            filetext = filetext + '\n'+paragraph.content

    newfile = fname.split('.')
    newfileloc = './notes/'+newfile[0]+'_notes.txt'
    save_to_file(newfileloc,filenotes)
    print("----------------------------------------")
    filetext = filetext + '\n----------------------------------------'
    return filetext
# [END analyze_read]

# =========================================================================================================