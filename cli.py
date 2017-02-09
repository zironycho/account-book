# -*- coding: utf-8 -*-
import yaml
import click
from trello.trelloclient import TrelloClient
import accountbook


@click.command()
@click.option('--config_file', default='.acbook.yaml', help='path for config file')
def report(config_file):
    with open(config_file) as f:
        acbook_config = yaml.load(f.read())

    client = TrelloClient(acbook_config['trello']['api_key'],
                          token=acbook_config['trello']['token'])

    boards = client.list_boards('open')
    selected_board = None
    for board in boards:
        if board.name == acbook_config['trello']['board_name']:
            selected_board = client.get_board(board.id)

    found = False
    while not found:
        print('Lists: ')
        for item in selected_board.open_lists():
            print(item.name)

        list_name = input('\n\nPlease type one of item: ')
        found = next(filter(lambda x: x.name == list_name, selected_board.open_lists()))
        accountbook.report_outcomes(selected_board, found)


if __name__ == '__main__':
    report()
