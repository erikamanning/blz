import requests
import requests_mock
session = requests.Session()
adapter = requests_mock.Adapter()
session.mount('mock://', adapter)
adapter.register_uri('GET', 'mock://test.com', text='data')
resp = session.get('mock://test.com')
resp.status_code, resp.text

from datetime import date 
TODAY = date.today()


