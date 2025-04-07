# Getting Started with Document Intelligence

## Set Up Your Azure Account
1. Create a new account on the Azure AI Portal: https://azure.microsoft.com/en-us/get-started/azure-portal
2. Set up a subscription (can be a free trial, student, or pay-as-you-go).

## Set Up Document Intelligence Resource
1. Create a Document Intelligence resource (located under Azure AI Services on the Azure Services Portal or in the AI+Machine Learning category on Create a Resource)
2. Creating a Resource pops up with a settings box
3. Select your subscription
4. Give your Resource Group a name
5. Set Region to West US2 (not all regions support Document Intelligence, but West US2 is the one recommended for us)
6. Give your Project Group a name
7. Set the Pricing Tier. In most cases, F0 should be fine. If you are processing a large number of pages, you will likely have to move up a tier.
8. Wait for Azure to finish deploying and creating the resource

## Get Your Endpoint and Key
1. Click on Go to Resource
2. Click on the Project Name to move to the project
3. Select “Click here to manage keys” to obtain the string values for the key and endpoint you’ll need to add to the doc_intel_analyze.py file. These are private keys and should not be shared publicly. Be sure to remove them whenever sharing code with others.
