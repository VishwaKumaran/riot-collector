import asyncio
import json
import re
from typing import List, Callable, Awaitable

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from app.crud.champion import Champion
from app.crud.item import Item
from app.crud.patch import Patch
from app.crud.perks import Perks
from app.crud.shard import Shard
from app.crud.summoner_spell import SummonerSpell
from app.schema.utils import convert_string, remove_spaces


async def get_champ_info(champ_name: str) -> dict:
    data: dict = {}
    page = BeautifulSoup(
        requests.get(f"https://leagueoflegends.fandom.com/wiki/Template:Data_{champ_name}").content
    )
    table = page.find('table', class_='article-table')
    for tr in table.find_all('tr')[1:]:
        if len(tr.find_all('th')) == 1:
            break

        td = tr.find_all('td')
        key = td[0].text.strip()
        value = convert_string(td[1].text.strip())
        if key == 'role':
            value = [v.strip() for v in value.split(',')]
        data[key] = value

    return data


async def get_champ_bio(title: str) -> List[str]:
    data: List[str] = []
    page = BeautifulSoup(
        requests.get(f'https://leagueoflegends.fandom.com/wiki/{title}').content
    )
    bio = page.find('span', id=['Biography', 'Lore'])
    if bio:
        for bio_data in bio.parent.next_siblings:
            if bio_data.name == 'h2':
                break
            elif bio_data.name == 'p':
                data.append(remove_spaces(bio_data.text.strip()))

    return data


