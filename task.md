# PROJECT GUIDE

- API Group is a collection of related APIs, like `auth` for authentication, `user` for user management, etc.
- create new schema for api in `app/schema/{api-group}.py`
- create new api by adding new python package in `app/api/{api-group}/`, then create api.py in that package.
- add new router from the api file to `app/route.py`
- model crud in `app/crud/{api-group}.py`

# Task in struction
- Create this API endpoint.
- Ask any question if needed
- Move any utility functions to utils folder

#### GET /practice/writing
Get writing practice questions

**Response:**
```json
{
  "success": true,
  "data": {
    "prompts": [
      {
        "id": "string (UUID)",
        "question": "string",
        "title": "string",
        "type": "string",
        "timeLimit": "number" (seconds),
        "wordLimit": "string"
      }
    ]
  }
}
```

- Note:
