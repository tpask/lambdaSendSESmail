import json
from ses_email import sendsesmail

mailInfo={
  "from": "from.address@domain.com",
  "to": "to.address@domain.com",
  "msg": "The message in the body of email"
  "subject": "The subject of the message"
}

def lambda_handler(event, context):
    resp = sendsesmail(event)
    print(resp)
    return {resp}
