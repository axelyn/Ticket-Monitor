from urllib.request import urlopen

page = urlopen('https://www.cineplex.com/Showtimes/any-movie/cineplex-cinemas-yongedundas-and-vip?Date=9/17/2019')
page_content = page.read()

file_name = 'test.html'

with open(file_name, 'wb') as f:
    f.write(page_content)
