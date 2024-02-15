import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os
from datetime import datetime
import uuid
from pymongo import MongoClient
from config import MONGO_CONNECTION_STRING, TESSERACT_CMD_PATH

# Connect to MongoDB
client = MongoClient(MONGO_CONNECTION_STRING)
db = client['ragLS']
documents_collection = db['docs']
images_collection = db['imgs']

# Tesseract file path
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD_PATH

# Extract text from the page
def extract_content_from_page(doc, page):
    text = page.get_text("text")
    print("Text extracted from page.")

    # Check if page is a table of contents and skip if it is
    if "table of contents" in text.lower():
        print("Skipping 'Table of Contents' page.")
        return "", []

    # Extract images and perform OCR if PDF is scanned
    images_info = []
    for img_index, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        img_dict = doc.extract_image(xref)
        
        if img_dict is None:  # Check if the image extraction is successful
            print(f"Unable to extract image {img_index} on page.")
            continue

        img_bytes = img_dict.get("image", None)

        if img_bytes:
            try:
                # Create an Image object
                image = Image.open(io.BytesIO(img_bytes))

                # Perform OCR to get associated text with the image
                associated_text = pytesseract.image_to_string(image).strip()
                print(f"Image {img_index} OCR processed.")

                # Save the image locally
                image_id = str(uuid.uuid4())
                image_path = f'C:/ragLS/docs/images/{image_id}.png'
                image.save(image_path, "PNG")
                print(f"Image {img_index} saved at {image_path}.")

                images_info.append({
                    "image_id": image_id,
                    "document_id": None,  # Will link in document entry function 
                    "file_path": image_path,
                    "associated_text": associated_text,
                    "tags": []  
                })
            except IOError:
                print(f"Unable to process image {img_index} on page: Invalid image data.")
        else:
            print(f"No valid image data found for image {img_index} on page.")

    return text, images_info

# Process the PDF content into Mongo collection
def process_pdf(pdf_path):
    file_name = os.path.basename(pdf_path)

    # Check if PDF already exists in Mongo
    if documents_collection.count_documents({"file_name": file_name}) > 0:
        print(f"Document '{file_name}' already exists in the database. Skipping.")
        return

    print(f"Processing document: {file_name}")
    document_id = str(uuid.uuid4())
    with fitz.open(pdf_path) as doc:
        all_text_content = ""
        all_images_info = []
        
        for page in doc:
            text, images_info = extract_content_from_page(doc, page)
            all_text_content += text
            for img_info in images_info:
                img_info["document_id"] = document_id
                images_collection.insert_one(img_info)
            all_images_info.extend(images_info)

        # Create and insert document entry
        document_entry = {
            "document_id": document_id,
            "file_name": file_name,
            "upload_date": datetime.now(),
            "last_modified": datetime.now(),
            "text_content": all_text_content,
            "related_docs": [],
            "summary": "", 
            "tags": [],  # Add tags at later date
            "category": "",  
            "author": "",  
            "source": "",  
            "images": [img["image_id"] for img in all_images_info],
            "vector_representation": None,  # Generate vectors at later date
            "question_answer_pairs": [],  
            "user_queries": [],  
            "feedback": []  
        }

        documents_collection.insert_one(document_entry)
        print(f"Document '{file_name}' processed and stored in database.")

# Local PDF directory
docs_directory = 'C:/ragLS/docs'
for filename in os.listdir(docs_directory):
    if filename.lower().endswith('.pdf'):
        pdf_path = os.path.join(docs_directory, filename)
        process_pdf(pdf_path)

print("Processing complete.")
