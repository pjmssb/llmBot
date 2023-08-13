import hashlib
import hmac
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def verify_signature(payload, token, received_signature):
    computed_signature = hmac.new(token.encode(), msg=payload, digestmod=hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed_signature, received_signature)

def lambda_handler(event, context):
    
    response = {
        'statusCode': 200,
        'body': json.dumps({'message': 'Received'})
    }
    
    logger.info("Received WhatsApp event: %s", json.dumps(event))
    
    version = event['version']
    logger.info("Received version: %s", json.dumps(version))
    

    
    hub_mode = event['queryStringParameters']['hub.mode']
    logger.info("Received hub_mode: %s", json.dumps(hub_mode))
    if hub_mode == 'subscribe':
        hub_challenge = event['queryStringParameters']['hub.challenge']
        logger.info("Received hub_challenge: %s", json.dumps(hub_challenge))
    
        hub_verify_token = event['queryStringParameters']['hub.verify_token']
        logger.info("Received hub_verify_token: %s", json.dumps(hub_verify_token))
        return {
              "statusCode": 200,
              "body": hub_challenge,
              "isBase64Encoded": 0
            }
    return response
    
    
    

    '''    
    received_signature = event['headers'].get('X-WhatsApp-Signature')
    logger.info("Received Signature: %s", json.dumps(received_signature))
    payload = event['body']
    logger.info("Received payload: %s", json.dumps(payload))
    
    challenge_token = event['body']
    
    #TODO: Cambiar a secret manager
    TOKEN = 'llmbot_3st33s3lS3cr3t0D3lW3bh00k'
     
    if not verify_signature(payload, TOKEN, received_signature):
        return {
            'statusCode': 403,
            'body': json.dumps({'message': 'Invalid signature'})
        }
    '''
    
