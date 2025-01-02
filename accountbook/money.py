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

    if 'USD' in text:
        locale = 'USD'
        money_part = text[text.upper().find('USD'):]
    elif 'THB' in text:
        locale = 'THB'
        money_part = text[text.upper().find('THB'):]
    else:
        locale = 'KRW'
        if '우리카드' in text:
            print('우리카드: ' + money_part)
            if 'KRW' in text:
                money_part = text.split('KRW ')[1]
            elif '일시불.승인' not in text:
                money_part = text.split(')')[2]
            elif '[해외승인] USD' in text:
                money_part = text.split('USD ')[1]
        elif '우리(' in text:
            money_part = text.split(')')[1]
        elif '신한카드' in text:
            money_part = text.split(')')[1]
        elif '씨티카드' in text:
            money_part = text.split('일시불')[1]
        elif '현대카드' in text:
            if '해외승인' in text:
                r = re.findall(r'AUD (\d[\d,\.]*)', text)
                money_part = r[0]
                locale = 'AUD'
            else:
                r = re.findall(r'([\d]*\/[\d]* [\d]*:[\d]*)[\s]+(\d[\d,\.]*)원', text)
                money_part = r[0][1]
        elif '롯데' in text:
            for item in text.split(' ')[4:]:
                if item.endswith('원'):
                    money_part = item
                    break

    money = re.findall(r'-*\d[\d,\.]*', money_part)[0]
    money = money.replace(',', '')
    return float(money), get_currency(locale)


def get_currency(locale):
    if locale.upper() == "USD":
        return 1460
    elif locale.upper() == "KRW":
        return 1
    elif locale.upper() == "THB":
        return 33
    elif locale.upper() == "AUD":
        return 912
    raise Exception('cannot support currency: {}'.format(locale))
