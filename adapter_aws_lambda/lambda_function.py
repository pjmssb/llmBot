import json
import logging
import boto3

#Para depuración
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Este token utilizado sólo cuando se valida el webhook
META_VERIFICATION_TOKEN = "Este no es el token de verificación"
LLMBOT_SQS_URL = "https://sqs.us-east-1.amazonaws.com/337340005201/sqs_llmbot.fifo"

#Recursos adicionales
sqs_client = boto3.client('sqs')

def is_meta_verification(event):
    qs_params = event.get('queryStringParameters', {})
    if qs_params == None: 
        return False
    return (qs_params.get('hub.mode') == 'subscribe' and 
            qs_params.get('hub.verify_token') == META_VERIFICATION_TOKEN)
            
def get_whatsapp_message(event):
    message = {}
    data = json.loads(event['body'])['entry'];
    
    if data == None:
        return message
        
    logger.info(f"llmbot - Mensaje: {data}")
    message['mensaje_id'] = data[0]['changes'][0]['value']['messages'][0]['id']
    message['telefono_destino'] = data[0]['changes'][0]['value']['metadata']['display_phone_number']
    message['telefono_origen'] = data[0]['changes'][0]['value']['messages'][0]['from']
    message['nombre_origen'] = data[0]['changes'][0]['value']['contacts'][0]['profile']['name'] 
    message['contenido'] = data[0]['changes'][0]['value']['messages'][0]['text']['body'] 
    return message


def lambda_handler(event, context):
    logger.info("llmbot - Message arrived")
    
    user_agent = event['headers']['User-Agent'][0:8]
    if user_agent != 'facebook':
        logger.warning('El evento no tiene formato de Meta %s',json.dumps(event))
        return  {
            'statusCode': 400,
            'body': json.dumps({'message': 'Wakarimasen! - mensaje no reconocido'})
        }

    # Esta porción se ejecuta sólo cuando se requiere una nueva subscripción como webhook
    logger.info(f"llmbot - Parámetros: {event['queryStringParameters']}")
    if is_meta_verification(event):
        return {
            "statusCode": 200,
            "body": event['queryStringParameters']['hub.challenge'],
            "isBase64Encoded": 0
        }
    
    wa_message = get_whatsapp_message(event) 
    sqs_client.send_message(
        QueueUrl = LLMBOT_SQS_URL,
        MessageBody = json.dumps(wa_message),
        MessageGroupId = wa_message['mensaje_id'],
        MessageDeduplicationId = wa_message['telefono_destino'])
    logger.info(f'llmbot - Mensaje {wa_message} recibido y procesado')
    
    return  {
    'statusCode': 200,
    'body': 'Mensaje recibido y procesado'
    }

    logger.warning(f'llmbot - Algo no esta bien con el mensaje {wa_message}')
    return  {
        'statusCode': 400,
        'body': 'Algo no esta bien con el mensaje {wa_message}'
    }
