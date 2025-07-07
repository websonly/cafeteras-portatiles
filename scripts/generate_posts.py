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

# Clave API de OpenAI
openai.api_key = os.getenv("CHATGPT_API_KEY")

def affiliateify(content: str) -> str:
    """
    Añade tu etiqueta de afiliado a todos los enlaces de Amazon.es.
    """
    pattern = r"(https://www\\.amazon\\.es/dp/([A-Z0-9]{10}))"
    return re.sub(pattern, lambda m: f"{m.group(1)}/?tag={ASSOCIATE_TAG}", content)

def generate_post(prompt: str) -> str:
    """
    Genera un post con la API de ChatGPT, con reintentos.
    """
    for attempt in range(RETRIES):
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
            time.sleep(BACKOFF ** (attempt + 1))
        except APIError:
            break
    return f"# Artículo provisional sobre {DOMAIN}\n\nContenido en breve."

if __name__ == "__main__":
    # Crear carpeta posts/
    os.makedirs("posts", exist_ok=True)

    # DEBUG: mostrar directorio de trabajo y existencia de JSON
    debug_path = os.path.join(os.getcwd(), "data/products.json")
    print("DEBUG: cwd=", os.getcwd())
    print("DEBUG: Looking for products at", debug_path)

    # Cargar lista de productos
    products_list = ""
    if os.path.exists(debug_path):
        print("DEBUG: data/products.json exists?", True)
        with open(debug_path, encoding="utf-8") as pf:
            products = json.load(pf)
        products_list = "\n\nModelos a comparar:\n" + "\n".join(
            f"- [{p['name']}](https://www.amazon.es/dp/{p['asin']}/?tag={ASSOCIATE_TAG})"
            for p in products
        )
    else:
        print("DEBUG: data/products.json exists?", False)

    # Generar posts
    for i in range(1, NUM_POSTS + 1):
        # Construir y debug del prompt
        prompt = (
            f"Genera un artículo de aproximadamente {WORDS_PER_POST} palabras sobre '{DOMAIN}'. "
            "Incluye una introducción, subtítulos claros, pros y contras, "
            "y ejemplos de enlaces a productos de Amazon con tu afiliado."
            f"{products_list}\n"
        )
        print("DEBUG: prompt=", prompt)

        raw = generate_post(prompt)
        print("DEBUG: Received raw content (first 200 chars)=", raw[:200])

        # Extraer título y fecha
        lines = raw.split("\n")
        title = lines[0].lstrip("# ").strip()
        date = datetime.date.today().isoformat()
        frontmatter = f"---\ntitle: {title}\ndate: {date}\n---\n\n"

        # Combinar y aplicar afiliados
        content = frontmatter + raw
        content = affiliateify(content)

        # Guardar fichero
        filename = f"posts/post_{i}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✔ Generado {filename}")
