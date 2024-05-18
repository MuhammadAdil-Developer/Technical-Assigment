from decouple import config
import jwt, datetime
from Api.models import *


def UserGenerateToken(fetchuser):
    try:
        secret_key = config("user_jwt_token")
        total_days = 1
        token_payload = {
            "id": str(fetchuser.id),
            "email":fetchuser.email,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=total_days),
            # "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1),  
              
        }
        detail_payload = {
            "id": str(fetchuser.id),
            "email":fetchuser.email,
            "first_name": fetchuser.fname,
            "last_name": fetchuser.lname,
        }
        token = jwt.encode(token_payload, key= secret_key, algorithm="HS256")
        UserToken.objects.create(user = fetchuser, token = token)
        return {"status": True, "token" : token, "payload": detail_payload}
    except Exception as e:
        return {"status": False, "message": f"Error during generationg token {str(e)}"}
    # except Exception as e:
    #     return {"status": False, "message": f"Error during generationg token {str(e)}"}


def UserDeleteToken(fetchuser, request):
    try:
        token = request.META["HTTP_AUTHORIZATION"][7:]
        whitelist_token = UserToken.objects.filter(user = fetchuser.id, token = token).first()
        whitelist_token.delete()
        admin_all_tokens = UserToken.objects.filter(user = fetchuser)
        for fetch_token in admin_all_tokens:
            try:
                decode_token = jwt.decode(fetch_token.token, config('user_jwt_token'), "HS256")
            except:    
                fetch_token.delete()
        return True
    except Exception :
        return False