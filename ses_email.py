import boto3
from botocore.exceptions import ClientError
import json

CHARSET = "UTF-8"
AWS_REGION = "us-west-2"

def maildata(event):
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Hey Hi...\r\n"
                "This email was sent with Amazon SES using the "
                "AWS SDK for Python (Boto)."
                "{msg}".format(msg=event['msg'])
                )

    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
        <h1>Hey Hi...</h1>
        <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
            AWS SDK for Python (Boto)</a>.<br>
            {msg}
        </p>
    </body>
    </html>
    """.format(msg=event['msg'])
    dest = list(event['to'].split(" "))
    return BODY_TEXT, BODY_HTML, dest


def sendsesmail(event):
    (BODY_TEXT, BODY_HTML, dest) = maildata(event)
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
        # Try to send the email.
    try:
    #Provide the contents of the email.
        response = client.send_email(
            Destination={'ToAddresses': dest},
            Message={
                'Body': {
                'Html': {'Data': BODY_HTML},
                'Text': {'Data': BODY_TEXT},
                },
                'Subject': {'Data': event['subject']},
            },
            Source=event['from']
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {"errorMsg":e.response['Error']['Message'], "success": "false"}
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
        return {"MessageId": response['MessageId'], "success": "true"}
        
