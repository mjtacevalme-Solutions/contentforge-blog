import os
POSTS_DIR = 'posts'
INDEX_FILE = 'index.html'

articles = []
seen_filenames = set()

for fname in sorted(os.listdir(POSTS_DIR), reverse=True):
    if fname.endswith('.html') and fname not in seen_filenames:
        seen_filenames.add(fname)
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
        articles.append({'title': title, 'filename': fname, 'date': date, 'topic': topic})

articles_html = ''
for a in sorted(articles, key=lambda x: x['date'], reverse=True):
    articles_html += f'''
        <article>
            <h2><a href="posts/{a['filename']}">{a['title']}</a></h2>
            <p>{a['topic']} - {a['date']}</p>
        </article>'''

index = f'''<!DOCTYPE html>
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
    {articles_html}

    <div class="cta">
        <p><strong>Genera contenido para tu negocio con IA</strong></p>
        <p>ContentForge Bot crea artículos SEO, posts sociales, descripciones y más.</p>
        <a href="https://t.me/AILocalMachine_bot" target="_blank"> Comenzar Gratis</a>
    </div>

    <footer>
        <p>ContentForge Blog | Contenido generado con IA para el mercado chileno</p>
    </footer>
</body>
</html>'''

with open(INDEX_FILE, 'w', encoding='utf-8') as f:
    f.write(index)

print(f'Index regenerated with {len(articles)} unique articles')
