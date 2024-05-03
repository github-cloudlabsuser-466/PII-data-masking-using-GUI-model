import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

# Azure Cognitive Services configuration
endpoint = "https://az-ai-language.cognitiveservices.azure.com/"
key = "309a6f8d686046a5bd12be63fcf212b6"

# Create a TextAnalyticsClient
credential = AzureKeyCredential(key)
text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

# Function to detect PII entities
def detect_pii_entities(text):
    response = text_analytics_client.recognize_pii_entities([text])
    pii_entities = response[0].entities
    return pii_entities

# Function to mask PII entities
def mask_pii_entities(text, pii_entities):
    masked_text = text
    for entity in pii_entities:
        start_offset = entity.offset
        end_offset = entity.offset + entity.length
        masked_text = masked_text[:start_offset] + '*' * entity.length + masked_text[end_offset:]
    return masked_text

# Function to handle masking based on selected category
def mask_data():
    selected_category = category_combobox.get()
    document_content = document_text.get("1.0", tk.END)
    
    # Define PII fields for each category
    if selected_category == "Loan application":
        pii_fields = ["Email", "INUniqueIdentificationNumber"]
    elif selected_category == "Credit card application":
        pii_fields = ["Email"]
    elif selected_category == "Account statement":
        pii_fields = ["Email", "INUniqueIdentificationNumber"]
    elif selected_category == "KYC records":
        pii_fields = ["Email", "INUniqueIdentificationNumber"]
    else:
        # If category is "ALL" or unknown, treat it as "ALL"
        pii_fields = None
    
    # If PII fields are defined, filter entities based on category
    if pii_fields:
        # Detect PII entities
        pii_entities = detect_pii_entities(document_content)
        # Filter entities based on selected category's PII fields
        pii_entities = [entity for entity in pii_entities if entity.category in pii_fields]
    else:
        # If category is "ALL" or unknown, mask all PII entities
        pii_entities = detect_pii_entities(document_content)
    
    # Mask the document content based on selected PII entities
    masked_document_content = mask_pii_entities(document_content, pii_entities)
    masked_text.delete("1.0", tk.END)
    masked_text.insert("1.0", masked_document_content)

# Function to handle file upload
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf")])
    if file_path:
        with open(file_path, "r") as file:
            document_content = file.read()
        document_text.delete("1.0", tk.END)
        document_text.insert("1.0", document_content)

# Function to handle simple download
def download_file():
    masked_content = masked_text.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(masked_content)

# Function to upload data to Azure Blob Storage
def upload_to_azure_blob():
    # Implement Azure Blob Storage upload logic here
    pass

# GUI Setup
root = tk.Tk()
root.title("PII Data Masking Tool")

# Dropdown menu for selecting PII categories
categories = ["ALL", "Loan application", "Credit card application", "Account statement", "KYC records"]
category_label = tk.Label(root, text="Select PII Category:")
category_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
category_combobox = ttk.Combobox(root, values=categories)
category_combobox.grid(row=0, column=1, padx=10, pady=5)

# Button to upload file
upload_button = tk.Button(root, text="Upload File", command=upload_file)
upload_button.grid(row=0, column=2, padx=10, pady=5)

# Text widget for input document
document_label = tk.Label(root, text="Enter Document Text:")
document_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
document_text = tk.Text(root, width=50, height=10)
document_text.grid(row=1, column=1, padx=10, pady=5)

# Button to trigger masking
mask_button = tk.Button(root, text="Mask PII Data", command=mask_data)
mask_button.grid(row=2, column=0, columnspan=2, pady=10)

# Text widget for displaying masked document content
masked_text_label = tk.Label(root, text="Masked Document Content:")
masked_text_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
masked_text = tk.Text(root, width=50, height=10)
masked_text.grid(row=3, column=1, padx=10, pady=5)

# Button to upload masked data to Azure Blob Storage
upload_to_blob_button = tk.Button(root, text="Upload to Azure Blob", command=upload_to_azure_blob)
upload_to_blob_button.grid(row=4, column=0, padx=10, pady=5)

# Button to download masked document
download_button = tk.Button(root, text="Download", command=download_file)
download_button.grid(row=4, column=1, padx=10, pady=5)

root.mainloop()
