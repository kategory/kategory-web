import re
import os
import html

# German month translations and formatting
GERMAN_MONTHS = {
   'jan': ('Januar', '01'),
   'feb': ('Februar', '02'),
   'mär': ('März', '03'),
   'apr': ('April', '04'),
   'mai': ('Mai', '05'),
   'jun': ('Juni', '06'),
   'jul': ('Juli', '07'),
   'aug': ('August', '08'),
   'sep': ('September', '09'),
   'okt': ('Oktober', '10'),
   'nov': ('November', '11'),
   'dez': ('Dezember', '12')
}

def slugify(title):
   """
   Converts title into a clean, 7-bit ASCII slug for filenames.
   Max length: 32 characters. Assures it starts with a letter.
   """
   # Lowercase
   s = title.lower()
   # Replace German umlauts
   s = s.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
   # Replace non-alphanumeric characters with hyphens
   s = re.sub(r'[^a-z0-9\s\-]', '', s)
   # Replace spaces and multiple hyphens with single hyphen
   s = re.sub(r'[\s\-]+', '-', s)
   # Trim hyphens
   s = s.strip('-')
   # Max length 32 characters
   s = s[:32].strip('-')
   # Ensure it is a valid Python variable name if - is replaced by _
   if s and s[0].isdigit():
      s = 'b-' + s
   return s

def parse_inline_markdown(text):
   """
   Translates inline markdown like bold and links into HTML.
   Must be performed after HTML escaping.
   """
   text = html.escape(text)
   # Bold text
   text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
   # Inline links
   text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a class="kategory-link" href="\2">\1</a>', text)
   return text

def parse_markdown_table(lines):
   """
   Translates a markdown table into standard HTML table with Bootstrap styling.
   """
   table_lines = []
   table_lines.append('   <div class="table-responsive my-4">')
   table_lines.append('      <table class="table table-bordered text-dark border-dark-gray">')
   
   thead_rendered = False
   for line in lines:
      line = line.strip()
      if not line.startswith('|'):
         continue
      
      cells = [c.strip() for c in line.split('|')[1:-1]]
      # Skip column separators
      if all(re.match(r'^:?\-+:?$', c) for c in cells):
         continue
         
      if not thead_rendered:
         table_lines.append('         <thead>')
         table_lines.append('            <tr>')
         for cell in cells:
            cell_html = parse_inline_markdown(cell)
            table_lines.append(f'               <th scope="col">{cell_html}</th>')
         table_lines.append('            </tr>')
         table_lines.append('         </thead>')
         table_lines.append('         <tbody>')
         thead_rendered = True
      else:
         table_lines.append('            <tr>')
         for cell in cells:
            cell_html = parse_inline_markdown(cell)
            table_lines.append(f'               <td>{cell_html}</td>')
         table_lines.append('            </tr>')
         
   if thead_rendered:
      table_lines.append('         </tbody>')
      
   table_lines.append('      </table>')
   table_lines.append('   </div>')
   return '\n'.join(table_lines)

def markdown_to_html(md_text):
   """
   Translates block-level markdown (paragraphs, headings, lists, tables) to HTML.
   """
   # Clean up escape backslashes used in input file
   md_text = md_text.replace(r'\!', '!').replace(r'\.', '.')
   
   # Split by blank lines
   blocks = re.split(r'\n\s*\n', md_text.strip())
   html_blocks = []
   
   for block in blocks:
      block_lines = [line.strip() for line in block.strip().splitlines() if line.strip()]
      if not block_lines:
         continue
         
      # 1. Table check
      if block_lines[0].startswith('|'):
         html_blocks.append(parse_markdown_table(block_lines))
         continue
         
      # 2. Heading check
      first_line = block_lines[0]
      if first_line.startswith('#'):
         match = re.match(r'^(#{2,6})\s+(.+)$', first_line)
         if match:
            level = len(match.group(1))
            title_text = parse_inline_markdown(match.group(2))
            if level == 2:
               html_blocks.append(f'   <h2 class="h3 fw-bold mt-5 mb-3">{title_text}</h2>')
            elif level == 3:
               html_blocks.append(f'   <h3 class="h4 fw-bold mt-4 mb-3">{title_text}</h3>')
            else:
               html_blocks.append(f'   <h4 class="h5 fw-bold mt-3 mb-2">{title_text}</h4>')
            continue
            
      # 3. List check
      is_ul = first_line.startswith('* ') or first_line.startswith('- ')
      is_ol = re.match(r'^\d+\.\s+', first_line) is not None
      
      if is_ul or is_ol:
         list_type = 'ul' if is_ul else 'ol'
         items_html = []
         for line in block_lines:
            line_content = line.strip()
            if list_type == 'ul':
               line_content = re.sub(r'^[\*\-]\s+', '', line_content)
            else:
               line_content = re.sub(r'^\d+\.\s+', '', line_content)
            items_html.append(f'      <li>{parse_inline_markdown(line_content)}</li>')
            
         items_str = '\n'.join(items_html)
         html_blocks.append(f'   <{list_type}>\n{items_str}\n   </{list_type}>')
         continue
         
      # 4. Standard paragraph
      paragraph_text = ' '.join(block_lines)
      paragraph_html = parse_inline_markdown(paragraph_text)
      html_blocks.append(f'   <p>{paragraph_html}</p>')
      
   return '\n\n'.join(html_blocks)

