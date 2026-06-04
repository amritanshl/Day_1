import os
import requests
import msal

CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
TENANT_ID = os.environ.get("AZURE_TENANT_ID")
SCOPES = ["Mail.Read"]


def get_access_token():
    app = msal.PublicClientApplication(
        client_id=CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
    )
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise RuntimeError("Failed to create device flow. Check your credentials.")
    print(flow["message"])
    result = app.acquire_token_by_device_flow(flow)
    if "access_token" in result:
        return result["access_token"]
    raise RuntimeError(result.get("error_description", "Failed to obtain access token."))


def fetch_inbox_messages(access_token, top=10):
    url = "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages"
    params = {"$top": str(top), "$select": "subject,from,receivedDateTime,bodyPreview"}
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json().get("value", [])


def main():
    access_token = get_access_token()
    messages = fetch_inbox_messages(access_token, top=10)
    for msg in messages:
        sender = msg.get("from", {}).get("emailAddress", {}).get("name", "Unknown")
        subject = msg.get("subject", "")
        received = msg.get("receivedDateTime", "")
        preview = msg.get("bodyPreview", "")
        print(f"From: {sender}")
        print(f"Subject: {subject}")
        print(f"Received: {received}")
        print(f"Preview: {preview}")
        print("-" * 40)


if __name__ == "__main__":
    main()