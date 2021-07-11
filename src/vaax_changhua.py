import csv
import requests

config_hospital = {
    'url': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQbbCaUPFslVVvzp0sHOXxWIfwrWHL_6XHcwLVnwFA9k9nxR4tFOl-YzPlxpl6HGoZCyrDWAL6KYNTZ/pub?output=csv',
    'column_mapping': [
        ('施打站全稱', '醫療院所名稱'),
        ('施打站縣市', '縣市'),
        ('施打站行政區', '鄉鎮市區'),
        ('施打站地址', '地址'),
        ('預約電話', '洽詢電話')
    ],
    'discard_lines': 1
}
config_clinic = {
    'url': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQFilSFeFFQ9lRFuvqVLlx3RRy9EDo1BgBcpUShzbaYdLI9nj-tlmCVfNeGW2m_tQmRNWJRl_1WkPIB/pub?output=csv',
    'column_mapping': [
        ('施打站全稱', '診所名稱'),
        ('施打站縣市', '縣市'),
        ('施打站行政區', '鄉政市區'),
        ('施打站地址', '地址'),
        ('預約電話', '洽詢電話')
    ],
    'discard_lines': 1
}

def parse(config, output):
    with requests.Session() as s:
        response = s.get(config['url'], allow_redirects=True)
        content = response.content.decode('utf-8').split('\n', config['discard_lines'])[config['discard_lines']]
        rows = csv.DictReader(content.splitlines(), delimiter=',')
        for row in rows:
            result = dict()
            for column in config['column_mapping']:
                value = row.get(column[1], None)
                result[column[0]] = value
            output.append(result)

output_buffer = list();
parse(config_hospital, output_buffer)
parse(config_clinic, output_buffer)

with open('../output/changhua.csv', 'w', newline='', encoding='utf-8') as f:
    column_names = ['施打站全稱', '施打站縣市', '施打站行政區', '施打站地址', '預約電話']
    writer = csv.DictWriter(f, fieldnames=column_names, delimiter=',')
    writer.writeheader()
    for row in output_buffer:
        writer.writerow(row)