async def get_champ_strategy(champ_name: str) -> dict:
    data: dict = {}
    page = BeautifulSoup(
        requests.get(f'https://leagueoflegends.fandom.com/wiki/{champ_name}/Strategy').content
    )
    if page.find('div', class_='noarticletext mw-content-ltr'):
        page = BeautifulSoup(
            requests.get(f'https://leagueoflegends.fandom.com/wiki/{champ_name}/LoL/Strategy').content
        )

    recommended_items = page.find('span', id='Recommended_Items')
    if recommended_items:
        _items: list = []
        for sib in recommended_items.parent.next_siblings:
            if isinstance(sib, Tag):
                if sib.name == 'h2':
                    break
                for i, row_data in enumerate(sib.find_all('tr')):
                    if i == 0:
                        _items.append({
                            'name': row_data.text.strip(),
                            'build': []
                        })
                    else:
                        tds = row_data.find_all('td')
                        _items[-1]['build'].append({
                            'name': tds[0].text.strip(),
                            'items': [{
                                'name': item.get('data-item'), 'number': int(item.text.strip()) if item.text else 1
                            } for item in tds[1].find_all('span', attrs={'data-game': 'lol'})]
                        })

        data['recommended_items'] = _items

    tips = page.find('span', id='Tips')
    if tips:
        row_name: str = ''
        for sib in tips.parent.next_siblings:
            if sib.name == 'h2':
                break
            elif sib.name == 'dl':
                _dl = sib.text.strip().lower()
                row_name = 'ally_tips' if 'as' in _dl else 'enemy_tips' if 'against' in _dl else 'team_mate_tips'
            elif sib.name == 'ul':
                data[row_name] = [
                    remove_spaces(li.text.strip()) for li in sib.find_all('li')
                ]

    tricks = page.find('span', id='Tricks')
    if tricks:
        _tricks: List[dict] = []
        _h3 = tricks.parent.find('h3')
        for sib in tricks.parent.next_siblings:
            if sib.name == 'h2':
                break
            elif sib.name == 'p':
                _tricks.append({
                    "value": [{
                        'text': [remove_spaces(sib.text.strip())]
                    }]
                })
            elif sib.name == 'dl':
                if _h3:
                    _tricks[-1]['value'].append({
                        'title': remove_spaces(sib.text.strip()),
                        'text': []
                    })
                else:
                    _tricks.append({
                        'title': remove_spaces(sib.text.strip()),
                        'value': []
                    })
            elif sib.name == 'h3':
                _tricks.append({
                    'title': remove_spaces(sib.text.strip()),
                    'value': []
                })
            elif sib.name == 'ul':
                if not _tricks:
                    _tricks.append({
                        'value': []
                    })

                for li in sib.find_all('li', recursive=False):
                    sub_ul = li.find('ul')
                    if sub_ul:
                        _tricks[-1]['value'].append({
                            'title': remove_spaces(
                                ' '.join(child.text.strip() for child in li.children if child.name != 'ul')),
                            'text': [remove_spaces(_li.text.strip()) for _li in li.find('ul').find_all('li')]
                        })
                    else:
                        _tricks[-1]['value'].append({
                            "title": remove_spaces(li.text.strip())
                        })

        data['tricks'] = _tricks

    playstyle = page.find('span', id='Playstyle')
    if playstyle:
        _playstyle = []
        for sib in playstyle.parent.next_siblings:
            if sib.name == 'h2':
                break
            elif sib.name == 'p':
                _playstyle.append({
                    'ability_text': [sib.text.strip()]
                })
            elif sib.name == 'dl':
                _playstyle.append({
                    'ability_name': sib.text.strip(),
                    'ability_text': []
                })
            elif sib.name == 'ul':
                if not _playstyle:
                    _playstyle.append({
                        'ability_text': []
                    })
                _playstyle[-1]['ability_text'].extend([li.text.strip() for li in sib.find_all('li')])

        data['playstyle'] = _playstyle

    runes = page.find('span', id='Runes')
    if runes:
        _runes = []
        for sib in runes.parent.next_siblings:
            if sib.name == 'h2':
                break
            elif sib.name == 'p':
                _runes.append({
                    'text': remove_spaces(sib.text.strip())
                })
            elif sib.name == 'ul':
                for li in sib.find_all('li', recursive=False):
                    keystone = None
                    perk = li.text.strip()

                    if "Paths" in perk:
                        ul = li.find('ul')
                        for _li in ul.find_all('li', recursive=False):
                            keystone = None
                            _ul = _li.find('ul')
                            if _ul:
                                keystone = [l.text.strip() for l in _ul.find_all('li')]
                                _ul.decompose()
                            _runes.append({
                                'perks': _li.text.strip(),
                                'keystone': keystone
                            })
                    else:
                        ul = li.find('ul')
                        if ul:
                            keystone = [l.text.strip() for l in ul.find_all('li')]
                            ul.decompose()
                        _runes.append({
                            'perks': li.text.strip(),
                            'keystone': keystone
                        })

        data['runes'] = _runes

    items = page.find('span', id='Items')
    if items:
        _items = []
        for sib in items.parent.next_siblings:
            if sib.name == 'h2':
                break
            elif sib.name == 'p':
                _items.append(sib.text.strip())
            elif sib.name == 'ul':
                for li in sib.find_all('li', recursive=False):
                    ul = li.find('ul')
                    if ul:
                        for l in ul.find_all('li'):
                            _items.append(l.text.strip())
                        ul.decompose()
                    _items.append(li.text.strip())

        data['items'] = _items

    return data


async def get_champ_skins() -> dict:
    page = BeautifulSoup(
        requests.get('https://leagueoflegends.fandom.com/wiki/Module:SkinData/data').content
    )
    code_text = page.find('pre', class_='mw-code mw-script', dir='ltr').get_text()
    code_text = re.sub(r'-- <pre>', '', code_text)
    code_text = re.sub(r'return\s*', '', code_text)
    code_text = re.sub(r'\["', '"', code_text)
    code_text = re.sub(r'"]', '"', code_text)
    code_text = re.sub(r'=', ':', code_text)
    code_text = re.sub(r'\{"', '["', code_text)
    code_text = re.sub(r'"}', '"]', code_text)
    code_text = re.sub(r'nil', 'null', code_text)
    code_text = re.sub(r',\s*([]}])', r'\1', code_text)
    code_text = re.sub(r',\s*--.*$', ',', code_text, flags=re.MULTILINE)
    code_text = re.sub(r'--\s</pre>.*$', '', code_text, flags=re.DOTALL)
    code_text = code_text.strip()

    return json.loads(code_text)


