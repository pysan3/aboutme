from paramsparser import Json2Params
import argparse
import datetime as dt
import json
import os
import random
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

from bs4 import BeautifulSoup as bs
from rich import print
from rich.table import Table


def rinput(*args):
    print(*args, end='', flush=True)
    return input()


checkyes = False


def unix2ctime(t: str):
    return dt.datetime.fromtimestamp(int(t)).ctime()


mattermost = False


def share_on_mattermost(*msg: str):
    share_msg = '\n'.join([s.replace('"', r'\"') for s in msg])
    if mattermost == 'strict':
        print('not sharing...')
        return
    print('mattermost share', share_msg)
    if mattermost or rinput('Share it on Mattermost? \\[y/N]: ') == 'y':
        note = rinput('Note ? [""]: ')
        if len(note) != 0:
            share_msg += '\nNote: ' + note
        print(share_msg)
        os.system(f'mattermost share "{share_msg}"')


class DotEnvParser:
    def __init__(self, env_path) -> None:
        if not isinstance(env_path, Path):
            env_path = Path(env_path)
        self.env_path = env_path
        self.parse()

    def parse(self):
        self.envs = os.environ
        with self.env_path.open(mode='r') as f:
            for line in f.read().split('\n'):
                key, *values = line.split('=')
                self.envs[key] = '='.join(values)


class MarkdownParser:
    def __init__(self, path: Path, info=None, compiler='showdown') -> None:
        if info is None:
            info = {}
        self.path: Path = path
        if not self.path.exists():
            print('[red]No File Found[/]', file=sys.stderr)
            sys.exit(1)
        elif self.path.suffix != '.md':
            print('[red]File is not a markdown[/]')
            sys.exit(1)
        self.file_content = self.get_content_with_compiler(compiler)
        self.info = info
        self.info['markdown'] = str(self.path)
        self.info['created_at'] = self.get_created_at()
        self.info['title'] = self.get_title()
        self.info['description'] = self.get_description()
        self.info['category'] = self.get_category()
        self.info['img'] = self.get_img()
        self.info['pdflink'] = self.get_pdflink()
        for k in ['bibtex']:
            self.info[k] = self.get_keys(k)

    def get_content_with_compiler(self, compiler_name) -> str:
        if not compiler_name:
            compiler_name = 'markdown-it'
        compiler_name = compiler_name.lower().replace('-', '')
        options = {
            'showdown': self.showdown_content,
            'markdownit': self.markdownIt_content,
            'md': self.md_content,
            'markdown': self.md_content
        }
        return options[compiler_name]() if compiler_name in options else self.default_content(compiler_name)

    def get_created_at(self):
        if 'created_at' not in self.info:
            result = dt.datetime.now().strftime('%s')
        else:
            result = self.info['created_at']
        created = rinput(f'created_at? \\[yy mm dd] (default: {unix2ctime(result)}): ')
        if created == 'now':
            result = dt.datetime.now().strftime('%s')
        elif created != '':
            result = dt.datetime(*[int(i) for i in created.split(' ')]).strftime('%s')  # type: ignore
        return result

    def get_title(self):
        title = bs(self.file_content, 'html.parser').find('h1')
        if title:
            return ''.join([f'{s}'.strip() for s in title.contents])
        print('[red]Could not find title[/]', file=sys.stderr)
        sys.exit(1)

    def get_description(self):
        description = []
        flag = False
        header_depth = 0
        for line in self.file_content.split('\n'):
            if r'<!-- description: ' in line:
                return line.strip()[18:4].strip()
            if r'<!-- enddescription -->' in line:
                return ''.join(description)
            if re.search(r'<h\d', line):
                header_depth += 1
            if flag and len(line.strip()) > 0 and header_depth == 0:
                description.append(line.strip())
            if re.search(r'</h\d>', line):
                header_depth -= 1
            if r'<!-- description -->' in line:
                flag = True
        return ''

    def get_category(self):
        return self.path.parent.name

    def get_img(self):
        highlight_path = 'events/events_img/default.png'
        for line in self.file_content.split('\n'):
            if r'highlight-img' in line:
                if r'<img' in line:
                    highlight_path = line[line.index('src="') + 5:].split('"')[0]
                else:
                    highlight_path = line[re.search(r'!\[(?:(?!!\[|\]).)*\]', line).end() + 1:].split(')')[0]
                break
        return str(Path(highlight_path))

    def get_pdflink(self):
        path = self.get_keys('pdflink')
        if path is not None:
            path = 'events/events_files/' + path
        return path

    def get_keys(self, keyname):
        result = re.search(rf'<!-- {keyname}:(?:(?!<!-- {keyname}:|-->).)*-->', self.file_content)
        if result:
            return result.group()[len(f'<!-- {keyname}:'):-len('-->')].strip()
        else:
            return None

    def print_info(self):
        print('file:', self.path)
        print('info:', self.info)

    def showdown_content(self):
        # tmpFile = (lambda x,f=lambda f,x=Path(f'tmp-{random.random()}.html'):f(f,f()if x.exists()else x):f(f))()
        def generateTmpFile(x: str = f'tmp-{random.random()}.html'):
            return generateTmpFile() if Path(x).exists() else x
        tmpFile = Path(generateTmpFile())
        tmpFile.touch(exist_ok=False)
        command = f'showdown makehtml -i {self.path} -o {tmpFile} '
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
        subprocess.run((command + ' --'.join(options)).split(), stdout=subprocess.DEVNULL)
        with tmpFile.open('r') as f:
            soup = bs(f.read(), 'html.parser')
            for img in soup.find_all('img'):
                img['src'] = str(Path(img['src']))
        tmpFile.unlink()
        return soup.prettify()

    def markdownIt_content(self):
        return self.default_content('node events/md_cli.mjs -p src/plugins/markdown.js')

    def md_content(self):
        with self.path.open(mode='r') as f:
            return f.read()

    def default_content(self, cmd):
        with self.path.open(mode='r') as f:
            p = subprocess.Popen(cmd.split(' '), stdin=f, stdout=subprocess.PIPE)
            return p.stdout.read().decode()


