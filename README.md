# EduFit - Aplicación Educativa de Matemáticas

Una aplicación Streamlit que replica la interfaz de EduFit para enseñar fracciones de manera interactiva.

## Características

- **Selección de temas**: Elige entre 6 temas divertidos (Autos, Cocina, Música, Fútbol, Espacio, Animales)
- **Explicaciones dinámicas**: Contenido generado por GPT adaptado al tema seleccionado
- **Ejercicios interactivos**: Problemas de suma de fracciones con feedback inmediato
- **Inputs flexibles**: Acepta respuestas en formato de fracción (ej: "1/4") o números enteros
- **Sistema de calificación**: Escala del 0-10 para medir comprensión
- **Feedback educativo**: Explicaciones detalladas para respuestas correctas e incorrectas

## Configuración

1. **Configura tu API key de OpenAI**:
   - Abre el archivo `secrets.py`
   - Reemplaza `"tu-api-key-aqui"` con tu API key real de OpenAI
   ```python
   OPENAI_API_KEY = "sk-tu-api-key-real-aqui"
\`\`\`

2. **Instala las dependencias**:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. **Ejecuta la aplicación**:
\`\`\`bash
streamlit run app.py
\`\`\`

## Estructura de la Aplicación

- **Selección de Tema**: Elige el contexto para los ejercicios
- **Pantalla de Bienvenida**: Saludo personalizado y explicación de fracciones
- **Pantalla de Ejercicios**: Problemas adaptativos con feedback inteligente
- **Pantalla de Finalización**: Resumen de aprendizaje y evaluación

## Seguridad

- El archivo `secrets.py` contiene información sensible y está excluido del control de versiones
- Nunca subas tu API key a repositorios públicos
- Asegúrate de configurar tu propia API key antes de usar la aplicación

## Tecnologías

- **Streamlit**: Framework de la interfaz web
- **OpenAI GPT**: Generación de contenido educativo dinámico
- **Python**: Lógica de la aplicación y procesamiento de fracciones
</markdown>
