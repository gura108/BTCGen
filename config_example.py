bot_token = ''
owner_id = 0

dictionary_url = 'https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt'
balance_url = 'https://blockchain.coinmarketcap.com/api/address?address={address}&symbol=BTC&start=1&limit=0'

save_empty = True
total_count = 0
wet_count = 0
dry_count = 0

results_path = 'results'

dry_filename = '{results_path}/dry.txt'.format(results_path=results_path)
wet_filename = '{results_path}/wet.txt'.format(results_path=results_path)

help_text = """
This program was made by Aryn.
It generates Bitcoin by searching multiple possible
wallet combinations until it's finds one with over 0 BTC.

Contacts:
@aryn_bots (Telegram)
"""

proxy_text = 'Enter proxy (http): '
threads_text = 'Number of threads: '
save_text = 'Save empty? (y/n): '

output_text_format = 'Address: {address} | Balance: {balance}'
output_full_text_format = '{text} | Seed phrase: {seed} | Private WIF: {private_key}'

#title_text_format = 'Total: {total_count} - Found: {wet_count} - Empty: {dry_count}\a'
