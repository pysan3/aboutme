import fs from 'fs';
import path from 'path';
import args from 'commander';
import MarkdownIt from 'markdown-it';

args.version('1.0.0')
  .option('-p --package <path>', 'specify path to md parser')
  .option('-i --input <path>', 'path to markdown file to parse, if not specified, will be taken from stdin')
  .option('-o --output <path>', 'path to html file to parse, if not specified, will be printed to stdout')
  .parse(process.argv);

const resolve = (p) => {
  if (p) return path.resolve(process.env.PWD, p);
  return undefined;
};

const loadMyPackage = (packagePath) => {
  const tmpFile = resolve(function t(f = `tmp-${Math.random()}.mjs`) { return fs.existsSync(f) ? t() : f; }());
  fs.writeFileSync(tmpFile, fs.readFileSync(packagePath));
  return import(tmpFile).then((e) => {
    fs.unlinkSync(tmpFile);
    return e.default;
  }).catch((error) => {
    fs.unlinkSync(tmpFile);
    console.error(error);
  });
};

const main = async () => {
  const markdownIt = args.package ? await loadMyPackage(resolve(args.package)) : new MarkdownIt({
    html: true,
    linkify: true,
    breaks: true,
    typographer: true,
  });

  const html = markdownIt.render(fs.readFileSync(resolve(args.input) || '/dev/stdin', 'utf-8'));

  if (args.output) {
    fs.writeFileSync(args.output, html);
  } else {
    console.log(html);
  }
};

main().catch((e) => { console.log(e.stack); });
