import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Wedge
import random
from fractions import Fraction
import re

from gpt_logic import (
    generar_explicacion_teorica, 
    generar_explicacion_aplicada, 
    adaptar_ejercicio_a_tema, 
    explicar_error,
    base_ejercicios
)

# Configuración de la página
st.set_page_config(
    page_title="EduFit - Matemáticas",
    page_icon="📚",
    layout="wide"
)

# CSS personalizado para replicar el estilo
st.markdown("""
<style>
    .main-header {
        background-color: #4A90E2;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .exercise-card {
        background-color: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
    }
    
    .correct-answer {
        background-color: #d4edda;
        border: 2px solid #c3e6cb;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .incorrect-answer {
        background-color: #f8d7da;
        border: 2px solid #f5c6cb;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .fraction {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin: 0 1rem;
    }
    
    .fraction-line {
        border-top: 3px solid black;
        margin: 0.2rem 0;
    }
    
    .big-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .rating-buttons {
        display: flex;
        gap: 0.5rem;
        margin: 1rem 0;
    }
    
    .rating-button {
        width: 40px;
        height: 40px;
        border-radius: 5px;
        border: none;
        color: white;
        font-weight: bold;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar estado de la sesión
if 'screen' not in st.session_state:
    st.session_state.screen = 'topic_selection'  # cambiar pantalla inicial a selección de temas
if 'selected_topic' not in st.session_state:  # agregar estado para tema seleccionado
    st.session_state.selected_topic = None
if 'current_question' not in st.session_state:
    st.session_state.current_question = 1
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'show_feedback' not in st.session_state:
    st.session_state.show_feedback = False
if 'current_exercises' not in st.session_state:
    st.session_state.current_exercises = []
if 'current_exercise_index' not in st.session_state:
    st.session_state.current_exercise_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'difficulty_level' not in st.session_state:
    st.session_state.difficulty_level = "fácil"
if 'theoretical_explanation' not in st.session_state:
    st.session_state.theoretical_explanation = None
if 'applied_explanation' not in st.session_state:
    st.session_state.applied_explanation = None

def create_circle_fraction(numerator, denominator):
    """Crear un círculo dividido para mostrar fracciones"""
    fig, ax = plt.subplots(figsize=(4, 4))
    
    # Crear círculo base
    circle = plt.Circle((0, 0), 1, fill=False, color='black', linewidth=2)
    ax.add_patch(circle)
    
    # Dividir el círculo en secciones
    angle_per_section = 360 / denominator
    for i in range(denominator):
        angle = i * angle_per_section
        x = np.cos(np.radians(angle))
        y = np.sin(np.radians(angle))
        ax.plot([0, x], [0, y], 'black', linewidth=1)
    
    # Sombrear las secciones correspondientes al numerador
    for i in range(numerator):
        angle_start = i * angle_per_section - 90  # -90 para empezar desde arriba
        angle_end = (i + 1) * angle_per_section - 90
        wedge = Wedge((0, 0), 1, angle_start, angle_end, 
                     facecolor='lightblue', alpha=0.7)
        ax.add_patch(wedge)
    
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')
    
    return fig

def show_header():
    """Mostrar el header de la aplicación"""
    st.markdown("""
    <div class="main-header">
        <div style="font-size: 1.5rem; font-weight: bold;">EduFit</div>
        <div>Aula en vivo matemática | Fracciones</div>
        <div style="font-size: 1.5rem;">✕</div>
    </div>
    """, unsafe_allow_html=True)

def show_topic_selection_screen():
    """Pantalla de selección de temas"""
    show_header()
    
    st.markdown('<div class="big-title">¡Hola María!</div>', unsafe_allow_html=True)
    
    st.markdown("### ¿Qué tema te divierte más hoy?")
    
    # Crear cuadrícula de temas con emojis
    topics = [
        {"name": "Autos", "emoji": "🚗", "key": "autos"},
        {"name": "Cocina", "emoji": "🎂", "key": "cocina"},
        {"name": "Música", "emoji": "🎹", "key": "musica"},
        {"name": "Fútbol", "emoji": "⚽", "key": "futbol"},
        {"name": "Espacio", "emoji": "🚀", "key": "espacio"},
        {"name": "Animales", "emoji": "🐻", "key": "animales"}
    ]
    
    # Crear tarjetas en cuadrícula 2x3
    for row in range(2):
        cols = st.columns(3)
        for col_idx in range(3):
            topic_idx = row * 3 + col_idx
            if topic_idx < len(topics):
                topic = topics[topic_idx]
                with cols[col_idx]:
                    # Crear tarjeta clickeable
                    if st.button(
                        f"{topic['emoji']}\n\n**{topic['name']}**",
                        key=f"topic_{topic['key']}",
                        use_container_width=True,
                        help=f"Seleccionar tema: {topic['name']}"
                    ):
                        st.session_state.selected_topic = topic['name']
                        with st.spinner("Generando explicaciones personalizadas..."):
                            st.session_state.theoretical_explanation = generar_explicacion_teorica()
                            st.session_state.applied_explanation = generar_explicacion_aplicada(topic['name'].lower())
                            st.session_state.current_exercises = generate_dynamic_exercises(topic['name'])
                        st.session_state.screen = 'welcome'
                        st.rerun()

    # Agregar CSS para las tarjetas de temas
    st.markdown("""
    <style>
        div[data-testid="column"] button {
            height: 150px !important;
            font-size: 1.2rem !important;
            background-color: #f8f9fa !important;
            border: 2px solid #e9ecef !important;
            border-radius: 15px !important;
            margin: 0.5rem 0 !important;
        }
        
        div[data-testid="column"] button:hover {
            background-color: #e9ecef !important;
            border-color: #4A90E2 !important;
        }
    </style>
    """, unsafe_allow_html=True)

def show_welcome_screen():
    """Pantalla de bienvenida"""
    show_header()
    
    topic_text = f" sobre {st.session_state.selected_topic}" if st.session_state.selected_topic else ""
    st.markdown('<div class="big-title">¡Hola María!</div>', unsafe_allow_html=True)
    
    if st.session_state.theoretical_explanation:
        st.markdown(f"**Explicación teórica:**")
        st.markdown(st.session_state.theoretical_explanation)
        
        st.markdown(f"**Aplicado al tema {st.session_state.selected_topic}:**")
        st.markdown(st.session_state.applied_explanation)
    else:
        st.markdown(f"""
        La actividad de hoy va a ser sobre **fracciones**{topic_text}.
        
        Las fracciones son una manera de mostrar partes de algo. Por ejemplo, si cortamos una torta en 4 
        pedazos iguales y nos comemos 1, comimos 1/4 de la torta. En esta actividad, vamos a aprender a sumar 
        fracciones. Algunas van a tener el mismo número abajo (denominador) y otras no.
        """)

    st.markdown("### Repasemos un poco:")
    
    # Crear el círculo de fracciones
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig = create_circle_fraction(0, 5)
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.markdown("""
        <div style="background-color: #f0f0f0; padding: 1rem; border-radius: 10px; margin-top: 2rem;">
        ¡Pinta los triángulos que quieras, y mirá como cambia la fracción!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="fraction">
            <div>0</div>
            <div class="fraction-line"></div>
            <div>5</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Estoy listo para empezar", key="start", use_container_width=True):
            st.session_state.screen = 'exercise'
            st.rerun()
    
    with col2:
        if st.button("¿Me explicás denuevo?", key="explain", use_container_width=True):
            st.info("¡Perfecto! Las fracciones representan partes de un todo. El número de arriba (numerador) indica cuántas partes tomamos, y el de abajo (denominador) en cuántas partes dividimos el total.")

def show_exercise_screen():
    """Pantalla de ejercicios"""
    show_header()
    
    if not st.session_state.current_exercises:
        st.error("No se pudieron generar ejercicios. Por favor, selecciona un tema nuevamente.")
        if st.button("Volver a selección de temas"):
            st.session_state.screen = 'topic_selection'
            st.rerun()
        return
    
    current_ex_idx = st.session_state.current_exercise_index
    if current_ex_idx >= len(st.session_state.current_exercises):
        st.session_state.screen = 'completion'
        st.rerun()
        return
    
    current_exercise = st.session_state.current_exercises[current_ex_idx]
    
    st.markdown(f'<div class="big-title">Pregunta {current_ex_idx + 1}</div>', unsafe_allow_html=True)
    
    st.markdown(current_exercise['question'])
    
    user_answer = st.text_input(
        "Tu respuesta (puedes escribir fracciones como 1/4 o números enteros como 3):",
        key=f"answer_{current_ex_idx}",
        placeholder="Ejemplo: 1/2, 3/4, 2, etc."
    )
    
    if st.session_state.show_feedback:
        correct_answer = current_exercise['correct_answer']
        
        if user_answer:
            user_fraction = parse_fraction_input(user_answer)
            correct_fraction = parse_fraction_input(correct_answer)
            
            if user_fraction and correct_fraction and user_fraction == correct_fraction:
                st.markdown("""
                <div class="correct-answer">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <div style="background-color: green; color: white; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem;">✓</div>
                        <div>
                            <strong>¡Bien!</strong><br>
                            Tu respuesta es <strong>correcta</strong>.
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="incorrect-answer">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <div style="background-color: red; color: white; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem;">✕</div>
                        <div>
                            <strong>Repasemos un poco:</strong><br>
                """, unsafe_allow_html=True)
                
                if user_answer:
                    with st.spinner("Generando explicación..."):
                        error_explanation = explicar_error(
                            current_exercise['question'], 
                            correct_answer, 
                            user_answer
                        )
                    st.markdown(error_explanation)
                else:
                    st.markdown(f"La respuesta correcta es: {correct_answer}")
                
                st.markdown("""
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Botones de acción
    col1, col2 = st.columns(2)
    
    with col1:
        if not st.session_state.show_feedback:
            if st.button("Revisar respuesta", key="check", use_container_width=True):
                st.session_state.show_feedback = True
                st.rerun()
        else:
            if st.button("Siguiente pregunta", key="next", use_container_width=True):
                st.session_state.current_exercise_index += 1
                st.session_state.show_feedback = False
                st.rerun()
    
    with col2:
        if st.button("No entiendo", key="help", use_container_width=True):
            st.info("¡No te preocupes! Para sumar fracciones con el mismo denominador, solo sumas los numeradores (números de arriba) y mantienes el mismo denominador (número de abajo).")

def show_completion_screen():
    """Pantalla de finalización"""
    show_header()
    
    st.markdown('<div class="big-title">¡Terminaste!</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Buen trabajo, ya terminaste la actividad de hoy. Vamos a repasar las cosas que aprendiste:
    
    • Sumar fracciones con el mismo denominador
    • Sumar fracciones con denominador distinto
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### Del 1 al 10, ¿qué tan bien sentiste que entendiste los temas que viste hoy?")
    
    st.markdown('<div style="margin: 1rem 0;"><span style="margin-right: 2rem;">No entendí nada</span><span style="float: right;">Entendí todo</span></div>', unsafe_allow_html=True)
    
    # Crear botones de calificación
    rating_cols = st.columns(11)
    colors = ['#dc3545', '#dc3545', '#fd7e14', '#fd7e14', '#ffc107', '#ffc107', '#28a745', '#28a745', '#28a745', '#28a745', '#28a745']
    
    selected_rating = None
    for i, col in enumerate(rating_cols):
        with col:
            if st.button(str(i), key=f"rating_{i}", use_container_width=True):
                selected_rating = i
                st.session_state.rating = i
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### ¿Cuál de los temas sentís que fue el que más te costó?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Sumar fracciones con mismo denominador", key="topic1", use_container_width=True):
            st.session_state.difficult_topic = "mismo_denominador"
    
    with col2:
        if st.button("Sumar fracciones con distinto denominador", key="topic2", use_container_width=True):
            st.session_state.difficult_topic = "distinto_denominador"
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if st.button("Cerrar actividad", key="close", use_container_width=True):
        st.success("¡Gracias por completar la actividad! Has aprendido mucho sobre fracciones hoy.")
        if st.button("Reiniciar", key="restart"):
            # Limpiar todos los estados
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.screen = 'topic_selection'
            st.rerun()

def parse_fraction_input(input_str):
    """Parsear input de fracción como '1/4' o '3' y convertir a fracción"""
    input_str = input_str.strip()
    if '/' in input_str:
        try:
            return Fraction(input_str)
        except:
            return None
    else:
        try:
            return Fraction(int(input_str))
        except:
            return None

def generate_dynamic_exercises(topic, num_exercises=3):
    """Generar ejercicios adaptados al tema seleccionado"""
    exercises = []
    levels = ["fácil", "medio", "difícil"]
    
    for i in range(num_exercises):
        level = levels[min(i, len(levels)-1)]
        candidates = [e for e in base_ejercicios if e["nivel"] == level]
        base_exercise = random.choice(candidates)
        
        # Adaptar ejercicio al tema
        adapted_question = adaptar_ejercicio_a_tema(base_exercise, level, topic.lower())
        
        exercises.append({
            'question': adapted_question,
            'correct_answer': base_exercise['respuesta'],
            'level': level,
            'base_exercise': base_exercise
        })
    
    return exercises

# Lógica principal de navegación
def main():
    if st.session_state.screen == 'topic_selection':  # agregar nueva pantalla al flujo
        show_topic_selection_screen()
    elif st.session_state.screen == 'welcome':
        show_welcome_screen()
    elif st.session_state.screen == 'exercise':
        show_exercise_screen()
    elif st.session_state.screen == 'completion':
        show_completion_screen()

if __name__ == "__main__":
    main()
