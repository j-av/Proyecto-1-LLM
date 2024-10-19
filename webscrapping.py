import requests
from bs4 import BeautifulSoup
import os

# Ruta donde se guardarán los archivos obtenidos
docs_path = r"C:\Users\USUARIO\PycharmProjects\doc-assistant\langchain-docs\api.python.langchain.com\en\latest"

# Función que obtiene y guarda el contenido de una página
def save_page_content(url, folder_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extrae el contenido principal de la página
        page_text = soup.get_text()

        # Genera el nombre del archivo a partir de la URL
        file_name = url.replace("https://", "").replace("/", "_") + ".txt"
        file_path = os.path.join(folder_path, file_name)

        # Guarda el contenido en un archivo de texto
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(page_text)
            print(f"Página guardada: {file_path}")

        return soup  # Devuelve el contenido parseado para extraer más enlaces

    except Exception as e:
        print(f"Error al obtener la página {url}: {e}")
        return None

# Función que extrae enlaces de una página y los guarda
def scrape_and_save_links(url, folder_path):
    # Obtiene el contenido de la página y lo guarda
    soup = save_page_content(url, folder_path)
    
    if soup:
        # Extrae todos los enlaces de la página
        links = soup.find_all('a', href=True)
        for link in links:
            # Convierte los enlaces relativos a enlaces absolutos
            href = link['href']
            if href.startswith("/"):
                href = url.rstrip("/") + href
            elif not href.startswith("http"):
                continue  # Ignora enlaces no válidos

            # Recursivamente guarda las páginas vinculadas
            save_page_content(href, folder_path)

# URL de inicio
start_url = "https://www.britannica.com/money/DreamWorks-Animation"

if __name__ == "__main__":
    # Verifica que el directorio de destino exista, si no, lo crea
    if not os.path.exists(docs_path):
        os.makedirs(docs_path)

    # Inicia el scraping desde la URL base
    scrape_and_save_links(start_url, docs_path)
