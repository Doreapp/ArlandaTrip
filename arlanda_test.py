import arlanda

import datetime

def test_api_date():
    print("Test API date (api_date)")
    print(arlanda.api_date(datetime.datetime.now()))

def test_api_call():
    print("Test API Call (api_call)")
    arlanda.api_call(
        arlanda.API_KEY,
        arlanda.ids["Odenplan"],
        arlanda.ids["Märsta"],
        arlanda.api_date(datetime.datetime.now()),
        '19:00'
    )

if __name__ == '__main__':
    print("Testing...")
    test_api_date()
    test_api_call()