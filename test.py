import requests

result = requests.post('https://littleshort.vercel.app/api/link',json={"origin":'https://www.w3schools.com/python/ref_requests_post.asp'})

print(result.json()['data'])