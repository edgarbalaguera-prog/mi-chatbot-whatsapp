# Esto es un chatbot muy simple que solo dice "OK" a Meta
from flask import Flask, request

app = Flask(__name__)

# Esta parte es el "saludo secreto" (el Token de Verificación)
TOKEN_VERIFICACION_SECRETO = "26CF22d2"

@app.route('/webhook', methods=['GET'])
def verificar_webhook():
    """Esta función le dice a Meta: '¡Hola! Soy yo'"""
    # Meta envía un "reto" (challenge) y nosotros lo devolvemos
    print("Verificando webhook con Meta...")
    return request.args.get("hub.challenge")

@app.route('/webhook', methods=['POST'])
def recibir_mensaje():
    """Esta función es donde llegarán los mensajes de los clientes"""
    print("¡Llegó un mensaje de un cliente!")
    # Aquí es donde programarías la respuesta real más adelante
    return "OK", 200

if __name__ == '__main__':
    # Esto inicia nuestro servidor en internet
    app.run(port=5000, host='0.0.0.0')
