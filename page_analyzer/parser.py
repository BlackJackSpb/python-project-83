from bs4 import BeautifulSoup

def parse_seo_data(html_text):
    soup = BeautifulSoup(html_text, 'lxml')
    h1_tag = soup.find('h1')
    h1 = (h1_tag.string.strip()
          if h1_tag and h1_tag.string else '')
    title_tag = soup.find('title')
    title = (title_tag.string.strip()
             if title_tag and title_tag.string else '')
    desc_meta = soup.find('meta', attrs={'name': 'description'})
    description = (desc_meta.get('content', '').strip()
                   if desc_meta else '')
    return {'h1': h1, 'title': title, 'description': description}