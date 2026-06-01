import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

# Paths
WORKSPACE_DIR = r"f:\Punjabi_Guftar_Workspace"
CLIENT_SECRETS_FILE = os.path.join(WORKSPACE_DIR, "06_Governance", "client_secret.json")

# Scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    # Don't open the browser automatically; print the URL so the agent can handle it.
    credentials = flow.run_local_server(port=0, open_browser=False)
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

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
    response = None
    while response is None:
        status, response = insert_request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%.")
    
    print(f"Video ID '{response['id']}' was successfully uploaded.")
    return response['id']

def set_thumbnail(youtube, video_id, thumbnail_path):
    print(f"Setting thumbnail {thumbnail_path} for video {video_id}...")
    youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(thumbnail_path)
    ).execute()
    print("Thumbnail set successfully.")

if __name__ == '__main__':
    print("Script execution started...")
    # SYSTEM TEST CONFIGURATION
    TEST_FILE = os.path.join(WORKSPACE_DIR, "05_Final_Deliverables", "test_02_alphabets_rough_cut.mp4")
    
    if not os.path.exists(TEST_FILE):
        print(f"Error: Test file not found at {TEST_FILE}")
    else:
        print("--- STARTING YOUTUBE API SYSTEM TEST ---")
        print("Note: A browser window will open. Please authorize the 'Punjabi Guftar Desktop Uploader'.")
        
        try:
            # 1. Authenticate
            service = get_authenticated_service()
            
            # 2. Upload (Private for safety)
            video_id = upload_video(
                service, 
                TEST_FILE, 
                title="API System Test: ਪੈਂਤੀ ਅੱਖਰ (Rough Cut)", 
                description="This is an automated test upload for the Punjabi Guftar pipeline. Status: System Audit.", 
                tags=["Punjabi", "Gurmukhi", "Education", "Test"],
                privacy="private" # Upload as private first
            )
            
            # 3. Set Thumbnail if available
            THUMB_PATH = os.path.join(WORKSPACE_DIR, "03_Visual_Laboratory", "01_Thumbnails", "PG-002_Auto_Thumbnail.png")
            if os.path.exists(THUMB_PATH):
                set_thumbnail(service, video_id, THUMB_PATH)
            
            print("\n--- TEST SUCCESSFUL ---")
            print(f"Video is now on YouTube (Private). URL: https://youtu.be/{video_id}")
            print("Next step: Manually check the Google Cloud Console Quota page.")
            
        except Exception as e:
            print(f"\n--- TEST FAILED ---")
            print(f"Error detail: {e}")
