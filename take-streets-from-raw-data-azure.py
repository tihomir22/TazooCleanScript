import asyncio
from azure.storage.blob import BlobServiceClient
import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd
from io import BytesIO
import os
from dotenv import load_dotenv
load_dotenv()  

blob_service_client = BlobServiceClient.from_connection_string(os.environ.get('CONNECTION_STRING'))
container_client = blob_service_client.get_container_client(os.environ.get('CONTAINER_NAME'))

blobs = container_client.list_blobs()
for blob in blobs:
    # Obtener el nombre del blob
    blob_name = blob.name
    print(blob_name)
    
    # Descargar el blob y guardarlo en un archivo local
    with open(blob_name, "wb") as file:
        blob_data = container_client.get_blob_client(blob_name)
        file.write(blob_data.download_blob().readall())
    
    # Procesar el archivo descargado, por ejemplo, leer un archivo Parquet en un DataFrame de pandas
    df = pd.read_parquet(blob_name)
    print(df['enter'])
    print(df['exit'])
    # Realizar operaciones adicionales con el DataFrame
    # ...
    
    # Eliminar el archivo descargado si ya no es necesario
    os.remove(blob_name)