import requests

def get_user(access_token):
    url = "https://www.googleapis.com/userinfo/v2/me"
    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user = response.json()
        return user['email']
    elif response.status_code == 401:
        return None


