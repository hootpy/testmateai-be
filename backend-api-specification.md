# TestMate Backend API Specification

## Overview
This document outlines the complete backend API structure needed to support the TestMate IELTS preparation application. The API should handle user management, practice questions, mock tests, study plans, and analytics.

## Base URL
```
https://api.testmate.com/v1
```

## Authentication
All endpoints require JWT authentication except for public endpoints marked with 🔓.

## API Endpoints

### 1. User Management

#### 🔓 POST /auth/register
Register a new user

**Request Body:**
```json
{
  "name": "string (required, 2-50 characters)",
  "email": "string (required, valid email format)",
  "targetScore": "number (optional, 0.0-9.0, default: 7.0)",
  "testDate": "string (optional, ISO date format YYYY-MM-DD)"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "string (UUID)",
      "name": "string",
      "email": "string",
      "targetScore": "number",
      "testDate": "string",
      "level": "number",
      "xp": "number",
      "createdAt": "string (ISO timestamp)"
    },
    "message": "Registration successful. Please check your email for OTP."
  }
}
```

#### 🔓 POST /auth/login
Request OTP for login

**Request Body:**
```json
{
  "email": "string (required, valid email format)"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "email": "string",
    "otpExpiry": "string (ISO timestamp, 5 minutes from now)"
  },
  "message": "OTP sent to your email. Please check your inbox."
}
```

#### 🔓 POST /auth/verify-otp
Verify OTP and complete login

**Request Body:**
```json
{
  "email": "string (required, valid email format)",
  "otp": "string (required, 6-digit code)"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "string (UUID)",
      "name": "string",
      "email": "string",
      "currentScore": "number",
      "targetScore": "number",
      "testDate": "string",
      "hasPreviousTest": "boolean",
      "lastTestScore": "number",
      "level": "number",
      "xp": "number"
    },
    "token": "string (JWT token)"
  },
  "message": "Login successful"
}
```

#### POST /auth/logout
Logout user (invalidate JWT)

**Response:**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

#### GET /auth/profile
Get current user profile

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
    "createdAt": "string (ISO timestamp)",
    "updatedAt": "string (ISO timestamp)"
  }
}
```

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

### 2. User Progress & XP System

#### GET /users/progress
Get user's current progress and stats

**Response:**
```json
{
  "success": true,
  "data": {
    "level": "number",
    "xp": "number",
    "currentScore": "number",
    "targetScore": "number",
    "testDate": "string",
    "hasPreviousTest": "boolean",
    "lastTestScore": "number",
    "xpToNextLevel": "number",
    "levelProgress": "number (0-100)"
  }
}
```

#### POST /users/xp/add
Add XP to user account

**Request Body:**
```json
{
  "amount": "number (required, positive integer)",
  "source": "string (required, practice|mock_test|streak)",
  "activityId": "string (optional, UUID)"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "previousLevel": "number",
    "newLevel": "number",
    "previousXp": "number",
    "newXp": "number",
    "xpGained": "number",
    "leveledUp": "boolean"
  },
  "message": "XP added successfully"
}
```



### 3. Practice Questions

#### GET /practice/listening
Get listening practice questions

**Response:**
```json
{
  "success": true,
  "data": {
    "passages": [
      {
        "id": "string (UUID)",
        "title": "string",
        "text": "string",
        "questions": [
          {
            "id": "string (UUID)",
            "question": "string",
            "options": ["string"] (for multiple choice),
            "correct": "number" (index for multiple choice),
            "answer": "string" (for completion/short answer),
            "type": "string"
          }
        ]
      }
    ]
  }
}
```

#### GET /practice/reading
Get reading practice questions

**Response:**
```json
{
  "success": true,
  "data": {
    "passages": [
      {
        "id": "string (UUID)",
        "title": "string",
        "passage": "string",
        "questions": [
          {
            "id": "string (UUID)",
            "text": "string",
            "options": ["string"] (for multiple choice/true-false),
            "correct": "number" (index for multiple choice, 0/1 for true-false),
            "answer": "string" (for completion/short answer),
            "type": "string"
          }
        ]
      }
    ]
  }
}
```

#### GET /practice/speaking
Get speaking practice questions

**Response:**
```json
{
  "success": true,
  "data": {
    "questions": [
      {
        "id": "string (UUID)",
        "question": "string",
        "title": "string",
        "part": "string",
        "type": "speaking",
        "preparationTime": "number" (seconds)
      }
    ]
  }
}
```

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

### 4. Mock Tests

#### GET /mock-tests
Get all available mock tests

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "string (UUID)",
      "name": "string",
      "description": "string",
      "duration": "number" (minutes),
      "sections": [
        {
          "id": "string",
          "name": "string",
          "time": "string",
          "questions": "number"
        }
      ],
      "createdAt": "string (ISO timestamp)"
    }
  ]
}
```