class Events:
    def __init__(self, output_dir='./events/', json_name='events.json', compiler='markdown-it') -> None:
        if not isinstance(output_dir, Path):
            output_dir = Path(output_dir)
        self.output_dir: Path = output_dir
        self.json_path: Path = self.output_dir / json_name
        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True, exist_ok=True)
        if not self.json_path.exists():
            self.delete_all_events(True)
        self.compiler = compiler or 'markdown-it'
        self.load()
        self.save(self.output_dir / 'events_backup.json')

    def load(self):
        self.params = Json2Params(filename=str(self.json_path))
        self.events = self.params['events']
        self.topic_group = self.params['topic_group']
        self.max_id = self.params['max_id']

    def save(self, new_filename=None):
        self.params.events = self.events
        self.params.topic_group = self.topic_group
        self.params.max_id = self.max_id
        self.params.biblist = [f'events/events_files/{b.name}' for b in self.output_dir.glob('events_files/*.bib')]
        if new_filename is None:
            new_filename = self.json_path
        self.params.save(new_filename=str(new_filename), overwrite=True)

    def list_events(self, events):
        table = Table(show_header=True)
        table.add_column('index', justify='right')
        table.add_column('filename')
        table.add_column('title')
        table.add_column('version', justify='center')
        table.add_column('created_at')
        for i, event in enumerate(events):
            table.add_row(
                str(i),
                event['filename'] + '.md',
                f'[green]{event["title"]}',
                str(event['version']),
                unix2ctime(event['created_at'])
            )
        print(table)

    def delete(self):
        self.list_events(self.events)
        del_event = self.events.pop(int(input('Index? [-1]: ') or '-1'))
        self.topic_group[del_event['topic_id']].pop(del_event['lang'], None)
        self.show_all_events()

    def delete_all_events(self, force=False):
        if force or checkyes or rinput('Are you sure you want to delete all events? \\[y/N]: ') == 'y':
            os.system(f'rm -rf {self.json_path}')
            self.events = []
            self.topic_group = []
            self.max_id = 0
            self.save()

    def show_all_events(self):
        self.list_events(self.events)
        print('Topic Groups:', self.topic_group)
        print('Num of Contents:', self.max_id)

    def _title_options(self, s: str, lang: str):
        events_list = list(filter(lambda x: x['lang'] != lang, self.events))
        sets = set([])
        for keyword in s.split():
            sets |= set([e['id'] for e in events_list if keyword in e['title']]) \
                | set([e['id'] for e in events_list if keyword in e['markdown']])
        return [e for e in events_list if e['id'] in sets]

    def create(self, md_path: Path, translate=False):
        self.max_id += 1
        new_event = {
            'id': self.max_id,
            'lang': rinput('Language: '),
            'filename': md_path.stem,
            'version': 0,
        }

        md_parser = MarkdownParser(md_path, compiler=self.compiler)
        # md_parser.save_html(md_path / 'html')
        md_parser.print_info()
        new_event.update(md_parser.info)

        group_id = -1
        if translate:
            title_list = self._title_options(rinput('Translated title: '), new_event['lang'])
            self.list_events(title_list)
            group_id = title_list[int(rinput('Translated which File? [-1]: ') or '-1')]['topic_id']
        else:
            if new_event['filename'] in [e['filename'] for e in self.events]:
                print('[red]You probably have already added this file[/]', file=sys.stderr)
                sys.exit(1)

        if group_id == -1:
            self.topic_group.append({})
            group_id = len(self.topic_group) - 1
        new_event['topic_id'] = group_id
        self.topic_group[group_id][new_event['lang']] = new_event['id']

        self.events.append(new_event)
        self.show_all_events()

        share_on_mattermost('New page uploaded! https://esslab.jp/~takuto/#/event/' + str(new_event['id']),
                            f'**{new_event["title"]}**')

    def update(self, md_path: Path):
        old_events = list(filter(lambda x: x['markdown'] == str(md_path), self.events))
        if len(old_events) == 0:
            print('[red]Could not find old data.[/] Maybe try [blue]-c[/] option', sys.stderr)
            sys.exit(1)
        new_event = old_events[0]
        self.events.pop(self.events.index(new_event))
        new_event['version'] += 1
        md_parser = MarkdownParser(md_path, new_event, self.compiler)
        # md_parser.save_html(md_path / 'html')
        md_parser.print_info()
        new_event.update(md_parser.info)

        self.events.append(new_event)
        # self.show_all_events()

        share_on_mattermost('Updated https://esslab.jp/~takuto/#/event/' + str(new_event['id']),
                            f'**{new_event["title"]}**')


