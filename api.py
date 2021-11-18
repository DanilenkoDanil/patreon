import requests
import json

access_token = 'QMrmtp3ILTItXoJ5gGeLT8bnDS4hbNrfC5I_umIiltU'


def get_active_list():
    email_list = {500: [], 600: []}
    url = "https://www.patreon.com/api/oauth2/v2/campaigns/7328812/members?include=currently_entitled_tiers,address&fields[member]=full_name,email,is_follower,last_charge_date,last_charge_status,patron_status,will_pay_amount_cents"
    headers = {"authorization": f"Bearer {access_token}"}
    result = requests.get(url, headers=headers)
    users_list = json.loads(result.content)['data']
    # print(result.content)
    for i in users_list:
        if i['attributes']['patron_status'] == 'active_patron':
            if int(i['attributes']['will_pay_amount_cents']) == 2900:
                email_list[500].append(i['attributes']['email'])
            elif int(i['attributes']['will_pay_amount_cents']) == 4900:
                email_list[600].append(i['attributes']['email'])
    # return email_list
    return {500: [], 600: ['av@haus.me']}


# print(get_active_list())
