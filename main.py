from moneywagon import generate_keypair
from requests import get, exceptions
from random import choice
from os import path, makedirs
from sys import exit
from decimal import Decimal
from threading import Thread
from termcolor import colored
from config import *
from telebot import TeleBot

#from os import name as sys_name

#if sys_name == 'nt':
    #from ctypes import windll


bot = TeleBot(bot_token)


timeout = 5

dictionary = get(dictionary_url).text.strip().split('\n')


def get_balance(address, proxy=None):
    proxies = None

    if proxy:
        proxies = {'http': proxy}

    try:
        url = balance_url.format(address=address)
        resp = get(url, timeout=timeout, proxies=proxies)
        return Decimal(resp.json()['balance'])

    except exceptions.ProxyError:
        raise Exception('Прокси не рабочий!')
    except exceptions.ConnectionError:
        raise Exception('Сайт для проверки баланса BTC кошелька недоступен!')
    except exceptions.ReadTimeout:
        raise Exception('Сайт заблокировал за частые запросы!')
    except Exception as e:
        raise Exception(f"Неизвестная ошибка: {type(e)} - {e}!")

def generate_seed():
    return ''.join(choice(dictionary) if i == 0 else ' ' + choice(dictionary) for i in range(12))

def check(proxy=None):
    global total_count, wet_count, dry_count

    while True:
        try:
            seed = generate_seed()

            data = generate_keypair('btc', seed)

            private_key = data['private']['wif']
            address = data['public']['address']

            balance = get_balance(address, proxy)

            text = output_text_format.format(address=address, balance=balance)
            full_text = output_full_text_format.format(text=text, seed=seed, private_key=private_key)

            #title_text = title_text_format.format(total_count=total_count, wet_count=wet_count, dry_count=dry_count)

            #print(title_text)

            #if sys_name == 'nt':
                #windll.kernel32.SetConsoleTitleW(title_text)
            #else:
                #execute('start {text}'.format(text=title_text))
                #print('\33]0;{text}\a'.format(text=title_text), end='', flush=True)
                #print('\x1b]2;{text}\x07'.format(text=title_text), end='', flush=True)

            if balance > 0:
                bot.send_message(owner_id, full_text)
                print(colored(text, 'green'))

                wet_count += 1
                wet_file.write(f"{full_text}\n")

            else:
                print(text)

                dry_count += 1

                if save_empty:
                    dry_file.write(f"{full_text}\n")

            total_count += 1

        except Exception as e:
            print(e)


if __name__ == '__main__':
    print(help_text)
    print()

    if not path.exists(results_path):
        makedirs(results_path)

    proxy = input(proxy_text) or None

    threads = int(input(threads_text))

    save_empty = False if input(save_text).lower() in ['no', 'n'] else True

    dry_file = open(dry_filename, 'a')
    wet_file = open(wet_filename, 'a')

    print('\n')

    for _ in range(threads):
        Thread(target=check, args=(proxy,)).start()

    while True:
        try:
            pass
        except:
            exit(0)
