import json
import logging
import boto3

#  Para depuración
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#  Este token utilizado sólo cuando se valida el webhook
META_VERIFICATION_TOKEN = "Este no es el token de verificación"
LLMBOT_SQS_URL = "https://sqs.us-east-1.amazonaws.com/337340005201/sqs_llmbot.fifo"

#  Recursos AWS
sqs_client = boto3.client('sqs')

def is_meta_verification(event):
    qs_params = event.get('queryStringParameters', {})
    if qs_params is None: 
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
    message['timestamp'] = data[0]['changes'][0]['value']['messages'][0]['timestamp']
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

    #  Esta porción se ejecuta sólo cuando se requiere una nueva subscripción como webhook
    logger.info("llmbot - Parámetros: %s", event['queryStringParameters'])
    if is_meta_verification(event):
        return {
            "statusCode": 200,
            "body": event['queryStringParameters']['hub.challenge'],
            "isBase64Encoded": 0
        }
    
    #  Aquí se procesa los mensajes de los clientes
    wa_message = get_whatsapp_message(event) 

    if wa_message == '{}':
        logger.warning('llmbot - Algo no esta bien con el mensaje %s',wa_message)
        return  {
            'statusCode': 400,
            'body': 'Algo no esta bien con el mensaje {wa_message}'
        }
    
    sqs_client.send_message(
        QueueUrl=LLMBOT_SQS_URL,
        MessageBody=json.dumps(wa_message, ensure_ascii=False),
        MessageGroupId=wa_message['telefono_destino'],
        MessageDeduplicationId=wa_message['mensaje_id'])
    logger.info('llmbot - Mensaje %s recibido y procesado',wa_message)
    
    return  {
    'statusCode': 200,
    'body': 'Mensaje recibido y procesado'
    }