def copy_files(source: str, *dist: str):
    source_name = f'src/views/{source.capitalize()}.vue'
    for t in dist:
        if t == source:
            continue
        to_name = f'src/views/{t.capitalize()}.vue'
        os.system(f'diff {source_name} {to_name}')
        if checkyes or rinput('Change content? \\[y/N]: ') == 'y':
            os.system(f'cp {source_name} {to_name}')
            os.system(f'sed -i -e "s/{source}/{t}/g" {to_name}')


class Notifications:
    def __init__(self, output_dir='./events', json_name='notifications.json') -> None:
        if not isinstance(output_dir, Path):
            output_dir = Path(output_dir)
        self.output_dir: Path = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.json_name = json_name
        self.json_path: Path = self.output_dir / self.json_name
        if not self.json_path.exists():
            self.delete_all(save=True)
        self.load()

    def delete_all(self, save=True):
        self.data: List[Dict[str, Any]] = []
        if save:
            self.save()

    def load(self):
        with self.json_path.open(mode='r') as f:
            self.data: List[Dict[str, Any]] = json.loads(f.read())

    def save(self):
        with self.json_path.open(mode='w') as f:
            f.write(json.dumps(self.data, indent=4, sort_keys=True))

    def add(self, datetime: dt.datetime, contents: Dict[str, str], description=None, link=None):
        new_data = {
            'date': datetime.strftime('%s'),
            'content': contents,
        }
        new_data['description'] = description
        new_data['link'] = link
        self.data.append(new_data)

        share_on_mattermost('New notification on https://esslab.jp/~takuto/', new_data['description'])

    def add_interact(self):
        date, time = [s.strip() for s in (rinput('date [(Y )M D, (h m)]: ') + ',,').split(',')][:2]
        if len(date.split(' ')) == 2:
            date = f'{dt.datetime.now().year} {date}'
        time += '0 0'
        datetime = dt.datetime(*[int(i) for i in date.split(' ') + time.split(' ')])  # type: ignore
        languages = VueI18nDict().availableLocales
        content = {}
        content_prev = []
        for lang in languages:
            index = 0
            content[lang] = ''
            while True:
                if len(content_prev) <= index:
                    content_prev.append({'tag': '?', 'content': ''})
                prev = content_prev[index]
                tag, text = [s.lstrip() for s in (
                    rinput(f'<{prev["tag"]}>(q:quit), "{prev["content"]}" [[green]{lang}[/]]: ') + ',,').split(',')][:2]
                if tag == 'q':
                    break
                elif tag == '':
                    tag = prev['tag']
                    if tag == '?':
                        tag = 'span'
                t = tag.split(' ')[0]
                content[lang] += f'<{tag}>{text}</{t}>'
                content_prev[index] = {'tag': tag, 'content': text}
                index += 1
        description = {}
        for lang in languages:
            description[lang] = rinput(f'description [[green]{lang}[/]]: ') or None
        link = {}
        link_prev = None
        for lang in languages:
            link[lang] = rinput(f'link [[green]{lang}[/]]: ') or None
            if link[lang] == 'same':
                link[lang] = link_prev
            link_prev = link[lang]
        self.add(datetime, content, description, link)


