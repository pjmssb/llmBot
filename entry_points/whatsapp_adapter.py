#ESTE ES EL ADAPTADOR PRIMARIO PARA WHATSAPP
from flask import Flask, jsonify, request
app = Flask(__name__)
#CUANDO RECIBAMOS LAS PETICIONES EN ESTA RUTA
@app.route("/whatsapp/", methods=["POST", "GET"])
def webhook_whatsapp():
    #Me sentiría más cómodo con un POST
    if request.method == "GET":
        #SI EL TOKEN ES IGUAL AL QUE RECIBIMOS
        if request.args.get('hub.verify_token') == "HolaNovato":
            #ESCRIBIMOS EN EL NAVEGADOR EL VALOR DEL RETO RECIBIDO DESDE FACEBOOK
            return request.args.get('hub.challenge')
        else:
            #SI NO SON IGUALES RETORNAMOS UN MENSAJE DE ERROR
          return "Error de autentificacion."
    #RECIBIMOS TODOS LOS DATOS ENVIADO VIA JSON
    data=request.get_json()
    #EXTRAEMOS DATOS RELEVANTES
    telefonoCliente=data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    mensaje=data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    idWA=data['entry'][0]['changes'][0]['value']['messages'][0]['id']
    timestamp=data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
    #ESCRIBIMOS EL NUMERO DE TELEFONO Y EL MENSAJE EN EL ARCHIVO TEXTO
    #SI HAY UN MENSAJE
    #AQUI LLAMAMOS AL MODELO PARA UNA NUEVA INTERACCIÓN EN LA CONVERSACIÓN
    if mensaje is not None:
      f = open("texto.txt", "w")
      f.write(mensaje)
      f.close()
      #RETORNAMOS EL STATUS EN UN JSON
      return jsonify({"status": "success"}, 200)


if __name__ == "__main__":
  from dotenv import load_dotenv, find_dotenv
  import os
  _ = load_dotenv(find_dotenv()) # read local .env file
  print(os.environ['WHATSAPP_TOKEN'])
  app.run(debug=False)