# -*- coding: utf-8 -*-
import json
import unittest

from accountbook.money import get_currency, get_money


class TestMoney(unittest.TestCase):

    def test_currency_success(self):
        self.assertEqual(1460, get_currency('USD'))
        self.assertEqual(1, get_currency('KRW'))
        self.assertEqual(912, get_currency('AUD'))

    def test_currency_fail(self):
        self.assertRaises(Exception, get_currency, 'CN')

    def test_get_money(self):
        with open('./test/samples/card_items.json', 'rt') as f:
            items = json.loads(f.read())['data']
            for item in items:
                money = get_money(item['text'])
                self.assertEqual(int(item['money'] * get_currency(item['locale'])), money)
