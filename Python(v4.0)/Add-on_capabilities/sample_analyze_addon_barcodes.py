# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_analyze_addon_barcodes.py

DESCRIPTION:
    This sample demonstrates how to extract all identified barcodes using the
    add-on 'BARCODES' capability.

    This sample uses Layout model to demonstrate.

    Add-on capabilities accept a list of strings containing values from the `DocumentAnalysisFeature`
    enum class. For more information, see:
    https://aka.ms/azsdk/python/documentintelligence/analysisfeature.

    The following capabilities are free:
    - BARCODES
    - LANGUAGES

    The following capabilities will incur additional charges:
    - FORMULAS
    - OCR_HIGH_RESOLUTION
    - STYLE_FONT
    - QUERY_FIELDS

    See pricing: https://azure.microsoft.com/pricing/details/ai-document-intelligence/.

PREREQUISITES:
    The following prerequisites are necessary to run the code. For more details, please visit the "How-to guides" link: https://aka.ms/how-to-guide

    -------Python and IDE------
    1) Install Python 3.7 or later (https://www.python.org/), which should include pip (https://pip.pypa.io/en/stable/).
    2) Install the latest version of Visual Studio Code (https://code.visualstudio.com/) or your preferred IDE. 
    
    ------Azure AI services or Document Intelligence resource------ 
    Create a single-service (https://aka.ms/single-service) or multi-service (https://aka.ms/multi-service) resource.
    You can use the free pricing tier (F0) to try the service and upgrade to a paid tier for production later.
    
    ------Get the key and endpoint------
    1) After your resource is deployed, select "Go to resource". 
    2) In the left navigation menu, select "Keys and Endpoint". 
    3) Copy one of the keys and the Endpoint for use in this sample. 
    
    ------Set your environment variables------
    At a command prompt, run the following commands, replacing <yourKey> and <yourEndpoint> with the values from your resource in the Azure portal.
    1) For Windows:
       setx DOCUMENTINTELLIGENCE_API_KEY <yourKey>
       setx DOCUMENTINTELLIGENCE_ENDPOINT <yourEndpoint>
       • You need to restart any running programs that read the environment variable.
    2) For macOS:
       export key=<yourKey>
       export endpoint=<yourEndpoint>
       • This is a temporary environment variable setting method that only lasts until you close the terminal session. 
       • To set an environment variable permanently, visit: https://aka.ms/set-environment-variables-for-macOS
    3) For Linux:
       export DOCUMENTINTELLIGENCE_API_KEY=<yourKey>
       export DOCUMENTINTELLIGENCE_ENDPOINT=<yourEndpoint>
       • This is a temporary environment variable setting method that only lasts until you close the terminal session. 
       • To set an environment variable permanently, visit: https://aka.ms/set-environment-variables-for-Linux
       
    ------Set up your programming environment------
    At a command prompt,run the following code to install the Azure AI Document Intelligence client library for Python with pip:
    pip install azure-ai-documentintelligence --pre
    
    ------Create your Python application------
    1) Create a new Python file called "sample_analyze_addon_barcodes.py" in an editor or IDE.
    2) Open the "sample_analyze_addon_barcodes.py" file and insert the provided code sample into your application.
    3) At a command prompt, use the following code to run the Python code: 
       python sample_analyze_addon_barcodes.py
"""

import os


def analyze_barcodes():
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.ai.documentintelligence.models import DocumentAnalysisFeature, AnalyzeResult, AnalyzeDocumentRequest

    # For how to obtain the endpoint and key, please see PREREQUISITES above.
    endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
    key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]

    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # Analyze a document at a URL:
    formUrl = "https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/documentintelligence/azure-ai-documentintelligence/samples/sample_forms/add_ons/barcodes.jpg?raw=true"
    # Replace with your actual formUrl:
    # If you use the URL of a public website, to find more URLs, please visit: https://aka.ms/more-URLs 
    # If you analyze a document in Blob Storage, you need to generate Public SAS URL, please visit: https://aka.ms/create-sas-tokens
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-read",
        AnalyzeDocumentRequest(url_source=formUrl),
        features=[DocumentAnalysisFeature.BARCODES]    # Specify which add-on capabilities to enable.
    )       

    # # If analyzing a local document, remove the comment markers (#) at the beginning of these 11 lines.
    # # Delete or comment out the part of "Analyze a document at a URL" above.
    # # Replace <path to your sample file>  with your actual file path.
    # path_to_sample_document = "<path to your sample file>"
    # with open(path_to_sample_document, "rb") as f:
    #     poller = document_intelligence_client.begin_analyze_document(
    #         "prebuilt-layout",
    #         analyze_request=f,
    #         features=[DocumentAnalysisFeature.BARCODES],        # Specify which add-on capabilities to enable.
    #         content_type="application/octet-stream",
    #     )
    result: AnalyzeResult = poller.result()

    # [START analyze_barcodes]
    # Iterate over extracted barcodes on each page.
    # To learn the detailed concept of "bounding polygon" in the following content, visit: https://aka.ms/bounding-region
    for page in result.pages:
        print(f"----Barcodes detected from page #{page.page_number}----")
        if page.barcodes:
            print(f"Detected {len(page.barcodes)} barcodes:")
            for barcode_idx, barcode in enumerate(page.barcodes):
                print(f"- Barcode #{barcode_idx}: {barcode.value}")
                print(f"  Kind: {barcode.kind}")
                print(f"  Confidence: {barcode.confidence}")
                print(f"  Bounding regions: {barcode.polygon}")

    print("----------------------------------------")
    # [END analyze_barcodes]


if __name__ == "__main__":
    from azure.core.exceptions import HttpResponseError
    from dotenv import find_dotenv, load_dotenv

    try:
        load_dotenv(find_dotenv())
        analyze_barcodes()
    except HttpResponseError as error:
        # Examples of how to check an HttpResponseError
        # Check by error code:
        if error.error is not None:
            if error.error.code == "InvalidImage":
                print(f"Received an invalid image error: {error.error}")
            if error.error.code == "InvalidRequest":
                print(f"Received an invalid request error: {error.error}")
            # Raise the error again after printing it
            raise
        # If the inner error is None and then it is possible to check the message to get more information:
        if "Invalid request".casefold() in error.message.casefold():
            print(f"Uh-oh! Seems there was an invalid request: {error}")
        # Raise the error again
        raise

# Next steps:
# Learn more about Add-on capabilities (Barcode property extraction): https://aka.ms/barcode-property-extraction
# Find more sample code: https://aka.ms/doc-intelligence-samples
