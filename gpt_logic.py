from openai import OpenAI
import random
from api_key import OPENAI_API_KEY

base_ejercicios = [
    {"enunciado": "1/2 + 1/2", "respuesta": "1", "nivel": "fácil"},
    {"enunciado": "2/3 + 1/3", "respuesta": "1", "nivel": "fácil"},
    {"enunciado": "3/8 + 5/8", "respuesta": "1", "nivel": "medio"},
    {"enunciado": "2/5 + 3/10", "respuesta": "7/10", "nivel": "difícil"},
    {"enunciado": "5/6 + 2/9", "respuesta": "13/9", "nivel": "difícil"},
    {"enunciado": "1/4 + 1/4", "respuesta": "1/2", "nivel": "fácil"},
    {"enunciado": "3/5 + 1/10", "respuesta": "7/10", "nivel": "medio"},
    {"enunciado": "7/12 + 1/6", "respuesta": "3/4", "nivel": "medio"},
    {"enunciado": "5/8 + 3/16", "respuesta": "13/16", "nivel": "difícil"}
]

client = OpenAI(api_key=OPENAI_API_KEY)

# --- FUNCIÓN BASE GPT ---
def ask_gpt(messages, model="gpt-4"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.1
    )
    return response.choices[0].message.content.strip()

# --- FUNCIONES DE EXPLICACIÓN ---

def generar_explicacion_teorica():
    messages = [
        {"role": "system", "content": "Explicá la suma de fracciones con lenguaje simple para chicos de primaria. No uses frases como 'claro', 'por supuesto', 'ves', ni expresiones coloquiales. El estilo debe parecer un libro escolar."},
        {"role": "user", "content": "Explicá qué son la suma de fracciones."}
    ]
    return ask_gpt(messages)

def generar_explicacion_aplicada(tema):
    messages = [
        {"role": "system", "content": "Sos un profe explicando suma de fracciones de forma clara. Usá ejemplos del tema indicado. Estilo de libro escolar, sin expresiones coloquiales."},
        {"role": "user", "content": f"Explicá suma de fracciones usando ejemplos del tema: {tema}."}
    ]
    return ask_gpt(messages)

def adaptar_ejercicio_a_tema(ejercicio_base, nivel, tema):
    messages = [
        {"role": "system", "content": """
Sos un profe creativo que adapta ejercicios de fracciones a distintos temas (fútbol, espacio, cocina, etc.) para que sean más divertidos para los alumnos.

Reglas:
- El cálculo debe ser EXACTAMENTE el mismo que el ejercicio original (no cambies los números ni la operación).
- No cambies el nivel de dificultad.
- La salida debe ser SOLO el enunciado adaptado en una frase o dos, sin explicación ni texto extra.
- No incluyas la respuesta, solo la consigna.
- El estilo debe seguir los ejemplos dados.

Ejemplo 1:
Ejercicio original: "1/2 + 1/2"
Tema: Fútbol
Ejercicio adaptado: En un partido, un jugador corrió 1/2 de la cancha en la primera jugada y 1/2 en la segunda. ¿Cuánto corrió en total?

Ejemplo 2:
Ejercicio original: "7/12 + 1/6"
Tema: Espacio
Ejercicio adaptado: Una nave espacial gastó 7/12 de su combustible el día 1 y 1/6 el día 2. ¿Cuánto combustible gastó en total?

Ejemplo 3:
Ejercicio original: "5/8 + 3/16"
Tema: Animales
Ejercicio adaptado: En un área protegida, 5/8 de los animales son conejos y 3/16 ovejas. ¿Qué fracción de los animales son conejos u ovejas?
        """},
        {"role": "user", "content": f"Adaptá este ejercicio al tema {tema}:\nNivel de dificultad: {nivel}\nEjercicio original: {ejercicio_base['enunciado']}"}
    ]
    return ask_gpt(messages)

def explicar_error(pregunta, respuesta_correcta, respuesta_alumno):
    messages = [
        {"role": "system", "content": "Sos un profe que explica errores matemáticos a chicos. Sos un profe que explica errores matemáticos a chicos. Estilo simple y claro para alumnos de primaria. Solo das una breve explicación. No hacés ninguna pregunta, no nombrás al alumno, ni usás frases como 'el alumno respondió...'."},
        {"role": "user", "content": f"Soy un alumno de primaria. Respondí mal este ejercicio: '{pregunta}'. La respuesta correcta era: {respuesta_correcta}. Yo respondí: {respuesta_alumno}. Explicáme por qué está mal lo que hice yo y cómo resolverlo bien."}
    ]
    return ask_gpt(messages)

def get_tema_for_gpt(selected_topic):
    """Mapear el tema seleccionado en la UI al nombre que entiende GPT"""
    tema_mapping = {
        "Autos": "autos",
        "Cocina": "cocina", 
        "Música": "música",
        "Fútbol": "fútbol",
        "Espacio": "espacio",
        "Animales": "animales"
    }
    return tema_mapping.get(selected_topic, selected_topic.lower())
