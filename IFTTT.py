import requests
ifttt_webhook_url = 'https://maker.ifttt.com/trigger/webhook/with/key/jOM9YJKcNZ01TBEKU0h0-VveSjP4E95_Nr7_IV-Mdsu'

post = requests.post(ifttt_webhook_url)
print(post.text)
