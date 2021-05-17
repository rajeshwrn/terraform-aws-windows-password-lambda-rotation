import boto3
import logging
import os
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)
kms_key_id = os.environ['KMS_KEY_ID']

def lambda_handler(event, context):
    arn = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']

    print('---- Inside the lambda_handler ----')
    print('Secret arn:')
    print(arn)
    # Setup the client
    service_client = boto3.client('secretsmanager', endpoint_url=os.environ['SECRETS_MANAGER_ENDPOINT'])

    if step == "createSecret":
        create_secret(service_client, arn, token)

    elif step == "setSecret":
        set_secret(service_client, arn, token)

    elif step == "testSecret":
        test_secret(service_client, arn, token)

    elif step == "finishSecret":
        finish_secret(service_client, arn, token)

    else:
        raise ValueError("Invalid step parameter")


def create_secret(service_client, arn, token):
    print('------ Inside create_secret ------')
    mysecretresponse = service_client.describe_secret(SecretId=arn)
    print("mysecretresponse",mysecretresponse)
    # we need this unicode conversion because the tags are in unicode and we have back errors
    for tag in mysecretresponse['Tags']:
        if tag['Key'] == 'instanceid':
            instance = tag['Value']

    print('working on instnaceid ' + str(instance))
    client = boto3.client('ssm')

    try:
        # Generate a random password
        print('Generating new password')
        # create a parameter store to pass the new generated password in a secure way
        ssm = "alias/aws/ssm"
        print('Send command to change the password to the instance')
        response = client.send_command(DocumentName="AWSSupport-RunEC2RescueForWindowsTool",
                                       Targets=[{"Key": "InstanceIds", "Values": [instance]}],
                                       Parameters={"Command": ["ResetAccess"], "Parameters": [ssm]}, TimeoutSeconds=600,
                                       MaxConcurrency="50", MaxErrors="0")
        print("send_command : ", response)
        print('sleepping')
        time.sleep(60)
        response = client.get_parameter(
            Name="/EC2Rescue/Passwords/"+instance,
            WithDecryption=True
        )
        print(response)
        print('Put the new password in a secret')
        secure_string = '{ \"Administrator\": \"' + response['Parameter']['Value'] + '\"\n }'
        print('password :' + response['Parameter']["Value"])
        service_client.put_secret_value(SecretId=arn, ClientRequestToken=token, SecretString=secure_string,
                                        VersionStages=['AWSCURRENT'])
        logger.info("createSecret: Successfully put secret for ARN %s and version %s." % (arn, token))
        # Before delete the parameter we need to wait some seconds that the powershell will be executed
        # the above send_command is asyncronous
        print('Delete parameter')
        response = client.delete_parameter(
            Name="/EC2Rescue/Passwords/"+instance,
        )
        time.sleep(20)
        return True
    except Exception as e:
        print("Error")
        print(e)
        return False


def set_secret(service_client, arn, token):
    print('------ Inside set_secret ------')
    print('nothing to be done here left because secret manager needs to call this')
    return True


def test_secret(service_client, arn, token):
    print('------ Inside test_secret ------')
    print('nothing to be done here left because secret manager needs to call this')
    return True


def finish_secret(service_client, arn, token):
    print('------ Inside finish_secret ------')
    print('nothing to be done here left because secret manager needs to call this')
    return True
