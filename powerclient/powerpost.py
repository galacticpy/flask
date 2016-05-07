import requests
import json

def postApi(apikey,merchantid,pageid):
    url = 'http://services.powerreviews.com/api/reviews/'
    headers={'content-type': 'application/json'}
    
    data={'review': {'page_id': pageid,
                         'locale': 'en_US',
                         'headline': 'Testing Api Response',
                         'comments': 'Test Api Response Comment',
                         'rating': '5',
                         'name': 'Test API',
                         'location': 'Chicago'}}
    data=json.dumps(data)
    
    params={'apikey': apikey,'format': 'json','merchant_id': merchantid, 'review_data':data}
    
    writeapi = requests.post(url, params=params, headers=headers)
    response = writeapi.json()
    return response

