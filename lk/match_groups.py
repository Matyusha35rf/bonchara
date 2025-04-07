import re

from selectolax.parser import HTMLParser
from lk.lk_func import connect


class Group:
    def __init__(self, id_group, group):
        self.id = id_group
        self.group = group

    def __str__(self):
        return f'{self.group} — {self.id}'

    def __repr__(self):
        return f'{self.group} — {self.id}'


def parse_group():
    html = connect(
        'https://www.sut.ru/studentu/raspisanie/raspisanie-zanyatiy-studentov-ochnoy-i-vecherney-form-obucheniya')
    tree = HTMLParser(html)
    group_blocks = tree.css('.vt255')
    list_groups = []
    for i in group_blocks:
        for a in i.css("a"):
            id_group = re.search(r'\d+',a.attributes["href"] if "href" in a.attributes else '').group()
            group = a.text().strip()
            if not id_group or not id_group.isdigit():
                id_group = None
            if not group:
                group = None
            list_groups.append(Group(id_group, group))
    return list_groups

def find_id_by_name(name_group):
    html = connect(
        'https://www.sut.ru/studentu/raspisanie/raspisanie-zanyatiy-studentov-ochnoy-i-vecherney-form-obucheniya')
    tree = HTMLParser(html)
    group_blocks = tree.css('.vt255')
    list_groups = []
    for i in group_blocks:
        for a in i.css("a"):
            group = a.text().strip()
            if group == name_group:
                id_group = re.search(r'\d+',a.attributes["href"] if "href" in a.attributes else '').group()
                if not id_group or not id_group.isdigit():
                    return None
                return id_group
    return None

def get_matched_groups():
    list_groups = parse_group()
    return list_groups


if __name__ == '__main__':
    lst = get_matched_groups()
