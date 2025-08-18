# PROJECT GUIDE

- API Group is a collection of related APIs, like `auth` for authentication, `user` for user management, etc.
- create new schema for api in `app/schema/{api-group}.py`
- create new api by adding new python package in `app/api/{api-group}/`, then create api.py in that package.
- add new router from the api file to `app/route.py`
- model crud in `app/crud/{api-group}.py`

# Task in struction
- Create this API endpoint.

#### PUT /auth/profile
Update user profile

**Request Body:**
```json
{
  "name": "string (optional, 2-50 characters)",
  "email": "string (optional, valid email format)",
  "targetScore": "number (optional, 0.0-9.0)",
  "testDate": "string (optional, ISO date format YYYY-MM-DD)",
  "hasPreviousTest": "boolean (optional)",
  "lastTestScore": "number (optional, 0.0-9.0)"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "string (UUID)",
    "name": "string",
    "email": "string",
    "currentScore": "number",
    "targetScore": "number",
    "testDate": "string",
    "hasPreviousTest": "boolean",
    "lastTestScore": "number",
    "level": "number",
    "xp": "number",
    "updatedAt": "string (ISO timestamp)"
  },
  "message": "Profile updated successfully"
}
```

- Note:
