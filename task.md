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


#### GET /dashboard
Get comprehensive dashboard data

**Response:**
```json
{
  "success": true,
  "data": {
    "userStats": {
      "totalTestsTaken": "number",
      "averageScore": "number",
      "bestScore": "number",
      "studyStreak": "number",
      "totalStudyTime": "string",
      "completedLessons": "number",
      "currentStreak": "number"
    },
    "recentActivity": [
      {
        "id": "string (UUID)",
        "type": "string",
        "title": "string",
        "score": "number",
        "date": "string (ISO date)",
        "time": "string",
        "details": "string"
      },
      "take 3 recent activity"
    ]
  }
}
```

- Note:
