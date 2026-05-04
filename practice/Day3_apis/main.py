#api call
# import requests
# url = "https://jsonplaceholder.typicode.com/users"
# response = requests.get(url)
# print(response)



#api call and json file get
# import requests

# url = "https://jsonplaceholder.typicode.com/users"

# response = requests.get(url)

# data = response.json()

# print(data)




#Json file get and print name of users
# import requests

# url = "https://jsonplaceholder.typicode.com/users"

# response = requests.get(url)

# users = response.json()

# for user in users:
#     print(user["name"])



#error handling
# import requests

# url = "https://jsonplaceholder.typicode.com/users"

# response = requests.get(url)

# if response.status_code == 200:
#     print("Success")
# else:
#     print("Error")




#try except block for error handling
# import requests
# url = "https://jsonplaceholder.typicode.com/users"
# try:
#     response = requests.get(url)

#     response.raise_for_status()

#     data = response.json()

#     print(data)

# except requests.exceptions.RequestException as e:
#     print("API Error:", e)



#mini task of printing name, email and city of users
# import requests

# url = "https://jsonplaceholder.typicode.com/users"

# response = requests.get(url)

# users = response.json()

# for user in users:
#     print(user["name"], user["email"], user["address"]["city"])