class VueI18nDict:
    def __init__(self, lang_dir='./src/lang', json_name='dictionary.json') -> None:
        if not isinstance(lang_dir, Path):
            lang_dir = Path(lang_dir)
        self.lang_dir = lang_dir
        self.json_name = json_name
        self.json_path = self.lang_dir / self.json_name
        self.dictionary = {}
        if self.json_path.exists():
            with self.json_path.open('r') as f:
                self.dictionary = json.loads(f.read())
        self.availableLocales = list(self.dictionary.keys())

    def from_csv(self):
        for p in self.lang_dir.glob('*.csv'):
            with p.open(mode='r') as f:
                contents = f.read().split('\n')
                languages = contents[0].split(',')[1:]
                for lang in languages:
                    self.dictionary.setdefault(lang, {})
                for line in contents[1:]:
                    keys = line.split(',')
                    if len(keys) < len(languages) + 1:
                        continue
                    for i, lang in enumerate(languages):
                        self.dictionary[lang].setdefault(p.stem.capitalize(), {})
                        self.dictionary[lang][p.stem.capitalize()][keys[0]] = keys[i + 1].replace('~', ',')

    def reset(self):
        self.dictionary = {}

    def save(self):
        with self.json_path.open(mode='w') as f:
            f.write(json.dumps(self.dictionary, indent=4, sort_keys=True))

    def print(self):
        print(self.dictionary)


if __name__ == "__main__":
    env = DotEnvParser('./.env')

    parser = argparse.ArgumentParser(description='upload .md to your webpage')
    parser.add_argument('-y', '--yes', action='store_true', help='say yes to all questions')
    parser.add_argument('-p', '--paste', type=str, help='copy [from] [to,...]')
    parser.add_argument('-m', '--mattermost', type=str, help='share on mattermost without check')
    parser.add_argument('--compiler', type=str, help='compiler [command str]')
    args_notifications = parser.add_mutually_exclusive_group()
    args_notifications.add_argument('-n', '--notifications', action='store_true', help='add notification')
    args_notifications.add_argument('--nd', action='store_true', help='delete all notification')
    args_markdown = parser.add_mutually_exclusive_group()
    args_markdown.add_argument('-c', '--create', type=str, help='create [filepath]')
    args_markdown.add_argument('-t', '--translate', type=str, help='translate [filepath]')
    args_markdown.add_argument('-u', '--update', type=str, help='update [filepath]')
    args_markdown.add_argument('-d', '--delete', action='store_true', help='delete')
    args_markdown.add_argument('--deleteall', action='store_true', help='init events.json')
    args_markdown.add_argument('--showall', action='store_true', help='print events.json')
    parser.add_argument('--lang', action='store_true', help='language json')

    args = parser.parse_args()
    if args.yes:
        checkyes = True

    if args.paste:
        copy_files(*args.paste.split(' '))
    if args.mattermost:
        mattermost = True

    events = Events(output_dir='./events', json_name='events.json', compiler=args.compiler)
    if args.create:
        events.create(Path(args.create), translate=False)
    elif args.translate:
        events.create(Path(args.translate), translate=True)
    elif args.update:
        events.update(Path(args.update))
    elif args.delete:
        events.delete()
    elif args.deleteall:
        events.delete_all_events()
    elif args.showall:
        events.show_all_events()
    events.save()

    if args.nd:
        n = Notifications('./events', json_name='notifications.json')
        n.delete_all(save=True)
    if args.notifications:
        n = Notifications('./events', json_name='notifications.json')
        n.add_interact()
        n.save()

    if args.lang:
        lang = VueI18nDict('./src/lang', json_name='dictionary.json')
        lang.reset()
        lang.from_csv()
        lang.save()
        lang.print()