async def get_champ_stats(champ_name: str) -> dict:
    data: dict = {}
    page = BeautifulSoup(
        requests.get(f'https://leagueoflegends.fandom.com/wiki/Template:Data_{champ_name}').content
    )
    table_title = page.find('table', class_='article-table').find_all(
        "th", colspan=3, string=lambda text: text.strip() in ['Stats', 'Special Stats']
    )

    for title in table_title:
        row = title.parent

        while True:
            row = row.find_next_sibling('tr')
            row_data = row.find_all('td')
            if not row_data:
                break
            value = row_data[1].text.strip()
            data[row_data[0].text.strip()] = float(value) if value else None

    return data


def get_champ_spell(champ_name: str, spell_name: str) -> dict:
    data: dict = {}
    _spell_name: str = spell_name.replace(' ', '_')

    try:
        page = BeautifulSoup(
            requests.get(f"https://leagueoflegends.fandom.com/wiki/Template:Data_{champ_name}/{_spell_name}").content
        )
        ability = page.find('div', class_='ability-info-container').find_all('div', recursive=False)

        for stat in ability[0].find('section', attrs={'data-item-name': 'champion-ability-params'}).find_all(
                'div', class_='pi-item pi-data pi-item-spacing pi-border-color'
        ):
            value = stat.find('div').text.strip()
            value = re.sub(r'TO', '-', value)
            value = re.sub(r'[A-Za-z]', '', value)
            value = re.sub(r'\'', '', value)
            value = re.sub(r'\u00B0', '', value)
            value = re.sub(r'\(.*', '', value)
            value = re.sub(r'\*', '', value)
            value = re.sub(r'º', '', value)
            value = re.sub(r'%.*', '', value)
            value = value.strip()
            if '−' in value or '-' in value:
                span_split = value.replace('/', "")
                for _span in stat.find('div').find_all('span'):
                    _value = _span.get('data-bot_values')
                    if _value is not None:
                        span_split = _value
                        break

                value = [convert_string(_.strip()) for _ in span_split.split(';' if ';' in span_split else '-')]
            elif '/' in value:
                value = [convert_string(_.strip()) for _ in value.split('/')]
            else:
                value = convert_string(value)
            data[
                stat.find('h3').text.strip().lower().replace(':', '').replace(' ', '_')
            ] = value

        for stat in ability[1].find_all('dl'):
            value = stat.find('dd')

            _value = value.find('span').get('data-bot_values')
            if _value is not None:
                value = _value.split(';')

            value = re.sub(r'%.*', '', value.text.strip())
            value = re.sub(r'\(.*', '', value)
            value = re.sub(r'[A-Za-z]', '', value)
            value = re.sub(r'\u00B0', '', value)
            value = re.sub(r'º', '', value)
            value = value.strip()

            sep = '/' if '/' in value else '-' if '-' else None

            data[
                stat.find('dt').text.strip().lower().replace(":", "").replace(' ', '_')
            ] = [convert_string(_.strip()) for _ in value.split(sep)] if sep is not None else convert_string(value)

        data["explanation"] = []
        for stat in ability[1].find_all('p'):
            data['explanation'].append(stat.text.strip().replace('  ', ' ').strip())
    except Exception:
        pass

    return data


