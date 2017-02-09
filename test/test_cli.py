# -*- coding: utf-8 -*-
import json
import yaml
import mock
import unittest

from trello.trelloclient import TrelloClient
from accountbook import report_outcomes
from accountbook.money import get_currency
from cli import report
from click.testing import CliRunner


class TestCli(unittest.TestCase):
    def setUp(self):
        with open('.acbook.yaml') as f:
            test_config = yaml.load(f.read())

        client = TrelloClient(api_key=test_config['trello']['api_key'],
                              token=test_config['trello']['token'])

        self.board = client.add_board(test_config['trello']['board_name'])
        self.report_list = self.board.add_list('Jan')
        self.member = self.board.get_members('owner')[0]
        self.total = 0

        with open('./test/samples/card_items.txt', 'rt') as f:
            items = json.loads(f.read())['data']
            for item in items:
                text = item['text']
                self.report_list.add_card(text).assign(self.member.id)
                self.total += int(item['money'] * get_currency(item['locale']))

    def tearDown(self):
        self.board.close()

    def test_report_outcomes(self):
        outcomes = report_outcomes(self.board, self.report_list)
        self.assertEqual(1, len(outcomes))

        one_member_outcome = outcomes.get(self.member.id)
        self.assertIn('member', one_member_outcome)
        self.assertIn('total', one_member_outcome)
        self.assertIn('cards', one_member_outcome)
        self.assertEqual(self.total, one_member_outcome['total'])

    def test_cli(self):
        with mock.patch('builtins.input', return_value='Jan'):
            runner = CliRunner()
            result = runner.invoke(report, args=('--config_file=.acbook.yaml',))
            print(result.output)
            self.assertFalse(result.exception)

    def test_cli_without_config(self):
        with mock.patch('builtins.input', return_value='Jan'):
            runner = CliRunner()
            result = runner.invoke(report)
            print(result.output)
            self.assertFalse(result.exception)
