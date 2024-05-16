from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CustomerDocument, Customer, DocumentSet, UserProfile
from .utils import extract_text_from_document
from .forms import UploadForm
from django.db import IntegrityError

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, "dashboard.html")
    return redirect("/accounts/login/")


def upload_document(request):
    
    if not request.user.is_authenticated:
        return redirect('dashboard')

    user_country = UserProfile.objects.get(user__username=request.user).country
    if request.method == "POST":
        documents = [request.FILES.get(doc) for doc in request.FILES]
        selected_document_type = DocumentSet.objects.get(
            pk=request.POST.get("document_set_list")
        )

        #validation for backside compulsion
        if selected_document_type.has_backside and len(documents) < 2:
            return render(request, 'failure.html', {'message':"This documnet requires both sides"})

        extracted_text = extract_text_from_document(documents)

        if "text" in extracted_text:
            #considering fields that are present in ocr_labels
            ModelFields = selected_document_type.ocr_labels["labels"].split(",")
            cleaned_data = {
                key.lower(): value
                for key, value in extracted_text["text"].items()
                if key.lower() in ModelFields
            }

            #creating customer from extracted data
            try:
                customer = Customer.objects.create(
                    **cleaned_data,
                    created_by=request.user,
                    nationality=user_country,
                    document=selected_document_type,
                )
            except IntegrityError:
                return render(request, 'failure.html', {'message':'Customer Already Exists!'})


            #creating customer document
            document_dict = {
                "customer": customer,
                "file_front": documents[0],
                "extracted_data": extracted_text["text"],
            }
            if selected_document_type.has_backside:
                document_dict["file_back"] = documents[1]
            CustomerDocument.objects.create(**document_dict)

            return render(request, "success.html")
        else:
            return HttpResponse("Error", status=400)
    else:
        form = UploadForm()
    documents = DocumentSet.objects.filter(countries=user_country)
    return render(
        request,
        "upload.html",
        {"form": form, "documents": documents, "country": user_country.name},
    )