async def get_champ_data(version: str) -> List[dict]:
    data: dict = {}

    dragon = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{version}.1/data/en_US/championFull.json").json()
    skins = await get_champ_skins()

    for champ in dragon['data'].values():
        champ_id = champ.get('key')
        champ_name = champ.get('name')
        champ_skins = {
            name: {
                "cost": skin['cost'],
                "release_date": skin["release"],
                "voice_actor": skin.get('voiceactor'),
                "splash_artist": skin.get("splashartist"),
                "lore": skin.get('lore')
            } for name, skin in skins.get(champ_name, {}).get('skins', {}).items()
        }
        champ_info = await get_champ_info(champ_name)
        champ_strategy = await get_champ_strategy(champ_name)
        champ_bio = await get_champ_bio(champ_info['title'])
        _champ_info = {
            **{k: champ_info[v] for k, v in KEYS.items()},
            "tactical": {k: champ_info[v] for k, v in TACTICAL.items()},
            **champ_strategy,
            "biography": champ_bio
        }

        community = requests.get(
            f"https://raw.communitydragon.org/{version}/plugins/rcp-be-lol-game-data/global/default/v1/champions/{champ_id}.json"
        ).json()
        champ_stats = await get_champ_stats(champ_name)

        data[champ_id] = {
            **_champ_info,
            'champ_id': champ_id,
            'name': champ_name,
            'patch': version,
            'icon': f"https://raw.communitydragon.org/{version}/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{champ_id}.png",
            'stats': {
                'health': {
                    'flat': champ.get('stats', {}).get('hp', 0),
                    'per_level': champ.get('stats', {}).get('hpperlevel', 0),
                },
                'health_regen': {
                    'flat': champ.get('stats', {}).get('hpregen', 0),
                    'per_level': champ.get('stats', {}).get('hpregenperlevel', 0),
                },
                'mana': {
                    'flat': champ.get('stats', {}).get('mp', 0),
                    'per_level': champ.get('stats', {}).get('mpperlevel', 0),
                },
                'mana_regen': {
                    'flat': champ.get('stats', {}).get('mpregen', 0),
                    'per_level': champ.get('stats', {}).get('mpregenperlevel', 0),
                },
                'move_speed': {
                    'flat': champ.get('stats', {}).get('movespeed', 0),
                    'per_level': champ.get('stats', {}).get('movespeedperlevel', 0),
                },
                'armor': {
                    'flat': champ.get('stats', {}).get('armor', 0),
                    'per_level': champ.get('stats', {}).get('armorperlevel', 0),
                },
                'magic_resistance': {
                    'flat': champ.get('stats', {}).get('spellblock', 0),
                    'per_level': champ.get('stats', {}).get('spellblockperlevel', 0),
                },
                'attack_range': {
                    'flat': champ.get('stats', {}).get('attackrange', 0),
                    'per_level': champ.get('stats', {}).get('attackrangeperlevel', 0),
                },
                'crit': {
                    'flat': champ.get('stats', {}).get('crit', 0),
                    'per_level': champ.get('stats', {}).get('critperlevel', 0),
                },
                'attack_damage': {
                    'flat': champ.get('stats', {}).get('attackdamage', 0),
                    'per_level': champ.get('stats', {}).get('attackdamageperlevel', 0),
                },
                'attack_speed': {
                    'flat': champ.get('stats', {}).get('attackspeed', 0),
                    'per_level': champ.get('stats', {}).get('attackspeedperlevel', 0),
                },
                "missile_speed": champ_stats['missile_speed'],
                "attack_cast_time": champ_stats['attack_cast_time'],
                "attack_total_time": champ_stats['attack_total_time'],
                "attack_delay_offset": champ_stats['attack_delay_offset'],
                "acquisition_radius": champ_stats['acquisition_radius'],
                "selection_radius": champ_stats['selection_radius'],
                "gameplay_radius": champ_stats['gameplay_radius'],
                "pathing_radius": champ_stats['pathing_radius'],
                "aram_dmg_dealt": champ_stats['aram_dmg_dealt'],
                "aram_dmg_taken": champ_stats['aram_dmg_taken'],
                "aram_healing": champ_stats['aram_healing'],
                "aram_shielding": champ_stats['aram_shielding'],
                "urf_dmg_dealt": champ_stats['urf_dmg_dealt'],
                "urf_dmg_taken": champ_stats['urf_dmg_taken'],
                "urf_healing": champ_stats['urf_healing'],
                "urf_shielding": champ_stats['urf_shielding'],
            },
            "spells": [
                {
                    "key": spell["id"][-1],
                    "name": spell["name"],
                    "description": community['spells'][i]['description'],
                    'icon': f"https://raw.communitydragon.org/{version}/plugins/rcp-be-lol-game-data/global/default/assets/characters/{champ_name.lower()}/hud/icons2d/{community['spells'][i]['abilityIconPath']}",
                    "max_rank": spell.get("maxrank"),
                    **get_champ_spell(champ_name, spell['name']),
                    "cooldown": spell.get("cooldown"),
                    "cost": spell.get("cost"),
                    "range": spell.get("range"),
                } for i, spell in enumerate(champ.get("spells", []))
            ],
            'passive': {
                'name': champ.get("passive", {}).get('name'),
                'description': community.get("passive").get("description"),
                'icon': community.get("passive").get("abilityIconPath"),
                **get_champ_spell(champ_name, champ.get("passive", {}).get('name'))
            },
            "skins": [
                {
                    'id': skin['id'],
                    'is_base': skin['isBase'],
                    'name': skin['name'],
                    **(champ_skins[next((key for key in champ_skins if key in skin['name']), None)] if next(
                        (key for key in champ_skins if key in skin['name']), None) else {}),
                    'splash': f"https://raw.communitydragon.org/{version}/plugins/rcp-be-lol-game-data/global/default/v1/champion-splashes/{champ_id}/{skin['splashPath'].split('/')[-1]}",
                    'icon': f"https://raw.communitydragon.org/{version}/plugins/rcp-be-lol-game-data/global/default/v1/champion-tiles/{champ_id}/{skin['tilePath'].split('/')[-1]}",
                    "chroma_icon": f"https://raw.communitydragon.org/{version}/plugins/rcp-be-lol-game-data/global/default/v1/champion-chroma-images/{champ_id}/{skin['chromaPath'].split('/')[-1]}" if skin.get(
                        'chromaPath') is not None else None,
                    "chromas": [
                        {
                            'id': chroma.get('id'),
                            'name': chroma.get('name'),
                            'icon': chroma.get('chromaPath'),
                        } for chroma in skin.get("chromas", [])
                    ]
                } for skin in community['skins']
            ]
        }

    return list(data.values())


