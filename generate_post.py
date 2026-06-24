import sys, os, json, datetime, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import asyncio
from src.services.ai_service import ollama_chat

BLOG_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_DIR = os.path.join(BLOG_DIR, 'posts')
INDEX_FILE = os.path.join(BLOG_DIR, 'index.html')

NICHIOS = [
    "como generar contenido para redes sociales con IA",
    "mejores herramientas IA para marketing digital Chile",
    "automatizar contenido redes sociales pequeña empresa",
    "chatbot IA para atencion al cliente Chile",
    "como crear descripciones de productos para MercadoLibre",
    "inteligencia artificial para generar contenido SEO",
    "ahorrar tiempo en marketing de contenidos con IA",
    "como hacer publicaciones para Instagram con IA",
    "ideas de contenido para LinkedIn IA",
    "automatizar WhatsApp Business con inteligencia artificial",
    "generador textos publicitarios para Google Ads",
    "como escribir articulos blog SEO con IA",
]

async def generate_article(topic: str) -> dict:
    system = (
        "Eres un experto en marketing digital y contenido para negocios chilenos. "
        "Genera un artículo en español optimizado para SEO. "
        "Incluye: título llamativo, introducción, subtítulos (h2, h3), "
        "consejos prácticos, y una conclusión que promueva el uso de herramientas de IA. "
        "El artículo debe tener entre 800-1200 palabras."
    )

    prompt = (
        f"Escribe un artículo de blog completo sobre: {topic}. "
        "Al final, menciona que herramientas como bots de IA en Telegram "
        "pueden ayudar a generar contenido automáticamente (menciona ContentForge)."
    )

    content = await ollama_chat(prompt, system)
    today = datetime.date.today().isoformat()

    title = content.split('\n')[0].replace('#', '').strip() if content else topic
    slug = topic.lower().replace(' ', '-').replace('í', 'i').replace('á', 'a')[:50]
    slug = ''.join(c for c in slug if c.isalnum() or c == '-')

    article = {
        'title': title,
        'slug': slug,
        'date': today,
        'topic': topic,
        'content': content,
        'filename': f"{today}-{slug}.html"
    }

    return article


