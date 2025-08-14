# TASK INSTRUCTION


- Instruction: add new endpoint for first time login user:

1.2 User Registration (First Time Login)
POST /api/auth/register
- Body: { email, name, targetScore, testDate }
- Response: { message: "OTP sent successfully" }

POST /api/auth/complete-registration
- Body: { email, otp, name, targetScore, testDate }
- Response: { token, user: { id, email, name, level, xp, targetScore, testDate } }