def extract_teaser(md_text):
   """
   Robustly extracts the first plain text paragraph from markdown to use as teaser.
   Truncates to max 280 characters.
   """
   md_text = md_text.replace(r'\!', '!').replace(r'\.', '.')
   blocks = re.split(r'\n\s*\n', md_text.strip())
   for block in blocks:
      block_lines = [line.strip() for line in block.strip().splitlines() if line.strip()]
      if not block_lines:
         continue
      first_line = block_lines[0]
      # Skip headings, tables, and lists
      if first_line.startswith('#') or first_line.startswith('|') or first_line.startswith('*') or first_line.startswith('-') or re.match(r'^\d+\.\s+', first_line):
         continue
         
      # This is the first standard text paragraph
      paragraph = ' '.join(block_lines)
      # Strip bold and link markdown syntax for plain text teaser
      paragraph = re.sub(r'\*\*(.*?)\*\*', r'\1', paragraph)
      paragraph = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1', paragraph)
      
      if len(paragraph) > 280:
         paragraph = paragraph[:277] + '...'
      return paragraph
   return ""

def parse_blog_file(filepath):
   """
   Reads blog.md and parses all articles with their metadata and body.
   """
   with open(filepath, 'r', encoding='utf-8') as f:
      content = f.read()
      
   # Find all article boundaries using header patterns like "# 6.1 ..."
   matches = list(re.finditer(r'(?m)^#\s+6\.(\d+)\s+(.+)$', content))
   posts = []
   
   for idx, match in enumerate(matches):
      num = match.group(1)
      raw_title = match.group(2).strip()
      
      # Determine start and end indices of the article content block
      start_pos = match.end()
      end_pos = matches[idx + 1].start() if idx + 1 < len(matches) else len(content)
      article_block = content[start_pos:end_pos].strip().replace(r'\.', '.').replace(r'\!', '!')
      
      # Extract metadata
      date_match = re.search(r'(\d{1,2})\.\s*([A-Za-zä]+)\.?(?:\s*(\d{4}))?', article_block)
      reading_time_match = re.search(r'(\d+)\s*Min\.\s*Lesezeit', article_block)
      
      # Default year is 2026 if not specified
      year = "2026"
      day = 1
      month_name = "Januar"
      month_num = "01"
      
      if date_match:
         day = int(date_match.group(1))
         m_name_raw = date_match.group(2).lower()[:3]
         if m_name_raw in GERMAN_MONTHS:
            month_name, month_num = GERMAN_MONTHS[m_name_raw]
         if date_match.group(3):
            year = date_match.group(3)
      else:
         print(f"Warning: No date found for article 6.{num}: {raw_title}")
            
      iso_date = f"{year}-{month_num}-{day:02d}"
      formatted_date = f"{day:02d}. {month_name} {year}"
      
      reading_time = "3 Min. Lesezeit"
      if reading_time_match:
         reading_time = f"{reading_time_match.group(1)} Min. Lesezeit"
         
      # Extract Categories
      categories = []
      for line in article_block.splitlines():
         cat_match = re.match(r'^\*?\s*\[([^\]]+)\]\(https://www.kategory.de/blog/categories/[^\)]+\)', line.strip())
         if cat_match:
            categories.append(cat_match.group(1).strip())
            
      # Strip headers, metadata and category lines to get actual article body
      body_lines = []
      for line in article_block.splitlines():
         l_stripped = line.strip()
         if not l_stripped:
            body_lines.append("")
            continue
         # Skip metadata lines
         if "Jörg Kunze" in l_stripped or "Lesezeit" in l_stripped or "Min." in l_stripped:
            continue
         if date_match and date_match.group(0) in line:
            continue
         # Skip category list lines at bottom
         if "categories" in l_stripped:
            continue
         body_lines.append(line)
         
      body_text = '\n'.join(body_lines).strip()
      
      # Generiere HTML, Teaser und Dateiname (Slug)
      html_content = markdown_to_html(body_text)
      teaser = extract_teaser(body_text)
      slug = slugify(raw_title)
      filename = f"{iso_date}-{slug}.html"
      
      posts.append({
         'num': num,
         'title': raw_title,
         'slug': slug,
         'filename': filename,
         'formatted_date': formatted_date,
         'iso_date': iso_date,
         'reading_time': reading_time,
         'categories': categories,
         'html_content': html_content,
         'teaser': teaser
      })
      
   # Sort chronologically descending
   posts = sorted(posts, key=lambda x: x['iso_date'], reverse=True)
   return posts