#### GET /mock-tests/{testId}
Get specific mock test details

**Path Parameters:**
- `testId` (required): `string (UUID)`

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "string (UUID)",
    "name": "string",
    "description": "string",
    "duration": "number" (minutes),
    "sections": [
      {
        "id": "string",
        "name": "string",
        "time": "string",
        "questions": "number"
      }
    ],
    "createdAt": "string (ISO timestamp)"
  }
}
```

#### POST /mock-tests/{testId}/start
Start a mock test session

**Path Parameters:**
- `testId` (required): `string (UUID)`

**Request Body:**
```json
{
  "userId": "string (required, UUID)"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "sessionId": "string (UUID)",
    "testId": "string (UUID)",
    "startTime": "string (ISO timestamp)",
    "endTime": "string (ISO timestamp)",
    "duration": "number" (minutes)
  },
  "message": "Mock test session started"
}
```

#### POST /mock-tests/{testId}/submit
Submit mock test answers

**Path Parameters:**
- `testId` (required): `string (UUID)`

**Request Body:**
```json
{
  "sessionId": "string (required, UUID)",
  "sections": {
    "listening": {
      "answers": "object (questionId: answer)",
      "timeSpent": "number" (seconds)
    },
    "reading": {
      "answers": "object (questionId: answer)",
      "timeSpent": "number" (seconds)
    },
    "writing": {
      "task1": "string",
      "task2": "string",
      "timeSpent": "number" (seconds)
    },
    "speaking": {
      "responses": ["string"],
      "timeSpent": "number" (seconds)
    }
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "sessionId": "string (UUID)",
    "overallScore": "number",
    "sectionScores": {
      "listening": "number",
      "reading": "number",
      "writing": "number",
      "speaking": "number"
    },
    "timeSpent": "number" (seconds),
    "completedAt": "string (ISO timestamp)"
  },
  "message": "Mock test submitted successfully"
}
```

#### GET /mock-tests/{testId}/results
Get mock test results and analysis

**Path Parameters:**
- `testId` (required): `string (UUID)`

**Query Parameters:**
- `sessionId` (required): `string (UUID)`

**Response:**
```json
{
  "success": true,
  "data": {
    "sessionId": "string (UUID)",
    "overallScore": "number",
    "sectionScores": {
      "listening": "number",
      "reading": "number",
      "writing": "number",
      "speaking": "number"
    },
    "analysis": {
      "strengths": ["string"],
      "weaknesses": ["string"],
      "recommendations": ["string"]
    },
    "timeSpent": "number" (seconds),
    "completedAt": "string (ISO timestamp)"
  }
}
```

### 5. Study Plans

#### GET /study-plans
Get available study plan templates

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "string (UUID)",
      "name": "string",
      "description": "string",
      "duration": "number" (weeks),
      "targetScore": "number",
      "weeklyHours": "number",
      "suitableFor": ["string"],
      "structure": [
        {
          "week": "number",
          "focus": "string",
          "dailyTasks": ["string"],
          "weeklyGoals": ["string"]
        }
      ]
    }
  ]
}
```

#### GET /study-plans/{planId}
Get specific study plan details

**Path Parameters:**
- `planId` (required): `string (UUID)`

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "string (UUID)",
    "name": "string",
    "description": "string",
    "duration": "number" (weeks),
    "targetScore": "number",
    "weeklyHours": "number",
    "suitableFor": ["string"],
    "structure": [
      {
        "week": "number",
        "focus": "string",
        "dailyTasks": ["string"],
        "weeklyGoals": ["string"]
      }
    ]
  }
}
```

#### POST /study-plans/generate
Generate personalized study plan

**Request Body:**
```json
{
  "currentScore": "number (required, 0.0-9.0)",
  "targetScore": "number (required, 0.0-9.0)",
  "testDate": "string (required, ISO date format YYYY-MM-DD)",
  "availableHours": "number (required, positive integer)",
  "weakAreas": ["string"] (optional)
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "string (UUID)",
    "summary": "string",
    "weeks": "number",
    "recommendations": ["string"],
    "focus_areas": [
      {
        "skill": "string",
        "reason": "string"
      }
    ],
    "weekly_schedule": [
      {
        "week": "number",
        "focus": "string",
        "tasks": ["string"]
      }
    ]
  },
  "message": "Study plan generated successfully"
}
```

#### GET /users/study-plan
Get user's current study plan

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "string (UUID)",
    "templateId": "string (UUID)",
    "summary": "string",
    "weeks": "number",
    "currentWeek": "number",
    "recommendations": ["string"],
    "focus_areas": [
      {
        "skill": "string",
        "reason": "string"
      }
    ],
    "weekly_schedule": [
      {
        "week": "number",
        "focus": "string",
        "tasks": ["string"],
        "completed": "boolean"
      }
    ],
    "progress": {
      "completedWeeks": "number",
      "totalTasks": "number",
      "completedTasks": "number"
    }
  }
}
```

