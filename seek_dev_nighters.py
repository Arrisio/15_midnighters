import requests
import pytz
from datetime import datetime


def is_midnighter(
        user_timestamp, user_timezone, midnight_start=0, midnight_end=6
):
    user_localized_time = datetime.fromtimestamp(
        user_timestamp,
        tz=pytz.timezone(user_timezone)
    )
    return midnight_start <= user_localized_time.hour <= midnight_end


def load_attempts(url='http://devman.org/api/challenges/solution_attempts/'):
    params = {'page': 0}

    while True:
        params['page'] += 1
        response = requests.get(url, params=params)
        if response.ok:
            for attempt in response.json().get('records'):
                yield attempt
        else:
            return


def get_midnighters():
    return set(attemp.get('username') for attemp in load_attempts()
               if is_midnighter(
                    user_timestamp=attemp.get('timestamp'),
                    user_timezone=attemp.get('timezone'))
               )


def print_midnighters(midnighters_list):
    if midnighters_list and len(midnighters_list) > 0:
        print('Devmat midnighters list:')
        for midnighter in midnighters_list:
            print(midnighter)
    else:
        print('No midnighters, everybody sleeps..')


if __name__ == '__main__':
    print_midnighters(get_midnighters())
