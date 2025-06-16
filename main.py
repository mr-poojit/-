from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import httpx
import os

app = FastAPI()

# LinkedIn OAuth credentials
CLIENT_ID = "client_id"
CLIENT_SECRET = "client_secret"
REDIRECT_URI = "http://localhost:8000/auth/linkedin/callback"

# Use a valid access token
ACCESS_TOKEN = "your_access_token"
# LinkedIn API endpoints
LINKEDIN_ME_URL = "https://api.linkedin.com/v2/userinfo"
LINKEDIN_UGC_POSTS_URL = "https://api.linkedin.com/v2/ugcPosts"

class ProfilePostRequest(BaseModel):
    content: str

class CompanyPostRequest(BaseModel):
    content: str
    organizationUrn: str

def create_post_payload(author_urn: str, content_text: str):
    return {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content_text
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

@app.post("/post/profile")
async def post_to_profile(request: ProfilePostRequest):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "X-Restli-Protocol-Version": "2.0.0",
        "LinkedIn-Version": "202410"
    }

    async with httpx.AsyncClient() as client:
        # Step 1: Fetch user info to get member URN
        profile_response = await client.get(LINKEDIN_ME_URL, headers=headers)
        if profile_response.status_code != 200:
            raise HTTPException(
                status_code=profile_response.status_code,
                detail={
                    "error": profile_response.text,
                    "message": "Failed to fetch user profile. Token might be invalid or expired."
                }
            )

        profile_data = profile_response.json()
        member_id = profile_data.get("sub") or profile_data.get("id")
        if not member_id:
            raise HTTPException(status_code=500, detail="User ID not found in profile response.")

        author_urn = f"urn:li:person:{member_id}"
        post_payload = create_post_payload(author_urn, request.content)

        # Step 2: Post content
        post_response = await client.post(LINKEDIN_UGC_POSTS_URL, json=post_payload, headers=headers)
        if post_response.status_code not in (200, 201):
            raise HTTPException(
                status_code=post_response.status_code,
                detail={
                    "error": post_response.text,
                    "message": "Failed to post content to LinkedIn."
                }
            )

        return {
            "message": "Post successfully published to LinkedIn profile",
            "linkedin_response": post_response.json()
        }
    
class CompanyPostRequest(BaseModel):
    content: str
    organizationUrn: str  # e.g. "urn:li:organization:12345678"

def create_company_post_payload(org_urn: str, content_text: str):
    return {
        "author": org_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content_text
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

@app.post("/post/company")
async def post_to_company(request: CompanyPostRequest):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "X-Restli-Protocol-Version": "2.0.0",
        "LinkedIn-Version": "202410",
        "Content-Type": "application/json"
    }

    payload = create_company_post_payload(request.organizationUrn, request.content)

    async with httpx.AsyncClient() as client:
        response = await client.post(LINKEDIN_UGC_POSTS_URL, json=payload, headers=headers)

    if response.status_code not in (200, 201):
        raise HTTPException(
            status_code=response.status_code,
            detail={
                "error": response.text,
                "message": "Failed to post to company page. Make sure token is valid and user is an admin of the organization."
            }
        )

    return {
        "message": "Successfully posted to company page.",
        "linkedin_response": response.json()
    }
