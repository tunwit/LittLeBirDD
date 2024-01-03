from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload, MediaUploadProgress
import os
import json
import datetime
import math
import discord
from request_data import request

credentials = service_account.Credentials.from_service_account_file(
    r'moonlit-poetry-378910-6523bdf8fae3.json',
    scopes=['https://www.googleapis.com/auth/drive'])
drive_service = build('drive', 'v3', credentials=credentials)
EXPIRE_TIME_HOUR = 24

class google_driveAPI():

    async def upload_link(file_path,interaction:discord.Interaction,title,respound):
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=EXPIRE_TIME_HOUR)
        expiration_date = expiration_time.isoformat() + 'z' 
        file_name = title+".mp4" 
        file_metadata = {'name': file_name,"parents":["1NGAJlp2zNc9nwpOzbd8N-KJeaR-y_kqj"]}
        media = MediaFileUpload(file_path,resumable=True,chunksize=math.ceil(os.path.getsize(file_path)*0.15))
        file = drive_service.files().create(body=file_metadata, media_body=media)
        response = None
        await interaction.edit_original_response(content = respound.get('uploading0').format(file_name=file_name))
        while response is None:
            status, response = file.next_chunk()
            if status:
                await interaction.edit_original_response(content = respound.get('uploading').format(file_name=file_name,percent=int(status.progress() * 100)))
                
        await interaction.edit_original_response(content=respound.get('upload_complete'))
        file_id = response["id"]
        file_url = f'https://drive.google.com/file/d/{file_id}'
        permission = {
            'type': 'anyone',
            'role': 'reader',
            'expirationTime': expiration_date
        }
        drive_service.permissions().create(fileId=file_id, body=permission).execute()
        re = request("database/deletefile.json")
        data = re.request_access()
        data[file_id] = expiration_time.strftime('%Y-%m-%d %H:%M:%S')
        re.update_access(data)
        await interaction.edit_original_response(content = respound.get('drive_uploaded').format(link = file_url))

