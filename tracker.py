from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
from datetime import date, timedelta

SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
KEY_FILE = 'service-account.json'

credentials = service_account.Credentials.from_service_account_file(
        KEY_FILE, scopes=SCOPES)

service = build('searchconsole', 'v1', credentials=credentials)

site_url = 'https://doorsystemsonline.co.uk/'

end_date = date.today()
start_date = end_date - timedelta(days=7)

request = {
    'startDate': start_date.strftime('%Y-%m-%d'),
    'endDate': end_date.strftime('%Y-%m-%d'),
    'dimensions': ['query'],
    'rowLimit': 1000
}

response = service.searchanalytics().query(siteUrl=site_url, body=request).execute()

rows = response.get('rows', [])
data = []

for row in rows:
    data.append([
        row['keys'][0],
        row.get('clicks', 0),
        row.get('impressions', 0),
        row.get('position', 0)
    ])

df = pd.DataFrame(data, columns=['Keyword', 'Clicks', 'Impressions', 'Position'])

df.to_csv('results/keyword_positions.csv', index=False)

print("Tracking Complete")