def build_index_page(posts, output_path):
   """
   Generates the blog overview list index.html page (blog.html).
   """
   # Extract all unique categories to build the dynamic filters
   all_categories = []
   for p in posts:
      for cat in p['categories']:
         if cat not in all_categories:
            all_categories.append(cat)
            
   # Create Category Filter Buttons
   filter_buttons = []
   filter_buttons.append('      <button class="btn filter-pill active" data-category="all">Alle</button>')
   for cat in sorted(all_categories):
      filter_buttons.append(f'      <button class="btn filter-pill" data-category="{slugify(cat)}">{html.escape(cat)}</button>')
      
   # Create Post Cards HTML
   cards_html = []
   for p in posts:
      cat_slugs = ','.join([slugify(cat) for cat in p['categories']])
      cats_display = '\n'.join([
         f'            <span class="badge badge-category">{html.escape(cat)}</span>'
         for cat in p['categories']
      ])
      
      card = f"""   <div class="blog-post-card p-4 mb-4 border border-dark-gray" data-categories="{cat_slugs}">
      <div class="d-flex justify-content-between align-items-center mb-2 small text-muted">
         <span>{p['formatted_date']}</span>
         <span>{p['reading_time']}</span>
      </div>
      <h2 class="h3 mb-3">
         <a href="blog/{p['filename']}" class="blog-title-link">{html.escape(p['title'])}</a>
      </h2>
      <p class="text-muted mb-3">{html.escape(p['teaser'])}</p>
      <div class="d-flex flex-wrap gap-1">
{cats_display}
      </div>
   </div>"""
      cards_html.append(card)
      
   index_template = f"""<!doctype html>
<html lang="de">
   <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <meta name="description" content="Der Blog von kategory. Gedanken, Ideen und Erkenntnisse aus den Bereichen IT-Beratung, Prozesse und Regulatorik.">
      <title>Blog &amp; Insights - kategory</title>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
      <link href="kategory.css" rel="stylesheet">
   </head>
   <body>
      <main class="site-shell d-flex flex-column p-4 p-md-5">
         <header class="w-100 d-flex justify-content-between align-items-start mb-5">
            <a href="index.html" aria-label="Zurück zur Startseite">
               <img class="logismy-logo" src="kategory.svg" alt="kategory">
            </a>
            <div class="h3 fw-normal m-0 d-none d-sm-block">kategory</div>
         </header>

         <div class="container flex-grow-1 mx-auto w-100" style="max-width: 52rem;">
            <div class="text-center mb-5">
               <h1 class="display-5 fw-bold mb-3">Blog &amp; Insights</h1>
               <p class="h5 fw-normal text-muted mb-0">Gedanken, Ideen und Erkenntnisse</p>
            </div>

            <div class="d-flex flex-wrap justify-content-center gap-2 mb-5" id="category-filter-container">
{'\n'.join(filter_buttons)}
            </div>

            <div class="d-flex flex-column gap-3" id="blog-posts-container">
{'\n\n'.join(cards_html)}
            </div>
         </div>

         <footer class="w-100 text-center mt-5 pt-4 border-top border-dark-gray">
            <p class="text-muted small mb-0">&copy; 2026 kategory.de. Alle Rechte vorbehalten.</p>
         </footer>
      </main>

      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
      <script>
         document.addEventListener('DOMContentLoaded', () => {{
            const buttons = document.querySelectorAll('.filter-pill');
            const cards = document.querySelectorAll('.blog-post-card');

            buttons.forEach(btn => {{
               btn.addEventListener('click', () => {{
                  buttons.forEach(b => b.classList.remove('active'));
                  btn.classList.add('active');

                  const filter = btn.getAttribute('data-category');
                  cards.forEach(card => {{
                     if (filter === 'all') {{
                        card.style.display = 'block';
                     }} else {{
                        const cats = card.getAttribute('data-categories').split(',');
                        if (cats.includes(filter)) {{
                           card.style.display = 'block';
                        }} else {{
                           card.style.display = 'none';
                        }}
                     }}
                  }});
               }});
            }});
         }});
      </script>
   </body>
</html>
"""
   # Assure we write with utf-8
   with open(output_path, 'w', encoding='utf-8') as f:
      f.write(index_template)

