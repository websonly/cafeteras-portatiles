import os
import re
import time
import datetime
import json
import openai
from openai.error import RateLimitError, APIError

# Número de posts a generar
NUM_POSTS = 2
# Longitud aproximada de cada post
WORDS_PER_POST = 200
# Tu código de afiliado
ASSOCIATE_TAG = "websonly-21"
# Dominio de tu sitio
DOMAIN = "cafeterasportatiles.online"
# Reintentos y backoff
RETRIES = 3
BACKOFF = 2

# Clave API de OpenAI (asegúrate de definir CHATGPT_API_KEY en tu entorno)
openai.api_key = os.getenv("CHATGPT_API_KEY")

def affiliateify(content: str) -> str:
    """
    Añade tu etiqueta de afiliado a todos los enlaces de Amazon.es
    que encuentre en el contenido.
    """
    pattern = r"(https://www\\.amazon\\.es/dp/([A-Z0-9]{10}))"
    return re.sub(pattern, lambda m: f"{m.group(1)}/?tag={ASSOCIATE_TAG}", content)

def generate_post(prompt: str) -> str:
    """
    Llama a la API de ChatGPT para generar un post según el prompt.
    Reintenta en caso de RateLimitError.
    """
    for i in range(RETRIES):
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente experto en redacción de artículos de blog."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            return resp.choices[0].message.content
        except RateLimitError:
            time.sleep(BACKOFF ** (i + 1))
        except APIError:
            break
    # Si falla la API, devolvemos un placeholder
    return f"# Artículo provisional sobre {DOMAIN}\n\nContenido en breve."

if __name__ == "__main__":
    # Asegurarnos de que existe la carpeta posts/
    os.makedirs("posts", exist_ok=True)

    # (Opcional) Cargar lista de productos reales desde data/products.json
    products_list = ""
    if os.path.exists("data/products.json"):
        with open("data/products.json", encoding="utf-8") as pf:
            products = json.load(pf)
        products_list = "\n\nModelos a comparar:\n" + "\n".join(
            f"- [{p['name']}](https://www.amazon.es/dp/{p['asin']}/?tag={ASSOCIATE_TAG})"
            for p in products
        )

    for i in range(1, NUM_POSTS + 1):
        # Construir el prompt con f-string
        prompt = (
            f"Genera un artículo de aproximadamente {WORDS_PER_POST} palabras "
            f"sobre \"{DOMAIN}\". "
            "Incluye una introducción, subtítulos claros para cada sección, "
            "y ejemplos de enlaces a productos de Amazon con tu código de afiliado."
            "\n\nEstructura sugerida:\n"
            "1. Introducción al tema.\n"
            "2. Pros y contras.\n"
            "3. Conclusión y recomendación.\n"
            f"{products_list}"
        )

        # Generar el texto completo
        raw = generate_post(prompt)

        # Extraer título y fecha, añadir frontmatter YAML
        lines = raw.split("\n")
        title = lines[0].lstrip("# ").strip()  # si GPT comienza con "# Título"
        date = datetime.date.today().isoformat()
        frontmatter = f"---\ntitle: {title}\ndate: {date}\n---\n\n"

        # Concatenar frontmatter + contenido bruto
        content = frontmatter + raw

        # Aplicar tu afiliado a los enlaces
        content = affiliateify(content)

        # Guardar en posts/post_{i}.md
        filename = f"posts/post_{i}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✔ Generado {filename}")
