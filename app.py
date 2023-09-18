from flask import Flask, request, render_template
import sett
import services

app = Flask(__name__)

@app.route('/bienvenido', methods=['GET'])
def  bienvenido():
    return 'Hola mundo bigdateros, desde Flask'

@app.route('/privacidad')
def privacidad():
    # Renderiza la plantilla de privacidad
    text = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Política de Privacidad</title>
</head>
<body>
    <h1>Política de Privacidad</h1>

    <p>En [Nombre de tu sitio web], nos comprometemos a proteger tu privacidad y tus datos personales. A continuación, te explicamos cómo recopilamos, utilizamos y protegemos tu información:</p>

    <h2>Información que Recopilamos</h2>

    <p>Recopilamos información personal que nos proporcionas voluntariamente, como tu nombre, dirección de correo electrónico y otra información de contacto cuando te registras en nuestro sitio o interactúas con nuestros servicios.</p>

    <h2>Uso de la Información</h2>

    <p>Utilizamos la información que recopilamos para proporcionarte nuestros servicios, mejorar tu experiencia en nuestro sitio y cumplir con nuestras obligaciones legales. Esto puede incluir el envío de correos electrónicos de servicio, la personalización de contenido y la realización de análisis para mejorar nuestros servicios.</p>

    <h2>Compartir Información</h2>

    <p>No compartimos tu información personal con terceros sin tu consentimiento, excepto cuando sea necesario para proporcionar nuestros servicios o cumplir con la ley.</p>

    <h2>Seguridad de Datos</h2>

    <p>Tomamos medidas de seguridad para proteger tu información personal contra el acceso no autorizado o la divulgación. Sin embargo, ninguna medida de seguridad en línea es completamente infalible.</p>

    <h2>Cookies y Tecnologías Similares</h2>

    <p>Utilizamos cookies y tecnologías similares para mejorar la funcionalidad de nuestro sitio web y recopilar información sobre cómo los usuarios interactúan con él. Puedes gestionar tus preferencias de cookies a través de la configuración de tu navegador.</p>

    <h2>Cambios en esta Política</h2>

    <p>Podemos actualizar esta Política de Privacidad en el futuro. Te recomendamos revisarla periódicamente para estar al tanto de cualquier cambio. Al continuar utilizando nuestro sitio, aceptas los términos de esta Política.</p>

    <p>Si tienes alguna pregunta o inquietud sobre nuestra Política de Privacidad, no dudes en <a href="contacto.html">contactarnos</a>.</p>

    <p>Última actualización: [Fecha de la última actualización]</p>
</body>
</html>

    """
    
    return text #render_template('privacidad.html')

@app.route('/webhook', methods=['GET'])
def verificar_token():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        print(request.args)


        if token == sett.token and challenge != None:
            return challenge
        else:
            return 'token incorrecto', 403
    except Exception as e:
        return e,403
    
@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    #print(request.get_json())
    try:
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = services.replace_start(message['from'])
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.obtener_Mensaje_whatsapp(message)

        services.administrar_chatbot(text, number,messageId,name)
        return 'enviado'

    except Exception as e:
        return 'no enviado ' + str(e)

if __name__ == '__main__':
    app.run()