def save_article(article: dict):
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']} - ContentForge Blog</title>
    <meta name="description" content="Artículo sobre {article['topic']} generado con IA">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.7; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2563eb; margin: 30px 0 15px; }}
        h2 {{ color: #1e40af; margin: 25px 0 10px; }}
        p {{ margin: 15px 0; }}
        .meta {{ color: #6b7280; font-size: 0.9em; margin-bottom: 30px; }}
        .cta {{ background: #f0fdf4; border: 1px solid #22c55e; padding: 20px; border-radius: 8px; margin: 30px 0; text-align: center; }}
        .cta a {{ display: inline-block; background: #22c55e; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: 600; }}
        footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb; text-align: center; color: #6b7280; }}
    </style>
</head>
<body>
    <article>
        <h1>{article['title']}</h1>
        <div class="meta">Publicado: {article['date']} | Categoría: {article['topic']}</div>
        <div>{article['content'].replace(chr(10), '<br>')}</div>
    </article>

    <div class="cta">
        <p><strong>¿Quieres generar contenido como este automáticamente?</strong></p>
        <p>ContentForge Bot genera artículos SEO, posts para redes sociales y más por IA.</p>
        <a href="https://t.me/AILocalMachine_bot" target="_blank"> Probar ContentForge Gratis</a>
    </div>

    <footer>
        <p><a href="/">ContentForge Blog</a> | Contenido generado con IA para negocios chilenos</p>
    </footer>
</body>
</html>"""

    filepath = os.path.join(POSTS_DIR, article['filename'])
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    return article['filename']


def update_index(articles: list):
    posts_html = ""
    articles2 = []
    for a in articles:
        if isinstance(a, dict) and 'filename' in a:
            articles2.append(a)
    articles = articles2
    for a in sorted(articles, key=lambda x: x.get('date', ''), reverse=True):

        if not isinstance(a, dict) or 'filename' not in a:
            continue
        posts_html += f"""
        <article>
            <h2><a href="posts/{a['filename']}">{a['title']}</a></h2>
            <p>{a['topic']} - {a['date']}</p>
        </article>"""

    index = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ContentForge Blog - Marketing Digital con IA para Chile</title>
    <meta name="description" content="Blog con artículos generados por IA sobre marketing digital, contenido y automatización para negocios chilenos">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
        header {{ background: linear-gradient(135deg, #2563eb, #7c3aed); color: white; padding: 40px 20px; border-radius: 12px; margin: 20px 0; text-align: center; }}
        header h1 {{ font-size: 2em; margin-bottom: 10px; }}
        article {{ padding: 20px; margin: 15px 0; background: #f8fafc; border-radius: 8px; }}
        article h2 {{ color: #2563eb; }}
        article a {{ color: #2563eb; text-decoration: none; }}
        article a:hover {{ text-decoration: underline; }}
        .cta {{ background: #f0fdf4; border: 1px solid #22c55e; padding: 20px; border-radius: 8px; margin: 30px 0; text-align: center; }}
        .cta a {{ display: inline-block; background: #22c55e; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: 600; }}
        footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb; text-align: center; color: #6b7280; }}
    </style>
</head>
<body>
    <header>
        <h1>ContentForge Blog</h1>
        <p>Marketing digital, contenido automatizado e IA para negocios chilenos</p>
        <p style="margin-top:15px"><a href="https://t.me/AILocalMachine_bot" style="color:white;background:#22c55e;padding:10px 20px;border-radius:6px;text-decoration:none;font-weight:600;"> Probar ContentForge</a></p>
    </header>

    <h2 style="margin:30px 0 15px;color:#1e40af;">Últimos Artículos</h2>
    {posts_html}

    <div class="cta">
        <p><strong>Genera contenido para tu negocio con IA</strong></p>
        <p>ContentForge Bot crea artículos SEO, posts sociales, descripciones y más.</p>
        <a href="https://t.me/AILocalMachine_bot" target="_blank"> Comenzar Gratis</a>
    </div>

    <footer>
        <p>ContentForge Blog | Contenido generado con IA para el mercado chileno</p>
    </footer>
</body>
</html>"""

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(index)


def load_existing_articles():
    articles = []
    if os.path.exists(POSTS_DIR):
        for fname in os.listdir(POSTS_DIR):
            if fname.endswith('.html'):
                filepath = os.path.join(POSTS_DIR, fname)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                title = "Artículo"
                topic = "general"
                date = fname[:10]
                for line in content.split('\n'):
                    if '<h1>' in line:
                        title = line.split('<h1>')[1].split('</h1>')[0]
                    if 'Categoría:' in line:
                        topic = line.split('Categoría: ')[1].split('<')[0]
                articles.append({
                    'title': title,
                    'filename': fname,
                    'date': date,
                    'topic': topic
                })
    return articles


async def main():
    import random
    topic = random.choice(NICHIOS)

    print(f"Generando artículo sobre: {topic}...")
    article = await generate_article(topic)
    filename = save_article(article)
    print(f"Artículo guardado: {filename}")

    existing = load_existing_articles()
    existing.append(article)
    update_index(existing)
    print(f"Blog actualizado. Total artículos: {len(existing)}")

    # Push to GitHub Pages
    repo_dir = BLOG_DIR
    token = os.environ.get("GH_TOKEN")
    if not token:
        raise ValueError("GH_TOKEN environment variable not set")
    try:
        subprocess.run(["git", "add", "-A"], cwd=repo_dir, capture_output=True)
        subprocess.run(["git", "commit", "-m", f"New post: {filename}"], cwd=repo_dir, capture_output=True)
        remote = f"https://mjtacevalme-Solutions:{token}@github.com/mjtacevalme-Solutions/contentforge-blog.git"
        subprocess.run(["git", "remote", "set-url", "origin", remote], cwd=repo_dir, capture_output=True)
        r = subprocess.run(["git", "push", "origin", "main"], cwd=repo_dir, capture_output=True, text=True)
        if r.returncode == 0:
            print("Publicado en: https://mjtacevalme-solutions.github.io/contentforge-blog/")
        else:
            print(f"Push stderr: {r.stderr}")
    except Exception as e:
        print(f"Push error: {e}")


if __name__ == '__main__':
    asyncio.run(main())
