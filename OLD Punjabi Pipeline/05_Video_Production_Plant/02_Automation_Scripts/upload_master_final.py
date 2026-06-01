import os
import pickle
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

# Paths
WORKSPACE_DIR = r"f:\Punjabi_Guftar_Workspace"
CLIENT_SECRETS_FILE = os.path.join(WORKSPACE_DIR, "06_Governance", "client_secret.json")
TOKEN_PICKLE = os.path.join(WORKSPACE_DIR, "06_Governance", "token.pickle")

# Scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_authenticated_service():
    credentials = None
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            credentials = pickle.load(token)
            
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            from google.auth.transport.requests import Request
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0, open_browser=False)
            
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(credentials, token)
            
    return build('youtube', 'v3', credentials=credentials)

def upload_video(youtube, file_path, title, description, tags, category="27", privacy="private"):
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category
        },
        'status': {
            'privacyStatus': privacy,
            'selfDeclaredMadeForKids': False,
        }
    }

    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )

    print(f"Starting upload of {file_path}...")
    response = insert_request.execute()
    print(f"Video ID '{response['id']}' was successfully uploaded.")
    return response['id']

def set_thumbnail(youtube, video_id, thumbnail_path):
    print(f"Setting custom thumbnail {thumbnail_path} for video {video_id}...")
    youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(thumbnail_path)
    ).execute()
    print("Thumbnail set successfully.")

if __name__ == '__main__':
    TEST_FILE = os.path.join(WORKSPACE_DIR, "05_Final_Deliverables", "PG-002_Master_Final.mp4")
    THUMB_PATH = os.path.join(WORKSPACE_DIR, "03_Visual_Laboratory", "01_Thumbnails", "PG-002_Auto_Thumbnail.png")
    
    if not os.path.exists(TEST_FILE):
        print(f"Error: Master file not found at {TEST_FILE}")
    else:
        try:
            service = get_authenticated_service()
            video_id = upload_video(
                service, 
                TEST_FILE, 
                title="Master Final: ਪੈਂਤੀ ਅੱਖਰ (The Science of Gurmukhi)", 
                description="Final test upload with animated flashcards, intro, and logo watermark.", 
                tags=["Punjabi", "Gurmukhi", "Education"],
                privacy="private"
            )
            
            if os.path.exists(THUMB_PATH):
                set_thumbnail(service, video_id, THUMB_PATH)
            
            print("\n--- MASTER TEST SUCCESSFUL ---")
            print(f"Video URL: https://youtu.be/{video_id}")
            
        except Exception as e:
            print(f"\n--- MASTER TEST FAILED ---")
            print(f"Error detail: {e}")
