import json
import logging
import heyoo

logger = logging.getLogger()
logger.setLevel(logging.INFO)
LLM_META_VERIFICATION = '3st4C4d3n4L4C4mb13D3spu3sD3Suscr1b1rm3?'


def lambda_handler(event, context): 
    logger.info("llmbot - Message arrived")
    
    user_agent = event['headers']['User-Agent'][0:8]
    
    if user_agent != 'facebook':
        logger.info('El evento no tiene formato de Meta %s',json.dumps(event))
        return  {
            'statusCode': 400,
            'body': json.dumps({'message': 'Ceci n`est pas un message WhatsApp'})
        }

    # Esta porción se ejecuta sólo cuando se requiere una nueva subscripción como webhook
    logger.info(f"llmbot - Parámetros: {event['queryStringParameters']}")
    if event['queryStringParameters'] != None:
        if event['queryStringParameters']['hub.mode'] == 'subscribe' and event['queryStringParameters']['hub.verify_token'] == LLM_META_VERIFICATION:
            hub_challenge = event['queryStringParameters']['hub.challenge']
            return {
                "statusCode": 200,
                "body": hub_challenge,
                "isBase64Encoded": 0
            }
    
    #Esta porción procesa el mensaje recibido
    mensaje = json.loads(event['body'])['entry'];
    if mensaje != None:
        logger.info(f"llmbot - Mensaje: {mensaje}")
        mensaje_id = mensaje[0]['changes'][0]['value']['messages'][0]['id']
        mensaje_telefono = mensaje[0]['changes'][0]['value']['messages'][0]['from']
        mensaje_nombre = mensaje[0]['changes'][0]['value']['contacts'][0]['profile']['name'] 
        mensaje_datos = mensaje[0]['changes'][0]['value']['messages'][0]['text']['body'] 
        logger.info(f'llmbot - Llego el mensaje {mensaje_id} \ndesde el teléfono {mensaje_telefono} \nde {mensaje_nombre}  \ndiciendo: {mensaje_datos}')
    

    return  {
        'statusCode': 400,
        'body': 'Algo no esta bien'
    }
