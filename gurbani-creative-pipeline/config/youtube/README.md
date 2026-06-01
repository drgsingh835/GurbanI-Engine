# YouTube OAuth Configuration Guide

To publish videos to YouTube automatically, you must configure Google OAuth credentials in this directory.

## Required Files

1. **`client_secret.json`**:
   * Get this file from the [Google Cloud Console](https://console.cloud.google.com/).
   * Enable the **YouTube Data API v3** in your Google Cloud Project.
   * Go to **APIs & Services** > **Credentials**, create an **OAuth 2.0 Client ID** (Desktop Application), and click **Download JSON**.
   * Rename the downloaded file to `client_secret.json` and place it in this folder.

2. **`token.pickle`**:
   * This file is generated automatically when you run the pipeline for the first time.
   * A browser window will open asking you to authorize the application with your YouTube/Google account.
   * Once authorization is complete, the API credentials will be cached in this folder as `token.pickle` for future automated runs.

> [!WARNING]
> Keep both of these files secret! Never commit them to a public Git repository. They are ignored by the root-level `.gitignore` file.
