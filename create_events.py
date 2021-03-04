import os
import sys
from pathlib import Path
import subprocess
import json
import re
import datetime as dt
from pathlib import Path
import argparse
from bs4 import BeautifulSoup
from rich import print

def get_all_data(json_data):
    return (
        sorted(json_data['events'], key=lambda x:x['id']),
        json_data['topic_group'],
        json_data['max_id']
    )

def title_options(title, lang, events):
    return [e for e in events if e['lang'] != lang and title in e['title']]

def get_title(path: Path):
    with path.open(mode='r') as f:
        for line in f.readlines():
            if line[:2] == '# ':
                return line[2:-1]
    print(f'[red]No Title found in {path}[/]')
    sys.exit(1)

def get_description(path: Path):
    description = ''
    flag = False
    with path.open(mode='r') as f:
        for line in f.readlines():
            if r'<!-- description: ' in line:
                return line[18:4]
            if r'<!-- enddescription -->' in line:
                return description.replace('\n', ' ')
            if flag:
                description += line
            if r'<!-- description -->' in line:
                flag = True
    return ''

def get_category(path: Path):
    with path.open(mode='r') as f:
        return re.search(r'<\!-- category:(?:(?!<\!-- category:| -->).)* -->', f.read()).group()[15:-4]

def get_img(path: Path):
    highlight_path = 'events_img/default.png'
    with path.open(mode='r') as f:
        data = [line for line in f.readlines() if r'<!-- highlight-img -->' in line]
        if len(data) > 0:
            img_line = data[0]
            if r'<img' in img_line:
                highlight_path = img_line[img_line.index('src="') + 6:].split('"')[0]
            else:
                highlight_path = img_line[re.match(r'\!\[(?:(?!\!\[|\]).)*\]', img_line).end() + 1:].split(')')[0]
    return 'img' / Path(highlight_path)

