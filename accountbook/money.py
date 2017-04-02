# -*- coding: utf-8 -*-
import re


def get_money(text):
    try:
        money, currency = _get_money_part(text)
        return int(currency * money)
    except Exception:
        print('cannot parsing money part: {}'.format(text))


def _get_money_part(text):
    money_part = text

    if 'USD ' in text:
        locale = 'USD'
        money_part = text[text.upper().find('USD'):]
    elif 'THB ' in text:
        locale = 'THB'
        money_part = text[text.upper().find('THB'):]
    else:
        locale = 'KR'
        if '우리카드' in text:
            if '일시불.승인' not in text:
                money_part = text.split(')')[2]
        elif '신한카드' in text:
            money_part = text.split(')')[2]
        elif '씨티카드' in text:
            money_part = text.split('일시불')[1]

    money = re.findall(r'\d[\d,\.]*', money_part)[0]
    money = money.replace(',', '')
    return float(money), get_currency(locale)


def get_currency(locale):
    if locale.upper() == "USD":
        return 1200
    elif locale.upper() == "KR":
        return 1
    elif locale.upper() == "THB":
        return 33
    raise Exception('cannot support currency: {}'.format(locale))
