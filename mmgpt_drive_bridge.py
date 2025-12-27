from fastapi import FastAPI
from pydantic import BaseModel
from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import Optional

app = FastAPI(
    title="MMGPT Drive Bridge",
    description="API bridge that connects MMGPT to Google Drive for reading and embedding SOPs, CSVs, and trading data.",
    version="1.0.0"
)

SERVICE_ACCOUNT_FILE = "mmgpt_drive_credentials.json"

class DriveCommand(BaseModel):
    command: str
    file_id: Optional[str] = None

def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    return build("drive", "v3", credentials=creds)

@app.post("/drive", tags=["Drive Operations"])
def drive_action(payload: DriveCommand):
    service = get_drive_service()

    if payload.command == "list_files":
        results = service.files().list(
            q="'1jDfZIBmYOvvvv0HOfwBpr3a1iJ6j9Oe_' in parents",
            pageSize=50,
            fields="files(id, name)"
        ).execute()
        return {"files": results.get("files", [])}

    elif payload.command == "get_file" and payload.file_id:
        metadata = service.files().get(fileId=payload.file_id, fields="id, name, mimeType").execute()
        content = service.files().get_media(fileId=payload.file_id).execute()
        return {"meta": metadata, "content": content.decode("utf-8", errors="ignore")}

    return {"error": "Invalid command or missing file_id"}

@app.get("/", tags=["System"])
def root():
    return {"status": "MMGPT Drive Bridge running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mmgpt_drive_bridge:app", host="0.0.0.0", port=5000, reload=True)

