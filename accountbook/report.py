# -*- coding: utf-8 -*-
import humanize
from accountbook.money import get_money


def report_outcomes(board, selected_list):
    grouped_cards = _grouping_cards_by_member(selected_list)

    members = board.get_members()
    for k, v in grouped_cards.items():
        total = 0
        member = next(filter(lambda x: x.id == k, members))

        print('\n{}'.format(member.username))
        for card in v['cards']:
            text = card.name
            money = get_money(text)
            if not money:
                print('[err] Cannot parse this: {}'.format(text))
                exit()
            total += int(money)
            print('[{}]: {}'.format(humanize.intcomma(money), text))

        grouped_cards[k]['member'] = member
        grouped_cards[k]['total'] = total

    print('\n')
    for value in grouped_cards.values():
        print('{}, {}'.format(value['member'].username, humanize.intcomma(value['total'])))

    return grouped_cards


def _grouping_cards_by_member(selected_list):
    cluster = dict()
    for card in selected_list.list_cards():
        if 1 != len(card.member_ids):
            raise Exception('[err] Please assign only one member in card: {}'.format(card.name))
        member_id = card.member_ids[0]
        if member_id not in cluster:
            cluster[member_id] = {'cards': []}

        cluster[member_id]['cards'].append(card)
    return cluster