#### PUT /users/study-plan
Update user's study plan

**Request Body:**
```json
{
  "planId": "string (required, UUID)",
  "customizations": "object (optional)"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "string (UUID)",
    "updatedAt": "string (ISO timestamp)"
  },
  "message": "Study plan updated successfully"
}
```

#### POST /study-plans/{planId}/progress
Update study plan progress

**Path Parameters:**
- `planId` (required): `string (UUID)`

**Request Body:**
```json
{
  "week": "number (required, positive integer)",
  "completedTasks": ["string"] (required),
  "timeSpent": "number (required, positive integer)"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "week": "number",
    "completedTasks": ["string"],
    "timeSpent": "number",
    "progress": "number" (0-100)
  },
  "message": "Progress updated successfully"
}
```

### 6. Practice Activities & Analytics

#### POST /practice/submit
Submit practice session results

**Request Body:**
```json
{
  "type": "string (required, listening|reading|writing|speaking)",
  "questionType": "string (required)",
  "answers": "object (required, questionId: answer)",
  "timeSpent": "number (required, positive integer)",
  "score": "number (required, 0.0-9.0)",
  "band": "number (required, 0.0-9.0)",
  "details": "object (optional)"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "activityId": "string (UUID)",
    "type": "string",
    "practiceType": "string",
    "score": "number",
    "band": "number",
    "xpEarned": "number",
    "timeSpent": "number",
    "createdAt": "string (ISO timestamp)"
  },
  "message": "Practice session submitted successfully"
}
```

#### GET /users/activities
Get user's activities

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "string (UUID)",
      "type": "string",
      "practiceType": "string",
      "score": "number",
      "band": "number",
      "details": "object",
      "xpEarned": "number",
      "createdAt": "string (ISO timestamp)"
    }
  ]
}
```

#### GET /users/analytics
Get user's performance analytics

**Response:**
```json
{
  "success": true,
  "data": {
    "overallStats": {
      "totalSessions": "number",
      "averageScore": "number",
      "bestScore": "number",
      "totalTimeSpent": "number" (minutes),
      "totalXpEarned": "number"
    },
    "skillStats": {
      "listening": {
        "sessions": "number",
        "averageScore": "number",
        "bestScore": "number",
        "timeSpent": "number"
      },
      "reading": {
        "sessions": "number",
        "averageScore": "number",
        "bestScore": "number",
        "timeSpent": "number"
      },
      "writing": {
        "sessions": "number",
        "averageScore": "number",
        "bestScore": "number",
        "timeSpent": "number"
      },
      "speaking": {
        "sessions": "number",
        "averageScore": "number",
        "bestScore": "number",
        "timeSpent": "number"
      }
    }
  }
}
```

### 7. Vocabulary Management

#### GET /vocabulary
Get user's vocabulary list

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "string (UUID)",
      "word": "string",
      "definition": "string",
      "source": "string",
      "reviewed": "boolean",
      "mastered": "boolean",
      "notes": "string",
      "createdAt": "string (ISO timestamp)"
    }
  ]
}
```

#### POST /vocabulary
Add new vocabulary words

**Request Body:**
```json
{
  "words": ["string"] (required, array of words),
  "source": "string (required, practice|mock_test|manual)",
  "context": "string (optional)"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "addedWords": "number",
    "duplicateWords": "number",
    "words": [
      {
        "id": "string (UUID)",
        "word": "string",
        "source": "string",
        "createdAt": "string (ISO timestamp)"
      }
    ]
  },
  "message": "Vocabulary words added successfully"
}
```

