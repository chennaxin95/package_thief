from twilio.rest import Client
 
account_sid = 'AC59f219f50e0c807bbef4a098e80cb22f'
auth_token = '25628f4df2124f081c048d95e9e1d98a'
client = Client(account_sid, auth_token)
 
call = client.messages.create(from_='+12062033943',
                       to='+12064278603',
                       body='Ahoy from Twilio!')

print(call.sid)