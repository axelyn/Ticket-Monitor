from bs4 import BeautifulSoup
from urllib.request import urlopen
import datetime
import threading
import time
import sys
import smtplib
from getpass import getpass
from email.mime.text import MIMEText
import gc


def find(url, start, end, sender, password, receiver):

    found = False
    found_times = ''

    try:
        while ~found:
            s = datetime.datetime.strptime(start, '%m/%d/%Y').date()
            e = datetime.datetime.strptime(end, '%m/%d/%Y').date()
            e += datetime.timedelta(days=1)

            if s > e:
                sys.exit()

            while s < e:

                page = urlopen(url + str(s).replace('-', '/'))
                page_content = page.read()
                page.close()

                soup = BeautifulSoup(page_content, 'html.parser')
                times = soup.body.find_all('ul', attrs={'class': 'showtime--list'})

                each_time = []
                for i in times:
                    each_time.append(i.find_all('li'))

                for show in each_time:
                    for show_time in show:
                        if not show_time.find('span', attrs={'class': 'qt-sold-out'}):
                            found = True
                            found_times += str(s.strftime('%m/%d/%Y')) + ': ' + show_time.find(
                                'a', attrs={'data-tooltip': 'true'}).get_text().strip() + '\n'

                del times[:]
                del times
                del each_time[:]
                del each_time

                soup.decompose()
                gc.collect()
                s += datetime.timedelta(days=1)
                time.sleep(2)

            if found:
                msg = MIMEText(found_times)
                msg['From'] = sender
                msg['To'] = receiver
                msg['Subject'] = 'Movie Tickets Available'

                smtp_server_name = 'smtp.gmail.com'
                port = '587'

                if port == '465':
                    server = smtplib.SMTP_SSL('{}:{}'.format(smtp_server_name, port))
                else:
                    server = smtplib.SMTP('{}:{}'.format(smtp_server_name, port))
                    server.starttls()  # this is for secure reason

                server.login(sender, password)
                server.send_message(msg)
                server.quit()
                print(found_times)
                sys.exit()

            time.sleep(300)

    except KeyboardInterrupt:
        sys.exit()
    except smtplib.SMTPAuthenticationError as e:
        print(e)
        sys.exit()


if __name__ == "__main__":

    try:
        url = input("URL with MM/DD/YYYY removed from end: ")
        start = input("Start date: ").strip()
        end = input("End date: ").strip()

        sender = input("Sender Email: ")
        password = getpass("Sender Password: ").strip()
        receiver = input("Receiver Email: ")

        t = threading.Thread(target=find(url, start, end, sender, password, receiver))
        t.daemon = True
        t.start()

    except KeyboardInterrupt:
        print()
