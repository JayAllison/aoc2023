import getpass
# import pprint
import os
import json
import requests
cache_filename = '.giftcard_cache'

cached_data = {}
if os.path.exists(cache_filename):
    cached_data = json.load(open(cache_filename))

if 'session_id' not in cached_data:
    # ask the user for an authenticated session ID, rather than hardcoding it or building auth workflow here
    print('\nPlease log in via https://www.adventofcode.com/ then paste the authenticated Session ID here.\n')
    cached_data['session_id'] = getpass.getpass('Advent of Code Session ID: ')
    print()

    json.dump(cached_data, open(cache_filename, 'w'))

giftcard_star_threshold = 25
leaderboard_url = 'https://adventofcode.com/2023/leaderboard/private/view/210077.json'

# use the session ID to get the data from the specified leaderboard
leaderboard_response = requests.get(leaderboard_url, headers={'Cookie': f'session={cached_data['session_id']};'})

try:
    leaderboard_response.raise_for_status()
except requests.HTTPError:
    print(f'URL request failed with {leaderboard_response.status_code}: {leaderboard_response.reason}')
    exit(-1)

try:
    leaderboard = leaderboard_response.json()
except requests.exceptions.JSONDecodeError:
    print('Valid response does not contain JSON body - perhaps not logged in?')
    exit(-1)

# see which users have crossed the threshold
gift_card_earners = {}
for member_id in leaderboard['members']:
    star_count = leaderboard['members'][member_id]['stars']
    if star_count >= 25:
        gift_card_earners[leaderboard['members'][member_id]['name']] = star_count

print('Gift Card Earners (alphabetical order):')
print('--------------------------------------')
print()

# sort output by star count high to low, then alphabetically by name
count = 0
for star_counts in sorted(set(gift_card_earners.values()), reverse=True):
    for earner in sorted(gift_card_earners.keys()):
        if star_counts == gift_card_earners[earner]:
            print(f'{earner}: {gift_card_earners[earner]}')
            count += 1

print(f'\nTotal qualifiers: {count}')
