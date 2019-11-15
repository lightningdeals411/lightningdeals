import urllib.request
import re
import smtplib
from datetime import datetime
from multiprocessing import Process
import time

email_sent = False
freq = 1800.0
end_process = False

# datetime(year, month, day, hour, minute, second, microsecond)
######## Start Values ############
start_year = 2019
start_month = 11
start_day = 5

start_hour = 11
start_minute = 25
##################################

########## End Values ############
end_year = 2019
end_month = 11
end_day = 5

end_hour = 17
end_minute = 25
##################################

start_datetime = datetime(start_year, start_month, start_day, start_hour, start_minute, 0, 0)
end_datetime = datetime(end_year, end_month, end_day, end_hour, end_minute, 0, 0)


def send_email():
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("lightningdeals411@gmail.com", "amazon$1")

    # message to be sent
    message = "Update amount in lightning deal"

    # sending the mail
    s.sendmail("lightningdeals411@gmail.com", "karrbello@gmail.com", message)

    print('Email sent to update lightning deal')

    # terminating the session
    s.quit()


def get_percentage():
    # URL
    url = "https://www.amazon.com/InstaNatural-Hyaluronic-Ingredients-Advanced-Moisturizer/dp/B00K2O3NV2/ref=sr_1_2?keywords=InstaNatural+-+Hyaluronic+Acid+Serum+-+With+Vitamin+C%2C&qid=1572971774&sr=8-2"
    tag = 'dealStatusPercentage'

    # Request website
    fp = urllib.request.urlopen(url)

    web_bytes = fp.read()
    html_str = web_bytes.decode("utf8")

    # Close request
    fp.close()

    # Create text file with HTML
    file = open('html.txt', 'w', encoding='utf8')
    file.write(html_str)
    file.close()

    # Read file and separate lines
    read_file = open('html.txt', 'r', encoding='utf8')
    content = [line.strip() for line in read_file]
    read_file.close()

    # Get line that contains percentage claimed
    percentage_line = ''
    for html_line in content:
        if tag in html_line:
            percentage_line = html_line

    percentage_list = re.compile('<span[^>]*>([^<]+)</span>').split(percentage_line)
    percentage = percentage_list[1].replace('%', '') if len(percentage_list) >= 2 else ''

    print('Current lightning deal percentage at: ' + percentage + '%\n')
    return percentage


def start_process():
    global end_process
    global email_sent
    global freq

    while not end_process:
        print('Attempting to check percentage at: ' + str(datetime.now()))
        if datetime.now() < start_datetime:
            wait_seconds = (start_datetime - datetime.now()).total_seconds()
            print('Deal has not started. It will start in: ' + str(wait_seconds) + '\n')
            time.sleep(wait_seconds + 300) # 5 minutes extra
        else:
            if datetime.now() >= end_datetime:
                end_process = True
                print('Ending process...\n')
            else:
                p_str = get_percentage()
                p = 0

                if not p_str:
                    print("PROGRAM IS NOT GETTING A PERCENTAGE. CHECK WEBSITE.\n")
                else:
                    p = int(p_str)

                if p < 70:
                    email_sent = False
                    time.sleep(freq)
                else:
                    if p < 80:
                        freq = 600.0
                        print('Updating frequency...\n')
                        time.sleep(freq)
                    else:
                        if not email_sent:
                            freq = 1800.0
                            email_sent = True
                            print('Begin sending email function.\n')
                            send_email()
                        time.sleep(freq)


if __name__ == "__main__":

    print('STARTING PROGRAM\n\n')
    p = Process(target=start_process())
    p.start()

