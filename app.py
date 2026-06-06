from flask import Flask, request
import requests
import json

app = Flask(__name__)

# --- CONFIGURACIÓN CRUCIAL QUE DEBES LLENAR ---
# 1. Tu Token de acceso de Meta (temporal o permanente)
ACCESS_TOKEN = "EAAXvYJIdng8BRscKZCWmgQLczjVZA5jW7ZAbYHH4N2MOWR0Q5TO5aC13bZCjqD72X5YYS7mcoCqYuCFZA2ZCZBCF8guxKwlG88JEnAwJ6LEnWl89oGo7ec7gzAZAuUi6keE2OWybLf1amzGcFd19mzrOOXHdrd7BHSLcq8d5sDsqUXVjdNFVOt1379WX8TxpQXis1sIMYoCZAbckwVsu5xVZBvKdNVMZCEMg3311WeNb1wdqi0BLCdzxZAm5kZCbrgM2gXZAP5yjueoZCzOZBnycWt7U4Du3Fd50"
# 2. El ID de tu número de teléfono de WhatsApp en Meta
PHONE_NUMBER_ID = "1108364832363382"
# 3. Tu Token de verificación (el de 'image_5.png')
VERIFICATION_TOKEN = "26CF22d2" 

@app.route('/webhook', methods=['GET'])
def verificar_webhook():
    """Lógica de verificación para Meta"""
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
            return "Falló la verificación del token", 403
        return request.args.get("hub.challenge")
    return "Webbhook funcionando", 200

@app.route('/webhook', methods=['POST'])
def recibir_mensaje():
    """Lógica para recibir y responder mensajes"""
    try:
        body = request.json
        print("¡Paquete de datos recibido de WhatsApp!")
        # print(json.dumps(body, indent=2)) # Descomenta para ver todo el paquete en los logs de Render

        # Intentamos extraer el mensaje de texto y el número del cliente
        mensaje_recibido = body['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        telefono_cliente = body['entry'][0]['changes'][0]['value']['messages'][0]['from']

        print(f"El cliente {telefono_cliente} dijo: {mensaje_recibido}")

        # --- AQUÍ DEFINES LA RESPUESTA ---
        # Puedes personalizar este mensaje como quieras
        respuesta = f"Hola 👋, recibimos tu mensaje: '{mensaje_recibido}'. En breve te atenderemos."

        # Llamamos a la función que envía el mensaje de vuelta a Meta
        enviar_respuesta_api(telefono_cliente, respuesta)

        return "OK", 200
    except Exception as e:
        # Esto ocurre si el mensaje no es de texto (por ejemplo, una imagen)
        # Por ahora, simplemente ignoramos esos mensajes para no dar error
        print(f"Error procesando mensaje (probablemente no sea texto): {e}")
        return "OK", 200 

def enviar_respuesta_api(telefono, mensaje_respuesta):
    """Lógica para llamar a la API de Meta para enviar mensajes"""
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": telefono,
        "type": "text",
        "text": {
            "body": mensaje_respuesta
        }
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status() # Lanza error si la API responde mal
        print("✅ Mensaje de respuesta enviado correctamente a Meta.")
    except Exception as e:
        print(f"❌ Error enviando mensaje a Meta: {e}")
        print(f"Detalles del error: {response.text if 'response' in locals() else 'No hay respuesta'}")

if __name__ == '__main__':
    app.run(port=5000)
