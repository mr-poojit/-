# 🚀 LinkedIn Auto Poster (FastAPI)

This FastAPI project provides an API endpoint to automate posting text content to a LinkedIn **Company Page** using the LinkedIn Marketing API.

---

## 📌 Features

- ✅ Post content to your LinkedIn company page.
- 🔐 Uses LinkedIn OAuth 2.0 access token.
- 📡 FastAPI-based async API.
- 🔄 Easily deployable with `uvicorn`.

---

## 🛠️ Requirements

- Python 3.8+
- A valid **LinkedIn Developer App**
- Your company LinkedIn **organization URN** (e.g., `urn:li:organization:12345678`)
- Access token with the following LinkedIn **OAuth scopes**:

  - `w_organization_social`
  - `rw_organization_admin` (optional but recommended)

---

## ⚖️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/linkedin-company-poster.git
cd linkedin-company-poster
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install fastapi httpx uvicorn python-dotenv
```

### 4. Create `.env` file

In the root directory, create a `.env` file and add:

```env
LINKEDIN_ACCESS_TOKEN=your_long_lived_access_token_here
```

---

## 🚀 Running the API Server

```bash
uvicorn main:app --reload
```

Visit Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📤 API Usage

### POST `/post/company`

Posts a text update to your LinkedIn company page.

#### Request Body:

```json
{
  "content": "Hello from FastAPI LinkedIn Poster!",
  "organizationUrn": "urn:li:organization:12345678"
}
```

> ⚠️ Replace `12345678` with your **LinkedIn Company ID** (not username).

---

## 📡 How to Get Your Organization URN

1. Use LinkedIn's [Get Organizations API](https://docs.microsoft.com/en-us/linkedin/marketing/integrations/community-management/organizations/organization-lookup)
2. Or hardcode it if you know your company ID:

   ```
   urn:li:organization:<your_company_id>
   ```

---

## 🔐 How to Get a LinkedIn Access Token

1. Create a LinkedIn Developer App: [https://www.linkedin.com/developers/apps](https://www.linkedin.com/developers/apps)
2. Add permissions under “Products” (choose `w_organization_social`)
3. Follow OAuth flow to generate a token manually, or use tools like Postman to do it.
4. Save the token in `.env`

---

## 📁 Project Structure

```
linkedin-company-poster/
│
├── main.py            # FastAPI application
├── .env               # Environment variables (not committed)
├── README.md
```

---

## ✅ Sample Success Response

```json
{
  "message": "Post published successfully to company page.",
  "linkedin_response": {
    "id": "urn:li:share:123456789"
  }
}
```

---

## ⚠️ Notes

- The access token must be valid and not expired.
- The authenticated user must have **Admin** permissions on the company page.
- This project currently supports **text-only posts**. Media/image sharing requires additional configuration.

---

## 📃 License

MIT License

---

## 🤛️ Need Help?

Feel free to open an issue or reach out if you need help with:

- Token generation
- Company URN lookup
- Posting media/images
