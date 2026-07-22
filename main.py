import jwt
import datetime
from functools import wraps

SECRET_KEY = "madrid_tech_secret"

def generate_token(user_id):
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow(),
        "sub": user_id
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def token_required(f):
    @wraps(f)
    def decorated(token, *args, **kwargs):
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return f(token, *args, **kwargs)
        except:
            return "Invalid or Expired Token"
    return decorated

@token_required
def get_protected_data(token):
    return "Access Granted: Welcome to the secure area!"

# Test
token = generate_token("fergodoii94")
print(f"Token: {token}")
print(get_protected_data(token))