async def get_patch_data(version: str) -> dict:
    page = requests.get(
        f"https://www.leagueoflegends.com/en-gb/news/game-updates/patch-{version.replace('.', '-')}-notes/"
    )
    soup = BeautifulSoup(page.content)
    patch_container = soup.find('div', id='patch-notes-container')
    data = {'version': version}

    for section in patch_container.find_all('header', class_='header-primary'):
        section_name: str = section.text.strip().lower()

        if section_name in ['champions', 'items', 'runes']:
            data[section_name] = []

            for sib in section.next_siblings:
                if sib.name == 'div' and 'content-border' in sib.attrs.get('class', []):
                    selectors = [
                        ('h3', {}),
                        ('h4', {'class_': 'change-detail-title ability-title'}),
                        ('p', {})
                    ]

                    for tag, attrs in selectors:
                        element = sib.find(tag, **attrs)
                        if element and element.text:
                            champ = element.text.strip()
                            break
                    else:
                        continue

                    summary = sib.find('p', class_='summary')
                    if summary is not None:
                        summary = summary.text.strip()

                    reason = sib.find('blockquote', class_='blockquote context')
                    if reason is not None:
                        reason = reason.text.strip()

                    _section_data = {
                        'name': champ,
                        'summary': summary,
                        'reason': reason
                    }

                    if section_name == 'champions':
                        base_stat = sib.find('h4', class_='change-detail-title')
                        if base_stat is not None:
                            if base_stat.text.strip() == 'Base Stats':
                                try:
                                    _section_data['base_stats'] = [
                                        change.text.strip() for change in sib.find('ul').find_all('li')
                                    ]
                                except Exception:
                                    _base_stats = []
                                    for base_stat_sib in base_stat.next_siblings:
                                        if base_stat_sib.name == 'div' and 'attribute-change' in base_stat_sib.attrs.get(
                                                'class', []):
                                            _base_stats.append(base_stat_sib.text.strip())
                                        elif base_stat_sib.name == 'hr' and 'divider' in base_stat_sib.attrs.get(
                                                'class', []):
                                            break

                                    _section_data['base_stats'] = _base_stats

                        spells = []
                        _spells_sib = sib.find_all('h4', class_='change-detail-title ability-title')
                        if _spells_sib is not None:
                            for spell in _spells_sib:
                                spell_split = spell.text.strip().split('-')
                                if len(spell_split) == 1:
                                    spell_split.insert(0, None)

                                old_version = []
                                for spell_sib in spell.next_siblings:
                                    if spell_sib.name == 'ul':
                                        spells.append({
                                            'key': spell_split[0].strip() if spell_split[0] is not None else
                                            spell_split[0],
                                            'name': spell_split[1].strip(),
                                            'changes': [change.text.strip() for change in spell_sib.find_all('li')]
                                        })
                                        break
                                    elif spell_sib.name == 'div' and 'attribute-change' in spell_sib.attrs.get('class',
                                                                                                               []):
                                        old_version.append(spell_sib.text.strip())
                                    elif spell_sib.name == 'hr' and 'divider' in spell_sib.attrs.get('class', []):
                                        spells.append({
                                            'key': spell_split[0].strip() if spell_split[0] is not None else
                                            spell_split[0],
                                            'name': spell_split[1].strip(),
                                            'changes': old_version
                                        })
                                        break

                        _section_data['spells'] = spells

                    elif section_name in ['items', 'runes']:
                        try:
                            _section_data['changes'] = [change.text.strip() for change in sib.find('ul').find_all('li')]
                        except Exception:
                            _section_data['changes'] = [
                                change.text.strip() for change in sib.find_all('div', class_='attribute-change')
                            ]

                    data[section_name].append(_section_data)

                elif sib.name == 'header' and 'header-primary' in sib.attrs.get('class', []):
                    break

    return data


