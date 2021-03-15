/*
npm install --save \
  markdown-it \
  highlight.js \
  markdown-it-sanitizer \
  markdown-it-emoji \
  @iktakahiro/markdown-it-katex \
  markdown-it-imsize \
  markdown-it-checkbox \
  markdown-it-sub \
  markdown-it-sup \
  markdown-it-container \
  markdown-it-ins \
  markdown-it-mark \
  markdown-it-footnote \
  markdown-it-deflist \
  markdown-it-abbr \
  markdown-it-anchor \
  markdown-it-multimd-table \
  markdown-it-attribution \
  markdown-it-named-headers \

  twemoji
*/

/*
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/3.0.1/github-markdown.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.6/styles/xcode.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.10.0/katex.min.css">
*/

// Usage
// this.markdownIt.render(rawText)

import MarkdownIt from 'markdown-it';
import hljs from 'highlight.js';
import emoji from 'markdown-it-emoji';
import katex from '@iktakahiro/markdown-it-katex';
import checkbox from 'markdown-it-checkbox';
import sub from 'markdown-it-sub';
import sup from 'markdown-it-sup';
import container from 'markdown-it-container';
import ins from 'markdown-it-ins';
import mark from 'markdown-it-mark';
import footnote from 'markdown-it-footnote';
import deflist from 'markdown-it-deflist';
import abbr from 'markdown-it-abbr';
import anchor from 'markdown-it-anchor';
import multimdtable from 'markdown-it-multimd-table';
import attribution from 'markdown-it-attribution';
import namedheaders from 'markdown-it-named-headers';
import twemoji from 'twemoji';

const md = new MarkdownIt({
  highlight(code, lang) {
    return hljs.highlightAuto(code, [lang]).value;
  },
  html: true,
  linkify: true,
  breaks: true,
  typographer: true,
})
  .use(attribution)
  .use(katex, { throwOnError: false, errorColor: ' #cc0000' })
  .use(emoji)
  .use(checkbox)
  .use(sub)
  .use(sup)
  .use(ins)
  .use(mark)
  .use(footnote)
  .use(deflist)
  .use(abbr)
  .use(anchor)
  .use(multimdtable)
  .use(namedheaders)
  .use(container, 'info')
  .use(container, 'success')
  .use(container, 'warning')
  .use(container, 'danger');

md.renderer.rules.emoji = (token, idx) => twemoji.parse(token[idx].content);

export default md;
