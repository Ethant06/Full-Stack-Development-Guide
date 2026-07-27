## 1. Real OAuth2 (the three-party kind)
Allowing users to sign in with Google or GitHub

## 2. JWT Token Life cycle issues

## 3. Multi-factor authentication (MFA/2FA)
Verification using SMS or Email Verification Codes

## 4. Account lifecycle features
- Email verification on signup (confirm the email is real before activating the account)
- Password reset flow (forgot-password email with a time-limited reset token — conceptually similar to what you already built with JWTs!)
- Changing password while logged in (re-verify current password first)

## 5. Writing Pytests and testing our Authentications