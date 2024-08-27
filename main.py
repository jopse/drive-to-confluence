import configparser
from google.oauth2 import service_account
from googleapiclient.discovery import build
from atlassian import Confluence
from bs4 import BeautifulSoup

# Cargar configuración desde el archivo config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Autenticación con Google Drive API
def authenticate_google_drive():
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    SERVICE_ACCOUNT_FILE = config['google']['service_account_file']

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('drive', 'v3', credentials=credentials)
    return service

# Autenticación con Confluence API
def authenticate_confluence():
    confluence = Confluence(
        url=config['confluence']['url'],
        username=config['confluence']['username'],
        password=config['confluence']['api_token']
    )
    return confluence

# Obtener estructura de carpetas y archivos de Google Drive
def get_drive_folder_structure(service, folder_id):
    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    items = results.get('files', [])

    folder_structure = []
    for item in items:
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            sub_folder = get_drive_folder_structure(service, item['id'])
            folder_structure.append({'name': item['name'], 'type': 'folder', 'id': item['id'], 'contents': sub_folder})
        else:
            folder_structure.append({'name': item['name'], 'type': 'file', 'id': item['id']})
    return folder_structure

# Exportar documentos de Google Drive
def export_drive_document(service, file_id, mime_type='text/html'):
    request = service.files().export_media(fileId=file_id, mimeType=mime_type)
    response = request.execute()
    return response.decode('utf-8')  # Decodificar contenido HTML

# Extraer índice y contenido del documento
def extract_toc_and_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    toc = []
    main_content = ''
    
    headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    for header in headers:
        toc.append({'title': header.get_text(), 'level': int(header.name[1]), 'content': str(header)})
        header.decompose()
    
    main_content = str(soup.body)
    return toc, main_content

# Crear página en Confluence
def create_confluence_page(confluence, space, parent_page_id, title, content):
    return confluence.create_page(
        space=space,
        title=title,
        body=content,
        parent_id=parent_page_id
    )

# Crear subpáginas en Confluence basadas en el índice
def create_confluence_subpages(confluence, space, parent_page_id, toc):
    for entry in toc:
        new_page = create_confluence_page(confluence, space, parent_page_id, entry['title'], entry['content'])
        new_page_id = new_page['id']

# Crear la estructura en Confluence
def create_confluence_structure(confluence, space, parent_page_id, folder_structure, drive_service):
    for item in folder_structure:
        if item['type'] == 'folder':
            new_page = create_confluence_page(confluence, space, parent_page_id, item['name'], '')
            new_page_id = new_page['id']
            create_confluence_structure(confluence, space, new_page_id, item['contents'], drive_service)
        else:
            if item['name'].endswith('.gdoc'):  # Si es un Google Doc
                html_content = export_drive_document(drive_service, item['id'])
                toc, main_content = extract_toc_and_content(html_content)
                
                # Crear la página principal
                main_page = create_confluence_page(confluence, space, parent_page_id, item['name'], main_content)
                main_page_id = main_page['id']

                # Crear subpáginas basadas en el índice
                create_confluence_subpages(confluence, space, main_page_id, toc)
            else:
                # Manejar otros tipos de archivos según sea necesario
                content = f"Archivo: {item['name']}"
                create_confluence_page(confluence, space, parent_page_id, item['name'], content)

# Ejecución del script
if __name__ == "__main__":
    # Autenticación
    drive_service = authenticate_google_drive()
    confluence = authenticate_confluence()

    # Configura los IDs y espacios necesarios desde config.ini
    google_drive_folder_id = config['google']['drive_folder_id']
    confluence_space = config['confluence']['space_key']
    confluence_parent_page_id = config['confluence']['parent_page_id']

    # Obtén la estructura de la carpeta de Google Drive
    folder_structure = get_drive_folder_structure(drive_service, google_drive_folder_id)

    # Crea la estructura en Confluence
    create_confluence_structure(confluence, confluence_space, confluence_parent_page_id, folder_structure, drive_service)
