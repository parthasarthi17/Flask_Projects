import requests

BASE = "http://127.0.0.1:5000/"

data = [{"name":"usahdsad", "likes":1331, "views":48967534056},
        {"name":"vd12", "likes":3232, "views":213133},
        {"name":"asdasd", "likes":12121, "views":213213},
        ]


for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

#response = requests.put(BASE + "video/", {"name":"sdsd", "likes":10, "views":12})

input()
response = requests.get(BASE + "video/2" )
print(response.json())
#print(response.json())
