# drive-to-confluence
Migration from Drive to Clonfluence Cloud

## Pasos para configurar y ejecutar el script:
### Credenciales y configuración:
1. Crea el archivo config.ini:
2. Usa el fichero de ejemplo proporcionado, ajustando los valores de las variables según tu configuración.
   2.1. Reemplaza 'path_to_your_service_account.json' con la ruta a tu archivo de credenciales de Google Drive.
   2.2. Sustituye 'your_email' y 'your_api_token' por tu correo electrónico y token de API de Confluence.
   2.3. Configura los IDs de la carpeta de Google Drive (google_drive_folder_id), el espacio en Confluence (confluence_space), y el ID de la página padre en Confluence (confluence_parent_page_id).
3. Coloca el archivo config.ini en el mismo directorio que el script.

### Instalación de dependencias: Asegúrate de tener instaladas las siguientes librerías:
``` bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client atlassian-python-api beautifulsoup4
```

## Ejecución
```bash
cd /ruta/al/directorio/del/script/
python migrate_drive_to_confluence.py
```

## Notas adicionales:
### HTML Parsing: 
El análisis del índice se realiza con BeautifulSoup, un enfoque básico que puede requerir ajustes según la estructura del documento.
### Límites de la API: 
Asegúrate de manejar posibles errores de API y límites de tasa en producción.
### Soporte de archivos:
Actualmente, solo los documentos de Google Docs son tratados para la exportación. Otros tipos de archivos se manejan como texto simple. Adapta el script según tus necesidades.
### Service account de Google
1. Crear un Proyecto en Google Cloud Console
Visita Google Cloud Console: Ve a Google Cloud Console.
Crear un nuevo proyecto:
En la barra superior, haz clic en el selector de proyecto (junto al logo de Google Cloud) y luego en "Nuevo Proyecto".
Dale un nombre a tu proyecto y haz clic en "Crear".
2. Habilitar la API de Google Drive
Seleccionar el proyecto: Asegúrate de que tu nuevo proyecto esté seleccionado en el selector de proyectos.
Habilitar la API:
En la barra lateral, ve a "APIs y servicios" > "Biblioteca".
Busca "Google Drive API" y haz clic en "Habilitar".
3. Crear una Cuenta de Servicio
Ir a "Credenciales":

En la barra lateral, ve a "APIs y servicios" > "Credenciales".
Haz clic en "Crear credenciales" y selecciona "Cuenta de servicio".
Configurar la cuenta de servicio:

Dale un nombre a tu cuenta de servicio y selecciona un rol, como "Editor" o "Owner".
Continúa con la configuración y haz clic en "Hecho". No es necesario asignar usuarios o permisos adicionales en este paso.
Generar la clave JSON:

En la lista de cuentas de servicio, busca la cuenta de servicio recién creada.
Haz clic en el ícono de edición (lápiz) para esa cuenta de servicio.
En la sección "Claves", haz clic en "Añadir clave" > "Crear clave".
Selecciona el formato JSON y haz clic en "Crear". Esto descargará el archivo service_account.json a tu computadora.
4. Configurar permisos de la cuenta de servicio en Google Drive
Compartir la carpeta de Google Drive:
Ve a Google Drive y selecciona la carpeta que deseas exportar.
Haz clic en "Compartir" y añade el correo electrónico de la cuenta de servicio (algo como your-service-account@your-project-id.iam.gserviceaccount.com).
Dale permisos de "Editor" o "Viewer" según sea necesario.
