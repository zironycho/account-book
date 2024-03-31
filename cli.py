# -*- coding: utf-8 -*-
import yaml
import click
from trello import TrelloClient
import accountbook
import requests

class TrelloSession(requests.Session):
    def request(self, method, url, **kwargs):
        if method == 'GET':
            kwargs = {**kwargs, 'data': None}
        return super().request(method, url, **kwargs)


@click.command()
@click.option('--config_file', default='.acbook.yaml', help='path for config file')
def report(config_file):
    with open(config_file) as f:
        acbook_config = yaml.load(f.read())

    try:
        client = TrelloClient(
            api_key=acbook_config['trello']['api_key'],
            api_secret=acbook_config['trello']['api_secret'],
            token=acbook_config['trello']['oauth_token'],
            token_secret=acbook_config['trello']['oauth_token_secret'],
            http_service=TrelloSession())
    except Exception as e:
        print(e)
        return

    # boards = client.list_boards('open')
    boards = client.list_boards('open')

    selected_board = None
    for board in boards:
        if board.name == acbook_config['trello']['board_name']:
            selected_board = client.get_board(board.id)

    if not selected_board:
        print('You don\'t have this board: \'{}\''.format(acbook_config['trello']['board_name']))
        print('Here is the your board list:')
        for board in boards:
            print(board)
        return

    print('Lists: ')
    try:
        open_lists = selected_board.open_lists()
        for item in open_lists:
            print(item.name)
    except:
        print('There is no list')
        return

    list_name = input('\n\nPlease type one of item: ')
    try:
        found = next(filter(lambda x: x.name == list_name, open_lists))
        accountbook.report_outcomes(selected_board, found)
    except Exception as e:
        print('could not find item about: {}'.format(list_name))
        print(e)
        return


if __name__ == '__main__':
    report()
