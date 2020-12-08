from sseclient import SSEClient

auth = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIxZjJlZGVmYWJiYTY0ZjAxOTc4YmM4YWI3ZWFmZjQzZSIsImlhdCI6MTU2ODY0OTExMiwiZXhwIjoxODg0MDA5MTEyfQ.XLFUZQD6BJAQpydjoSkvke8vhpQZ40mAS6YyAnISNOQ'}
messages = SSEClient('http://localhost:8123/api/stream', headers=auth)

for msg in messages:
    print(msg)
