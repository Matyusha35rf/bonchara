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
            id_group = re.search(r'\d+', a.attributes["href"] if "href" in a.attributes else '').group()
            group = a.text().strip()
            if not id_group or not id_group.isdigit():
                id_group = None
            if not group:
                group = None
            list_groups.append(Group(id_group, group))
    return list_groups


def find_id_by_name(name_group):
    from data.database import connect
    con,cur = connect()
    group_id = cur.execute('''SELECT group_id FROM groups WHERE group_name=?''', (name_group,)).fetchone()
    if group_id:
        return group_id[0]
    return None


def get_matched_groups():
    return parse_group()


def write_db():
    from data.database import connect
    con, cur = connect()
    list_groups = get_matched_groups()
    for group in list_groups:
        cur.execute('''INSERT OR IGNORE INTO groups (group_name, group_id) VALUES (?,?)''',(group.group, group.id))
    con.commit()
    con.close()


if __name__ == '__main__':
    lst = get_matched_groups()
    group = find_id_by_name('ИСТ-341')
    write_db()
    print(group)
