import boto3
from django.conf import settings
from textractcaller import call_textract_analyzeid


def extract_text_from_document(document_bytes):
    client = boto3.client(
        "textract",
        region_name=settings.AWS_SES_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    Docs = [doc.read() for doc in document_bytes]
    response = call_textract_analyzeid(
        document_pages=Docs, boto3_textract_client=client
    )
    extracted_data = {}
    for doc_fields in response["IdentityDocuments"]:
        for id_field in doc_fields["IdentityDocumentFields"]:
            doc_key = None
            doc_val = None
            for key, val in id_field.items():
                if "Type" in str(key):
                    doc_key = str(val["Text"])
            for key, val in id_field.items():
                if "ValueDetection" in str(key):
                    doc_val = str(val["Text"])
            if doc_val != "" and doc_key not in extracted_data:
                extracted_data[doc_key] = doc_val
    if extracted_data:
        return {"text": extracted_data}
    return {"error": "Failed to extract text from document."}
