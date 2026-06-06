from flask import Flask, request
import requests
import json

app = Flask(__name__)

# --- CONFIGURACIÓN CRUCIAL QUE DEBES LLENAR ---
ACCESS_TOKEN = "EAAXvYJIdng8BRscKZCWmgQLczjVZA5jW7ZAbYHH4N2MOWR0Q5TO5aC13bZCjqD72X5YYS7mcoCqYuCFZA2ZCZBCF8guxKwlG88JEnAwJ6LEnWl89oGo7ec7gzAZAuUi6keE2OWybLf1amzGcFd19mzrOOXHdrd7BHSLcq8d5sDsqUXVjdNFVOt1379WX8TxpQXis1sIMYoCZAbckwVsu5xVZBvKdNVMZCEMg3311WeNb1wdqi0BLCdzxZAm5kZCbrgM2gXZAP5yjueoZCzOZBnycWt7U4Du3Fd50"
PHONE_NUMBER_ID = "1108364832363382"
VERIFICATION_TOKEN = "26CF22d2"

# --- MEMORIA DEL ROBOT ---
# Aquí guardaremos en qué paso va cada cliente y sus datos.
# (En el futuro, cuando sea oficial, esto se guarda en una base de datos real).
clientes = {}

@app.route('/webhook', methods=['GET'])
def verificar_webhook():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
            return "Falló la verificación del token", 403
        return request.args.get("hub.challenge")
    return "Webbhook funcionando", 200

