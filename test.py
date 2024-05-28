import requests

# dataOBJ = { "case": 1, "ref_number": '28327', "cardid": '3005986032' }
# result = requests.post('https://center.cpw.ac.th/topup/topup/getdata.php',data=dataOBJ) #get balance
# print(result.json())

data = {
        "ref_number": '28182',
        "year": '2566',
        "term": '2',
        "token": '6f0cf653c75f2137e14061e5598884',
        "case": 1
    }
respound = requests.post('https://app.cpw.ac.th/gradereport/result/getdata.php',data=data) #get grad

result = respound.json()['data']

try:
    gradlocation = result['grade']['data']
except:
    gradlocation = result['score']['data']

print('ชื่อ',result['Student']['data']['nameTH'],result['Student']['data']['room'])
for i in gradlocation:
    print(f"{i['course_name']:40}",i['course_no'],i['score'],i['result'])