#### PUT /vocabulary/{wordId}
Update vocabulary word status

**Path Parameters:**
- `wordId` (required): `string (UUID)`

**Request Body:**
```json
{
  "reviewed": "boolean (optional)",
  "mastered": "boolean (optional)",
  "notes": "string (optional)"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "string (UUID)",
    "word": "string",
    "reviewed": "boolean",
    "mastered": "boolean",
    "notes": "string",
    "updatedAt": "string (ISO timestamp)"
  },
  "message": "Vocabulary word updated successfully"
}
```

#### DELETE /vocabulary/{wordId}
Remove vocabulary word

**Path Parameters:**
- `wordId` (required): `string (UUID)`

**Response:**
```json
{
  "success": true,
  "message": "Vocabulary word removed successfully"
}
```

### 8. AI Analysis

#### POST /ai/analyze
Generate AI analysis and feedback

**Request Body:**
```json
{
  "prompt": "string (required, the complete prompt to send to AI)",
  "context": "object (optional, additional context data)",
  "type": "string (optional, listening|reading|writing|speaking|study_plan|vocabulary|progress)"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "analysis": "object (AI response in JSON format)",
    "type": "string",
    "createdAt": "string (ISO timestamp)"
  }
}
```

### 9. Dashboard Data

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
      }
    ],
    "progressCharts": {
      "scoreProgress": [
        {
          "date": "string (ISO date)",
          "score": "number"
        }
      ],
      "skillProgress": {
        "listening": "number",
        "reading": "number",
        "writing": "number",
        "speaking": "number"
      },
      "weeklyStudyTime": [
        {
          "week": "string",
          "hours": "number"
        }
      ]
    },
    "upcomingTasks": [
      {
        "id": "string (UUID)",
        "title": "string",
        "type": "string",
        "dueDate": "string (ISO date)",
        "priority": "string",
        "estimatedTime": "string"
      }
    ],
    "recommendations": [
      {
        "id": "string (UUID)",
        "title": "string",
        "description": "string",
        "type": "string",
        "priority": "string"
      }
    ]
  }
}
```



## Database Schema

### Users Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  current_score DECIMAL(3,1) DEFAULT 0,
  target_score DECIMAL(3,1) DEFAULT 7.0,
  test_date DATE,
  has_previous_test BOOLEAN DEFAULT FALSE,
  last_test_score DECIMAL(3,1),
  level INTEGER DEFAULT 1,
  xp INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### OTP Table
```sql
CREATE TABLE otp_codes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL,
  otp_code VARCHAR(6) NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  used BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Practice Questions Table
```sql
CREATE TABLE practice_questions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  skill VARCHAR(50) NOT NULL, -- listening, reading, speaking, writing
  question_type VARCHAR(50) NOT NULL, -- multipleChoice, sentenceCompletion, etc.
  passage_id UUID REFERENCES passages(id),
  question_text TEXT NOT NULL,
  options JSONB, -- For multiple choice questions
  correct_answer TEXT,
  explanation TEXT,
  difficulty_level VARCHAR(20) DEFAULT 'intermediate',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Passages Table
```sql
CREATE TABLE passages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  skill VARCHAR(50) NOT NULL,
  question_type VARCHAR(50) NOT NULL,
  difficulty_level VARCHAR(20) DEFAULT 'intermediate',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Mock Tests Table
```sql
CREATE TABLE mock_tests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  duration INTEGER NOT NULL, -- in minutes
  sections JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### User Activities Table
```sql
CREATE TABLE user_activities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  type VARCHAR(50) NOT NULL, -- practice, mock_test, study_plan
  practice_type VARCHAR(50), -- listening, reading, writing, speaking
  score DECIMAL(3,1),
  band DECIMAL(3,1),
  details JSONB,
  xp_earned INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Vocabulary Table
```sql
CREATE TABLE vocabulary (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  word VARCHAR(255) NOT NULL,
  definition TEXT,
  source VARCHAR(50) DEFAULT 'practice',
  reviewed BOOLEAN DEFAULT FALSE,
  mastered BOOLEAN DEFAULT FALSE,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Study Plans Table
```sql
CREATE TABLE study_plans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  template_id UUID,
  customizations JSONB,
  current_week INTEGER DEFAULT 1,
  progress JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### AI Feedback Table
```sql
CREATE TABLE ai_feedback (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  activity_id UUID REFERENCES user_activities(id),
  skill VARCHAR(50) NOT NULL,
  feedback_data JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
