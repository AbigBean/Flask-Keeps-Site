from itsdangerous import URLSafeTimedSerializer

# Serializer for generating tokens
s = URLSafeTimedSerializer('<<your secret frase from config file>>') #example: S#perS3crEt_007

def generate_reset_token(email):
    return s.dumps(email, salt='email-reset-salt')

def verify_reset_token(token, expiration=3600):
    try:
        email = s.loads(token, salt='email-reset-salt', max_age=expiration)
    except:
        return None
    return email
