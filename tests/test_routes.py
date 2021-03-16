import urllib
import pytest
import config


@pytest.mark.usefixtures("test_client")
def test_authenticate_route_redirects_to_authentication_uri(test_client):
    client_id = config.CONFIG['CLIENT_ID']
    redirect_url = config.CONFIG['REDIRECT_URL']

    url_parameters = urllib.parse.urlencode({
        'response_type': 'code',
        'response_mode': 'form_post',
        'client_id': client_id,
        'scope': 'info cards accounts transactions balance offline_access',
        'redirect_uri': redirect_url,
        'providers': 'uk-cs-mock'
    })

    authentication_link = f'https://auth.truelayer.com/?{url_parameters}'

    with test_client:
        response = test_client.get('/')
        assert response.status_code == 200

@pytest.mark.usefixtures("test_client")
def test_authenticate_handler_redirects_to_transaction_route(test_client):

    with test_client:
        response = test_client.post('/signin_callback')
        assert response.status_code == 200
