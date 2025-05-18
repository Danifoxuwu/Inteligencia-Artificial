import requests
from bs4 import BeautifulSoup, NavigableString

def limpiar_texto(texto):
    # Elimina líneas vacías, espacios repetidos y líneas muy cortas (ruido)
    lineas = [line.strip() for line in texto.split('\n')]
    lineas = [line for line in lineas if len(line) > 0 and not line.lower().startswith(('copyright', '©', 'todos los derechos'))]
    texto_limpio = '\n'.join(lineas)
    return texto_limpio

def extraer_texto_de_web(url, archivo_salida):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Elimina scripts, estilos, formularios, anuncios, navegación, pie de página, encabezados, iframes, botones, imágenes y enlaces
    for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'form', 'noscript', 'iframe', 'button', 'img', 'figure', 'picture']):
        tag.decompose()
    # Elimina todos los enlaces pero deja el texto visible
    for a in soup.find_all('a'):
        a.unwrap()

    # Busca el contenido principal por selectores comunes
    main_content = None
    for selector in [
        'article', 'main', '[role=main]', '[id*=content]', '[class*=content]', '[id*=art]', '[class*=art]',
        '[id*=body]', '[class*=body]', '[id*=texto]', '[class*=texto]'
    ]:
        main_content = soup.select_one(selector)
        if main_content:
            break

    # Si no encuentra, busca el bloque más largo de texto en el body
    if not main_content and soup.body:
        max_text = ''
        for tag in soup.body.find_all(recursive=True):
            if isinstance(tag, NavigableString):
                continue
            text = tag.get_text(separator=' ', strip=True)
            if len(text) > len(max_text):
                max_text = text
        main_content = max_text

    # Extrae y limpia el texto
    if main_content:
        if isinstance(main_content, str):
            texto = main_content
        else:
            texto = main_content.get_text(separator='\n', strip=True)
    else:
        texto = soup.get_text(separator='\n', strip=True)

    texto_limpio = limpiar_texto(texto)

    # Forzar extensión .txt si no está presente
    if not archivo_salida.lower().endswith('.txt'):
        archivo_salida += '.txt'

    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write(texto_limpio)

if __name__ == "__main__":
    url = input("Introduce la URL de la página web: ").strip()
    if not url:
        url = "https://scielo.isciii.es/scielo.php?pid=S1886-58872018000200004&script=sci_arttext"
    archivo_salida = input("Nombre del archivo de salida (ejemplo: salida.txt): ").strip()
    if not archivo_salida:
        archivo_salida = "salida.txt"
    extraer_texto_de_web(url, archivo_salida)
    print(f"Texto extraído y guardado en {archivo_salida}")
