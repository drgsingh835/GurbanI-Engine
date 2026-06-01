import os
import sys
import pickle
import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

# Setup workspace directory
WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CLIENT_SECRETS_FILE = os.path.join(WORKSPACE_DIR, "config", "youtube", "client_secret.json")
TOKEN_PICKLE = os.path.join(WORKSPACE_DIR, "config", "youtube", "token.pickle")
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_authenticated_service():
    credentials = None
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            try:
                credentials = pickle.load(token)
                print("[+] Loaded OAuth credentials from cache (token.pickle)")
            except Exception as e:
                print(f"[!] Warning: Failed to load token.pickle ({e})")
            
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            from google.auth.transport.requests import Request
            print("[*] OAuth credentials expired. Refreshing token...")
            try:
                credentials.refresh(Request())
            except Exception as e:
                print(f"[!] Failed to refresh credentials: {e}. Starting fresh auth flow...")
                credentials = None
                
        if not credentials:
            if not os.path.exists(CLIENT_SECRETS_FILE):
                print(f"[-] Error: Google Client Secrets file not found at: {CLIENT_SECRETS_FILE}")
                sys.exit(1)
            print("[*] Initiating YouTube OAuth flow...")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0, open_browser=False)
            
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(credentials, token)
            print("[+] Saved updated credentials to token.pickle")
            
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

    print(f"[*] Starting upload of {file_path}...")
    response = None
    while response is None:
        status, response = insert_request.next_chunk()
        if status:
            print(f"[*] Uploaded {int(status.progress() * 100)}%.")
    
    print(f"[+] Video ID '{response['id']}' was successfully uploaded.")
    return response['id']

def set_thumbnail(youtube, video_id, thumbnail_path):
    print(f"[*] Setting custom thumbnail {thumbnail_path} for video {video_id}...")
    try:
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(thumbnail_path)
        ).execute()
        print("[+] Thumbnail set successfully.")
    except Exception as e:
        print(f"[!] Error setting thumbnail: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Programmatic YouTube Video Uploader")
    parser.add_argument("--video", required=True, help="Path to video file")
    parser.add_argument("--thumbnail", help="Path to custom thumbnail image")
    parser.add_argument("--title", required=True, help="Video title")
    parser.add_argument("--description", default="", help="Video description")
    parser.add_argument("--tags", default="", help="Comma separated list of tags")
    parser.add_argument("--privacy", default="private", choices=["private", "unlisted", "public"], help="Privacy status")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.video):
        print(f"[-] Video file not found: {args.video}")
        sys.exit(1)
        
    tag_list = [tag.strip() for tag in args.tags.split(",") if tag.strip()]
    
    try:
        service = get_authenticated_service()
        video_id = upload_video(
            service, 
            args.video, 
            title=args.title, 
            description=args.description, 
            tags=tag_list,
            privacy=args.privacy
        )
        
        if args.thumbnail and os.path.exists(args.thumbnail):
            set_thumbnail(service, video_id, args.thumbnail)
            
        print("\n[+] UPLOAD COMPLETED SUCCESSFULLY!")
        print(f"[+] Video URL: https://youtu.be/{video_id}")
        
    except Exception as e:
        print(f"\n[-] Upload process failed: {e}")
        sys.exit(1)
