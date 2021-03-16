import os
import urllib
import time
import requests
from client.api import DataAPI
from client.account import Account
from client.credentials import UserCredentials
from client.client_app import ClientCredentials
from flask import Flask, url_for, request, render_template, redirect
from werkzeug.utils import redirect

app = Flask(__name__)

client_creds = ClientCredentials()
CLIENT_ID = client_creds.client_id
SECRET_ID = client_creds.client_secret
REDIRECT_URL = client_creds.redirect_uri

AUTH_API = 'https://auth.truelayer.com/'

CLIENT_DATA = {}

# Home route
@app.route("/", methods=["GET"])
def sign_in():
    query = urllib.parse.urlencode(
        {
            "response_type": "code",
            "client_id": CLIENT_ID,
            "scope": "info cards accounts transactions offline_access",
            "nonce": int(time.time()),
            "redirect_uri": REDIRECT_URL,
            "enable_mock": "true",
            "enable_open_banking_providers": "true",
            "enable_credentials_sharing_providers": "false",
        }
    )

    authentication_link = f'{AUTH_API}?{query}'
    return f'Click <a href="{authentication_link}">here</a> to connect to your bank account'

@app.route("/signin_callback", methods=["GET"])
def handle_signin():
    # Accessing query parameters in Flask
    authorization_code = request.args.get("code")
    
    user_creds = UserCredentials(client_credentials=client_creds)
    # We exchange the authorization code with a token
    user_creds.from_code(authorization_code)

    # We persist the user credentials in our in-memory database
    CLIENT_DATA["user_creds"] = user_creds

    return redirect(url_for("show_user_home"))


@app.route("/refresh_token")
def refresh_token():

    CLIENT_DATA["user_creds"].refresh_access_token()
    return redirect(url_for("show_user_home"))


# Logged in user's home page
@app.route("/user_home")
def show_user_home():

    user_creds = CLIENT_DATA["user_creds"]

    api_client = DataAPI(credentials=user_creds)
    accounts = api_client.accounts()
    CLIENT_DATA["accounts"] = accounts

    first_account = accounts[0]
    provider_id = first_account.provider.provider_id
    provider_name = first_account.provider.display_name

    CLIENT_DATA["provider_data"] = {
        "providername": provider_name,
        "providerid": provider_id,
    }

    return render_template(
        "user_home.html",
        client_data_provider=CLIENT_DATA["provider_data"],
        client_data_token=user_creds,
        accounts=accounts,
    )

# Show account transactions
@app.route("/show_transactions", methods=["GET"])
def show_transactions():
    account_id = request.args.get("accountId")

    transactions = Account.transactions(CLIENT_DATA["user_creds"], account_id)
    account = [
        account
        for account in CLIENT_DATA["accounts"]
        if account.account_id == account_id
    ][0]

    return render_template(
        "transactions.html", account=account, transactions=transactions
    )