@app.route('/webhook', methods=['POST'])
def recibir_mensaje():
    try:
        body = request.json
        # Extraemos el número y el mensaje del cliente
        mensaje_recibido = body['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        telefono_cliente = body['entry'][0]['changes'][0]['value']['messages'][0]['from']
        
        # Convertimos el mensaje a minúsculas para entenderlo más fácil
        mensaje_limpio = mensaje_recibido.lower().strip()

        # Si el cliente es nuevo, lo registramos en el paso 1
        if telefono_cliente not in clientes:
            clientes[telefono_cliente] = {"paso": 1, "nombre": ""}

        paso_actual = clientes[telefono_cliente]["paso"]
        respuesta = ""

        # ==========================================
        # 🌳 ÁRBOL DE DECISIÓN DE INSOLVENCIA 🌳
        # ==========================================

        if paso_actual == 1:
            respuesta = "¡Hola! Entendemos lo agobiante que puede ser estar sobreendeudado, pero respira, estás en el lugar indicado. La Ley de Insolvencia es tu derecho y estamos aquí para ayudarte a recuperar tu tranquilidad financiera. 🤝\n\nPara empezar a asesorarte, ¿cuál es tu nombre?"
            clientes[telefono_cliente]["paso"] = 2

        elif paso_actual == 2:
            nombre = mensaje_recibido # Guardamos el nombre tal como lo escribió
            clientes[telefono_cliente]["nombre"] = nombre
            respuesta = f"Mucho gusto, {nombre}. Para analizar tu caso y saber si aplicas a los beneficios de la ley, ¿de cuánto es aproximadamente la suma total de TODAS tus deudas (bancos, tarjetas, terceros)?"
            clientes[telefono_cliente]["paso"] = 3

        elif paso_actual == 3:
            respuesta = "Entendido. Es una situación que podemos manejar. Ahora, una pregunta clave para definir nuestra estrategia legal:\n\n¿Actualmente tienes bienes a tu nombre sujetos a registro (como casas, apartamentos, lotes o vehículos)?\n\n👉 Responde *SÍ* o *NO*."
            clientes[telefono_cliente]["paso"] = 4

        elif paso_actual == 4:
            # Evaluamos si dijo que SÍ o que NO tiene bienes
            if "no" in mensaje_limpio and "si" not in mensaje_limpio and "sí" not in mensaje_limpio:
                respuesta = "¡Excelentes noticias! Al no tener bienes a tu nombre, el proceso es mucho más ágil. Te llevaremos a un escenario donde protegeremos tu mínimo vital y solucionaremos el problema de raíz.\n\n⚖️ Nuestra propuesta de honorarios es totalmente transparente: Cobramos el *10% + IVA* sobre el total de las deudas líquidas, pagadero en cuotas mensuales cómodas.\n\nUn abogado experto te contactará mañana para iniciar tu trámite. ¿A qué hora prefieres que te llamemos?"
                clientes[telefono_cliente]["paso"] = 6
                
            elif "si" in mensaje_limpio or "sí" in mensaje_limpio:
                respuesta = "Comprendo. Nuestro objetivo principal será *proteger tu patrimonio*.\n\nPara saber si podemos hacer acuerdos bilaterales y salvar tus bienes, ¿esos inmuebles o vehículos tienen alguna garantía (como Hipoteca o Prenda)?\n\n👉 Responde *SÍ* o *NO*."
                clientes[telefono_cliente]["paso"] = 5
                
            else:
                respuesta = "Por favor, para poder darte la estrategia correcta, responde únicamente *SÍ* o *NO*.\n¿Tienes bienes a tu nombre (casas, carros, etc.)?"

        elif paso_actual == 5:
            if "si" in mensaje_limpio or "sí" in mensaje_limpio:
                respuesta = "¡Perfecto! Esa es una gran ventaja. Nuestra estrategia será hacer acuerdos directos con los acreedores para CONSERVAR tus bienes, y al resto de las deudas llevarlas a otro escenario legal.\n\n⚖️ Tus honorarios con nosotros serían así:\n- *5% + IVA* de los créditos renegociados (los que salvan tus bienes).\n- *10% + IVA* de las demás deudas líquidas.\n(Todo pagadero en cómodas cuotas mensuales).\n\nNuestro abogado especialista te llamará mañana para diseñar el plan de rescate. ¿A qué hora te viene bien la llamada?"
                clientes[telefono_cliente]["paso"] = 6
                
            elif "no" in mensaje_limpio:
                respuesta = "Entendido. Al tener bienes libres, tu caso requiere un blindaje especial para evitar riesgos de pérdida de patrimonio.\n\nMañana mismo uno de nuestros abogados senior revisará tu situación exacta para darte la estrategia legal a seguir y explicarte nuestros honorarios (que se pueden pagar a cuotas).\n\n¿A qué hora podemos llamarte?"
                clientes[telefono_cliente]["paso"] = 6
                
            else:
                respuesta = "Por favor, responde únicamente *SÍ* o *NO*.\n¿Tus bienes tienen alguna hipoteca o prenda?"

        elif paso_actual == 6:
            # Aquí ya nos da su horario y terminamos el flujo
            nombre_cliente = clientes[telefono_cliente]["nombre"]
            respuesta = f"¡Todo listo, {nombre_cliente}! 🎉\n\nTu caso ha sido registrado y hemos anotado tu horario de preferencia. Un asesor de nuestro equipo legal se comunicará contigo desde nuestra línea principal.\n\n¡Que tengas una excelente noche, descansa que nosotros nos encargamos del resto!"
            clientes[telefono_cliente]["paso"] = 7 # Lo pasamos a un paso final

        elif paso_actual == 7:
            # Si el cliente sigue escribiendo después de terminar
            if "reiniciar" in mensaje_limpio:
                clientes[telefono_cliente]["paso"] = 1
                respuesta = "Hemos reiniciado el sistema. Escribe cualquier palabra para comenzar de nuevo."
                del clientes[telefono_cliente] # Borramos su memoria para empezar de cero
            else:
                respuesta = "Tu caso ya está en manos de nuestros expertos. Pronto nos comunicaremos contigo. 🤝\n*(Si deseas iniciar una nueva consulta desde cero, escribe la palabra REINICIAR)*."

        # ==========================================

        print(f"El cliente {telefono_cliente} está en el paso {paso_actual} y se le responderá algo.")

        # Enviamos la respuesta a WhatsApp
        enviar_respuesta_api(telefono_cliente, respuesta)

        return "OK", 200
    except Exception as e:
        print(f"Error procesando mensaje: {e}")
        return "OK", 200 

def enviar_respuesta_api(telefono, mensaje_respuesta):
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
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Error enviando mensaje a Meta: {e}")

if __name__ == '__main__':
    app.run(port=5000)

if __name__ == '__main__':
    app.run(port=5000)
