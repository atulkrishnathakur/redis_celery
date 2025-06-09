from fastapi.staticfiles import StaticFiles

def mount_uploaded_files(app):
    UPLOAD_DIRECTORY = "uploads"
    app.mount("/uploads", StaticFiles(directory=UPLOAD_DIRECTORY), name="uploads")

def mount_generated_pdf(app):
    UPLOAD_DIRECTORY = "generated_pdf"
    app.mount("/pdf", StaticFiles(directory=UPLOAD_DIRECTORY), name="generated_pdf")