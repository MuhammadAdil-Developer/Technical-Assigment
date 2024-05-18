import jwt
import datetime
import re
from Api.models import *

def checkemailforamt(email):
    emailregix = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if(re.match(emailregix, email)):

        return True

    else:
       return False



##both keys and required field validation


def passwordLengthValidator(password):
    if not (re.search(r'[!@#$%^&*(),.?":{}|<>]', password) and re.search(r'[A-Z]', password) and 8 <= len(password) <= 20):
        return False
    return True

  

def keystatus (reqData, requireFeilds):
    try:
        for i in requireFeilds:
            if i not in reqData:
                return False
        return True
    except:
        return False

def feildstatus (reqData, requireFeilds):
    try:
        for i in requireFeilds:
            if len(reqData[i]) == 0:
                return False
        return True
    except:
        return False

def requireFeildValidation(reqData, requireFeilds):
    try:
        key_status = keystatus(reqData, requireFeilds)
        feild_status = feildstatus(reqData, requireFeilds)
        if not key_status:
            return {"status": False, "message": f"{requireFeilds} All keys are required "}
        if not feild_status:
            return {"status": False, "message": f"{requireFeilds} All fields must be filled "}  # Changed "feild" to "field"
        return {"status": True}
    except Exception as e:
        return {"status": False, "message": str(e)}



def blacklisttoken(id,token):
    try:
        UserToken.objects.get(user = id,token = token).delete()
        return True
    
    except:
        return False


def generatedToken(fetchuser,authKey,totaldays,request):
    try:
        access_token_payload = {
            'id': str(fetchuser.id),
            'email':fetchuser.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=totaldays),
            'iat': datetime.datetime.utcnow(),

        }
        
        userpayload = { 'id': str(fetchuser.id),'email':fetchuser.email,'fname':fetchuser.fname,'lname':fetchuser.lname,'profile':fetchuser.profile.url,'role':fetchuser.role}
    
        access_token = jwt.encode(access_token_payload,authKey, algorithm='HS256')
        blacklisttoken(user = fetchuser,token = access_token).save()
        return {"status":True,"token":access_token,"payload":userpayload}

    except Exception as e:
        return {"status":False,"message":"Something went wrong in token creation","details":str(e)}


def execptionhandler(val):
    if 'error' in val.errors:
        error = val.errors["error"][0]
    else:
        key = next(iter(val.errors))
        error = key + ", "+val.errors[key][0]

    return error