def append_info(path: Path, info):
    with path.open(mode='r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(f'<!--\n{info}\n-->\n\n' + content)

def print_info(path: Path, info):
    print('file:', path)
    print('info:', info)

def compile_md(path: Path, to: Path):
    command = f'showdown makehtml -i {str(path)} -o {to} '
    options = [
        'omitExtraWLInCodeBlocks',
        'customizedHeaderId',
        'ghCompatibleHeaderId',
        'parseImgDimensions',
        'simplifiedAutoLink',
        'strikethrough',
        'tables',
        'ghCodeBlocks',
        'tasklists',
        'simpleLineBreaks',
        'requireSpaceBeforeHeadingText',
        'ghMentions',
        'ghMentionsLink',
        'emoji',
        'underline',
        'completeHTMLDocument'
    ]
    subprocess.run((command + ' --'.join(options)).split())
    with to.open('r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        for img in soup.find_all('img'):
            img['src'] = str('img' / Path(img['src']))
    with to.open('wb') as f:
        f.write(soup.prettify(encoding='utf-8'))
    return to

def create_newfile(md_file: Path, new_event):
    new_event['markdown'] = str(md_file)
    new_event['created_at'] = dt.datetime.now().strftime('%s')
    new_event['title'] = get_title(md_file)
    new_event['description'] = get_description(md_file)
    new_event['category'] = get_category(md_file)
    new_event['img'] = str(get_img(md_file))

    html_file = output_dir / 'events_html' / f'{md_file.stem}.html'
    html_file.touch()
    new_event['src_location'] = f'events/events_html/{md_file.stem}.html'

    compile_md(md_file, html_file)

def share_info_on_mattermost(title):
    os.system(f'mattermost share "new page \\"{title}\\" added on my webpage!"')

def update_json(events, topic_group, max_id):
    with json_path.open(mode='w') as f:
        f.write(json.dumps({
            'events': sorted(events, key=lambda x:x['created_at'], reverse=True),
            'topic_group': topic_group,
            'max_id': max_id
        }, indent=4, sort_keys=True))

def create_event(filepath: str, is_translate):
    with json_path.open(mode='r') as f:
        json_data = json.loads(f.read())
    events, topic_group, max_id = get_all_data(json_data)
    max_id += 1

    md_file = Path(filepath)
    new_event = {
        'id': max_id,
        'created_at': dt.datetime.now().strftime('%s'),
        'title': '',
        'filename': md_file.stem,
        'lang': input('Language: '),
        'description': None,
        'category': None,
        'img': None,
        'markdown': '',
        'src_location': '',
        'version': 0
    }

    if not md_file.exists():
        print(f'{md_file.stem} does not exits')
        return
    if md_file.suffix != '.md':
        print(f'suffix of {md_file.name} is not ".md"')
        return

    group_id = -1
    if is_translate:
        title_list = title_options(input('Translated title: '), new_event['lang'], events)
        group_id = title_list[int(input('\t'.join([f'{i}.{t["title"]}' for i, t in enumerate(title_list)]) + ': '))]['topic_id']
    else:
        if new_event['filename'] in [e['filename'] for e in events]:
            print('[red]You pprobably have added this file already[/]', file=sys.stderr)
            sys.exit(1)

    if group_id == -1:
        topic_group.append({})
        group_id = len(topic_group) - 1
    new_event['topic_id'] = group_id
    topic_group[group_id][new_event['lang']] = new_event['id']

    create_newfile(md_file, new_event)

    # append_info(new_event['markdown'], new_event)
    print_info(md_file, new_event)

    events.append(new_event)
    update_json(events, topic_group, max_id)
    # share_info_on_mattermost(new_event['title'])

def update_event(path: Path):
    with json_path.open(mode='r') as f:
        json_data = json.loads(f.read())
    events, topic_group, max_id = get_all_data(json_data)

    md_file = Path(path)
    old_events = list(filter(lambda x:x['markdown'] == str(md_file), events))
    if len(old_events) == 0:
        print(f'Could not file file {str(md_file)}')
        return

    new_event = old_events[0]
    events.pop(events.index(new_event))
    new_event['version'] += 1
    new_event['created_at'] = dt.datetime.now().strftime('%s')
    create_newfile(md_file, new_event)
    events.append(new_event)
    update_json(events, topic_group, max_id)
    # share_info_on_mattermost(new_event['title'])

    print_info(md_file, new_event)

def delete_event(path: Path):
    pass

def delete_all_events(force=False):
    if force or input('Are you sure you want to delete all events? (y/N): ') == 'y':
        update_json([], [], 0)

def show_all_events():
    with json_path.open(mode='r') as f:
        json_data = json.loads(f.read())
    events, topic_group, max_id = get_all_data(json_data)
    print(events)
    print(topic_group)
    print(max_id)

def language_settings():
    lang_path = Path('./src/lang')
    dictionary = {}
    for p in lang_path.glob('*.csv'):
        with p.open(mode='r') as f:
            contents = f.read().split('\n')
            languages = contents[0].split(',')[1:]
            for l in languages:
                dictionary.setdefault(l, {})
            for line in contents[1:]:
                keys = line.split(',')
                if len(keys) < len(languages) + 1:
                    continue
                for i, lang in enumerate(languages):
                    dictionary[lang].setdefault(p.stem.capitalize(), {})
                    dictionary[lang][p.stem.capitalize()][keys[0]] = keys[i + 1].replace('~', ',')
    with (lang_path / 'dictionary.json').open(mode=('w')) as f:
        f.write(json.dumps(dictionary))
        print(dictionary)

output_dir = Path('./events_md/')
json_path = output_dir / 'events.json'
if not (output_dir / 'events_html').exists():
    (output_dir / 'events_html').mkdir(parents=True)
if not json_path.exists():
    delete_all_events(True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='upload .md to your webpage')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--create', type=str, help='create [filepath]')
    group.add_argument('-t', '--translate', type=str, help='translate [filepath]')
    group.add_argument('-u', '--update', type=str, help='update [filepath]')
    group.add_argument('-d', '--delete', type=str, help='delete [filepath]')
    group.add_argument('--deleteall', action='store_true', help='init events.json')
    group.add_argument('--showall', action='store_true', help='print events.json')
    parser.add_argument('-b', '--build', action='store_true', help='run ./vue-build.sh')
    parser.add_argument('-r', '--run', action='store_true', help='npm run dev')
    parser.add_argument('--lang', action='store_true', help='language json')

    args = parser.parse_args()

    if args.create:
        create_event(args.create, False)
    elif args.translate:
        create_event(args.translate, True)
    elif args.update:
        update_event(args.update)
    elif args.delete:
        delete_event(args.delete)
    elif args.deleteall:
        delete_all_events()
    elif args.showall:
        show_all_events()

    if args.lang:
        language_settings()

    if args.build:
        os.system('sh vue-build.sh')
    elif args.run:
        os.system('npm run dev')
