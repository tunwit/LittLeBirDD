from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import datetime
from discord.ext import commands,tasks

credentials = service_account.Credentials.from_service_account_file(
    r'moonlit-poetry-378910-6523bdf8fae3.json',
    scopes=['https://www.googleapis.com/auth/drive'])
drive_service = build('drive', 'v3', credentials=credentials)

@tasks.loop(seconds=10,reconnect=True)
async def delete():
    with open("database/deletefile.json", "r") as f:
        data = json.load(f)
    for i in list(data):
        next_hour = datetime.datetime.strptime(data[i], '%Y-%m-%d %H:%M:%S')
        if datetime.datetime.utcnow() > next_hour:
            try:
                file = drive_service.files().get(fileId=i).execute()
                drive_service.files().delete(fileId=i).execute()
                del data[i]
                with open("database/deletefile.json", "w" ,encoding="utf8") as f:
                    json.dump(data,f,ensure_ascii=False,indent=4)
                print(f"{file['name']} has been deleted")
            except HttpError as error:
                if error.resp.status == 404:
                    del data[i]
                    with open("database/deletefile.json", "w" ,encoding="utf8") as f:
                        json.dump(data,f,ensure_ascii=False,indent=4)
                    print(f"The file doesn't exist on Google Drive. deleting {i}")
                else:
                    print(error)


                


