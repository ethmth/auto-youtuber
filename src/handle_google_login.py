import time
import requests
import datetime
from requests.structures import CaseInsensitiveDict


def log_action(message):
    iFile = open("/opt/src/current_values.var", "r")
    lines = iFile.readlines()
    iFile.close()

    for line in lines:
        if line[0:line.index("=")] == "START_DATE":
            start_date = line[(line.index("=") + 2):(line.index("\n") - 1)]

    oFile = open(f"/opt/shared/{start_date}.log", "a")
    oFile.write(message + "\n")
    oFile.close()


def handle_url(login_url):

    print("The login url is ", login_url)

    return

    ifile = open("/opt/src/current_values.var", "r")
    lines = ifile.readlines()
    ifile.close()

    for line in lines:
        if line[0:line.index("=")] == "IFTTT_KEY":
            ifttt_key = line[(line.index("=") + 2):(line.index("\n") - 1)]
        if line[0:line.index("=")] == "IFTTT_EVENT":
            ifttt_event = line[(line.index("=") + 2):(line.index("\n") - 1)]

    ifttt_url = f"https://maker.ifttt.com/trigger/{ifttt_event}/json/with/key/{ifttt_key}"

    log_action(str(datetime.datetime.now()) + " handle_url IFTTT URL: " + ifttt_url)
    log_action(str(datetime.datetime.now()) + " handle_url Login URL: " + login_url)

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"

    data = f"""
    {{
        "Sign-In URL": "{login_url}"
    }}
    """

    log_action(str(datetime.datetime.now()) + " handle_google_login Sending IFTTT request for URL Now")

    resp = requests.post(ifttt_url, headers=headers, data=data)
    print(resp.status_code)


def get_url():
    time.sleep(1)

    sign_in_url_found = False
    while sign_in_url_found == False:

        f = open("/opt/src/pyout.txt", "r")
        lines = f.readlines()
        f.close()

        for line in lines:
            if "https://accounts.google.com/o/oauth2/" in line:
                login_url = line[line.index("https://accounts.google.com/o/oauth2/"):line.index("\n")]
                sign_in_url_found = True

        if sign_in_url_found == True:
            handle_url(login_url)
        if sign_in_url_found == False:
            time.sleep(5)

