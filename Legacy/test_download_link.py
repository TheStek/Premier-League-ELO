import urllib.request

with open("test_download_link.txt", 'r') as file:
	link = file.read()
	# print(link)


urllib.request.urlretrieve(link, "test.xls")