import requests
import hashlib


def get_data(query_string):
    url = 'https://api.pwnedpasswords.com/range/' + query_string            # a dynamic request to api, need to pass the fist 5 letters of the sha1 generated hash of the entered string
    res = requests.get(url)
    if res.status_code != 200:
        print(f'Error fetching: {res.status_code}, check API and try again')
    return res


def get_pass_leaks(hashes, hashes_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hashes_to_check:
            return count
    return 0


def check_pwned_password(password):
    sha1pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()   # hash generation
    first5_char, tail = sha1pass[:5], sha1pass[5:]
    response = get_data(first5_char)
    return get_pass_leaks(response, tail)


user_pass = input("Enter the password you need to check: ")
times = check_pwned_password(user_pass)
if times:
    print(f'{user_pass} has been hacked {times} times. You probably need to change the password')
else:
    print(f'You are safe! {user_pass} has not yet been hacked.')