def build_detail_page(post, output_path):
   """
   Generates an individual blog detail page.
   """
   cats_display = '\n'.join([
      f'                     <span class="badge badge-category">{html.escape(cat)}</span>'
      for cat in post['categories']
   ])
   
   detail_template = f"""<!doctype html>
<html lang="de">
   <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <meta name="description" content="{html.escape(post['teaser'])}">
      <title>{html.escape(post['title'])} - kategory</title>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
      <link href="../kategory.css" rel="stylesheet">
   </head>
   <body>
      <main class="site-shell d-flex flex-column p-4 p-md-5">
         <header class="w-100 d-flex justify-content-between align-items-start mb-5">
            <a href="../index.html" aria-label="Zurück zur Startseite">
               <img class="logismy-logo" src="../kategory.svg" alt="kategory">
            </a>
            <div class="h3 fw-normal m-0 d-none d-sm-block">kategory</div>
         </header>

         <article class="container flex-grow-1 mx-auto w-100 mb-5" style="max-width: 44rem;">
            <div class="mb-5">
               <a href="../blog.html" class="back-link text-decoration-none d-inline-flex align-items-center mb-4">
                  <span class="me-1">&larr;</span> Zurück zur Übersicht
               </a>
               <div class="d-flex align-items-center gap-2 small text-muted mb-2">
                  <span>{post['formatted_date']}</span>
                  <span>&bull;</span>
                  <span>{post['reading_time']}</span>
               </div>
               <h1 class="display-6 fw-bold mb-4">{html.escape(post['title'])}</h1>
               <div class="d-flex flex-wrap gap-1">
{cats_display}
               </div>
               <hr class="border-dark-gray mt-4 mb-0">
            </div>

            <div class="blog-content">
{post['html_content']}
            </div>
         </article>

         <footer class="w-100 text-center mt-auto pt-4 border-top border-dark-gray">
            <p class="text-muted small mb-0">&copy; 2026 kategory.de. Alle Rechte vorbehalten.</p>
         </footer>
      </main>

      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
   </body>
</html>
"""
   with open(output_path, 'w', encoding='utf-8') as f:
      f.write(detail_template)

def main():
   blog_file = 'blog.md'
   blog_dir = 'blog'
   
   # Create blog directory if it does not exist
   if not os.path.exists(blog_dir):
      os.makedirs(blog_dir)
      print(f"Directory '{blog_dir}' created.")
      
   print("Parsing blog.md...")
   posts = parse_blog_file(blog_file)
   
   print(f"Found {len(posts)} articles.")
   
   # 1. Build blog.html (overview)
   print("Generating blog.html...")
   build_index_page(posts, 'blog.html')
   
   # 2. Build detail pages in blog/
   print("Generating blog articles detail pages...")
   for p in posts:
      out_file = os.path.join(blog_dir, p['filename'])
      print(f" -> {out_file}")
      build_detail_page(p, out_file)
      
   print("Generation completed successfully!")

if __name__ == '__main__':
   main()