async def get_shard_data(version: str) -> List[dict]:
    shards = requests.get(
        f'https://raw.communitydragon.org/{version}/plugins/rcp-be-lol-game-data/global/default/v1/perks.json'
    ).json()

    for shard in shards:
        if 'statmods' in shard.get('iconPath', '').lower():
            shard[
                'iconPath'] = f"https://raw.communitydragon.org/{version}/plugins/rcp-be-lol-game-data/global/default/v1/perk-images/statmods/{shard['iconPath'].split('/')[-1].lower()}"
        shard['patch'] = version

    return shards


async def get_summoner_spell_data(version: str) -> List[dict]:
    summoner_spell = requests.get(
        f"https://raw.communitydragon.org/{version}/plugins/rcp-be-lol-game-data/global/default/v1/summoner-spells.json"
    ).json()

    for data in summoner_spell:
        if 'iconPath' in data:
            icon = data['iconPath'].split('/')[-1].lower()
            data[
                'iconPath'] = f"https://raw.communitydragon.org/{version}/plugins/rcp-be-lol-game-data/global/default/data/spells/icons2d/{icon}"

        data['patch'] = version

    return summoner_spell


async def get_perks_data(version: str) -> List[dict]:
    data: list = []
    constant: dict = {
        "Domination": ["Malice", "Tracking", "Hunter"],
        "Precision": ["Heroism", "Legend", "Combat"],
        "Sorcery": ["Artifact", "Excellence", "Power"],
        "Resolve": ["Strength", "Resistance", "Vitality"],
        "Inspiration": ["Contraption", "Tomorrow", "Beyond"],
    }
    perks: List[dict] = requests.get(
        f'https://ddragon.leagueoflegends.com/cdn/{version}.1/data/en_US/runesReforged.json').json()
    perks_path: str = f"https://raw.communitydragon.org/{version}/game/assets/perks/styles"

    for perk in perks:
        sub: dict = {
            "name": perk["name"],
            "icon": f"{perks_path}/{perk["icon"].split("/")[-1].lower()}",
            "patch": version,
            "keystone": [{
                "name": rune["name"],
                "icon": f"{perks_path}/{"/".join([i.lower() for i in rune["icon"].split("/")[-3:]])}",
                "short_description": rune["shortDesc"],
                "description": rune["longDesc"],
            } for rune in perk['slots'][0]["runes"]]
        }
        slots: List[dict] = []

        for i, slot in enumerate(perk["slots"][1:]):
            slots.append({
                "name": constant[sub["name"]][i],
                "runes": [{
                    "name": rune["name"],
                    "icon": f"{perks_path}/{"/".join([i.lower() for i in rune["icon"].split("/")[-3:]])}",
                    "short_description": rune["shortDesc"],
                    "description": rune["longDesc"],
                } for rune in slot["runes"]]
            })

        sub["slots"] = slots
        data.append(sub)

    return data


async def get_items_data(version: str) -> List[dict]:
    data: list = []
    community = requests.get(
        f"https://raw.communitydragon.org/{version}/plugins/rcp-be-lol-game-data/global/default/v1/items.json"
    )
    icons = {
        str(item['id']): item['iconPath'] for item in community.json()
    } if community.status_code == 200 else {}

    for item_id, items in requests.get(
            f'https://ddragon.leagueoflegends.com/cdn/{version}.1/data/en_US/item.json'
    ).json()["data"].items():
        try:
            int(item_id)
        except Exception:
            continue

        description = re.sub(r'<[^>]+>', ' ', items['description'])
        description = re.sub(r'\s+', ' ', description.strip())
        data.append({
            "patch": version,
            "item_id": int(item_id),
            "name": items['name'],
            "description": description,
            'icon': f'https://raw.communitydragon.org/{version}/plugins{icons[item_id]}' if icons.get(
                item_id) else None,
            "build_from": items.get('from'),
            "build_into": items.get('into'),
            "tags": items['tags'],
            "max_stacks": items.get('stacks'),
            "gold": {
                'base': items['gold']['base'],
                "purchasable": items['gold']['purchasable'],
                'total': items['gold']['total'],
                "sell": items['gold']['sell']
            },
            'stats': {
                "move_speed": {
                    'flat': items.get('stats', {}).get('FlatMovementSpeedMod', 0),
                    'percent': items.get('stats', {}).get('PercentMovementSpeedMod', 0),
                },
                "health": {
                    'flat': items.get('stats', {}).get('FlatHPPoolMod', 0),
                    'percent': 0
                },
                "crit": {
                    'flat': items.get('stats', {}).get('FlatCritChanceMod', 0),
                    'percent': 0
                },
                "magic_damage": {
                    'flat': items.get('stats', {}).get('FlatMagicDamageMod', 0),
                    'percent': 0
                },
                "mana": {
                    'flat': items.get('stats', {}).get('FlatMPPoolMod', 0),
                    'percent': 0
                },
                "armor": {
                    'flat': items.get('stats', {}).get('FlatArmorMod', 0),
                    'percent': 0
                },
                "magic_resistance": {
                    'flat': items.get('stats', {}).get('FlatSpellBlockMod', 0),
                    'percent': 0
                },
                "attack_damage": {
                    'flat': items.get('stats', {}).get('FlatPhysicalDamageMod', 0),
                    'percent': 0
                },
                "attack_speed": {
                    'flat': 0,
                    'percent': items.get('stats', {}).get('PercentAttackSpeedMod', 0)
                },
                "life_steal": {
                    'flat': 0,
                    'percent': items.get('stats', {}).get('PercentLifeStealMod', 0)
                },
                "health_regen": {
                    'flat': items.get('stats', {}).get('FlatHPRegenMod', 0),
                    'percent': 0
                },
            }
        })

    return data


async def add_data(
        version: str,
        get_data_func: Callable[[str], Awaitable[List[dict] | dict]],
        add_func: Callable[[dict], Awaitable[None]]
) -> None:
    data = await get_data_func(version)

    if isinstance(data, list):
        tasks = [add_func(sub_data) for sub_data in data]
        await asyncio.gather(*tasks)
    else:
        await add_func(data)


async def patch_release() -> None:
    version = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()[0][:-2]

    patch = Patch(version)
    try:
        await patch.get()
    except Exception:
        await add_data(version, get_patch_data, Patch.add)
        await add_data(version, get_shard_data, Shard.add)
        await add_data(version, get_perks_data, Perks.add)
        await add_data(version, get_summoner_spell_data, SummonerSpell.add)
        await add_data(version, get_champ_data, Champion.add)
        await add_data(version, get_items_data, Item.add)
