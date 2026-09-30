// Offline renderer regressions; no dependencies, network, or homework writes.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const html = fs.readFileSync(path.join(__dirname, '../analysis/review_app/index.html'), 'utf8');
const script = html.match(/<script id="review-markdown">([\s\S]*?)<\/script>/)[1];
const markdown = vm.runInNewContext(script + '\nReviewMarkdown', {URL});
const decode = s => s.replace(/<[^>]*>/g, '').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, '&');
function mapped(source, rendered) {
  const spans = [...rendered.matchAll(/<span data-source-start="(\d+)" data-source-end="(\d+)">([\s\S]*?)<\/span>/g)];
  assert.ok(spans.length, 'source spans are present');
  for (const [,start,end,body] of spans) assert.equal(decode(body), source.slice(+start,+end));
  return spans;
}

test('all page scripts parse independently', () => {
  for (const [,code] of html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)) new vm.Script(code);
});
test('headings, lists, strong, emphasis, inline code, and quotes are formatted', () => {
  const source = '# Status\n\nOrder **2** is *delivered*.\n\n- **Total:** $217.75\n- `refund_eligible: true`\n\n> A quoted answer.';
  const out = markdown.render(source);
  for(const tag of ['h1','strong','em','ul','li','code','blockquote']) assert.match(out,new RegExp('<'+tag+'(?:>| )'));
  assert.doesNotMatch(decode(out), /\*\*|`refund/);
  mapped(source,out);
});
test('tables render header/body cells, alignment and escaped pipes', () => {
  const source = '| Item | Value |\n|:---|---:|\n| **Total** | $12.50 |\n| A \\| B | `x|y` |';
  const out = markdown.render(source);
  assert.match(out, /<table>/);assert.match(out, /<thead>/);assert.match(out, /text-align:right/);
  assert.equal((out.match(/<td /g)||[]).length,4);
  assert.match(decode(out), /A \| B/);assert.match(decode(out), /x\|y/);
  mapped(source,out);
});
test('legacy quotes with markup retain original offsets and highlights', () => {
  const source = 'Details:\n- **Total:** $217.75\n- Quantity: 1';
  const quote = '- **Total:** $217.75', start = source.indexOf(quote);
  const out = markdown.render(source,[{start,end:start+quote.length,id:'existing-human-note'}]);
  assert.match(out, /data-item="existing-human-note"/);
  assert.match(out, /<strong>/);assert.match(out, /<li>/);
  assert.doesNotMatch(decode(out), /\*\*/);
  mapped(source,out);
  const raw = markdown.render(source,[{start,end:start+quote.length,id:'existing-human-note'}],false);
  assert.equal(decode(raw),source);
});
test('overlapping human, suggestion, and pending highlights are retained', () => {
  const source = '**Total:** $42.00';
  const out=markdown.render(source,[{start:0,end:source.length,id:'human'},{start:2,end:7,id:'suggestion',type:'suggestion'},{start:3,end:6,id:'pending',pending:true}]);
  for(const id of ['human','suggestion','pending']) assert.match(out,new RegExp('data-item="'+id+'"'));
  assert.match(out,/highlight pending/);assert.match(out,/highlight suggestion/);mapped(source,out);
});
test('raw HTML is inert and remote images never fetch', () => {
  const source='<script>alert("x")</script> <img src=x onerror=alert(1)>\n\n![tracking](https://example.org/pixel)';
  const out=markdown.render(source);
  assert.doesNotMatch(out, /<(?:script|img|iframe)\b/i);
  assert.match(decode(out), /<script>/);assert.match(out,/Image:/);mapped(source,out);
});
test('unsafe destinations stay literal; safe links have noopener', () => {
  for(const url of ['javascript:evil','data:text/html,evil','file:///etc/passwd']) {
    assert.doesNotMatch(markdown.render(`[click](${url})`),/<a /);
  }
  const source='[policy](https://example.org/policy?q=1&v=2)';
  const out=markdown.render(source);assert.match(out,/rel="noopener noreferrer"/);mapped(source,out);
});
test('fenced code is literal, including HTML and emphasis syntax', () => {
  const source='```json\n{"x": "**literal**", "html":"<b>"}\n```';
  const out=markdown.render(source);assert.match(out,/<pre><code>/);assert.doesNotMatch(out,/<strong>|<b>/);
  assert.match(decode(out),/\*\*literal\*\*/);mapped(source,out);
});
test('unicode, CRLF, underscores in identifiers, and repeated quotes map exactly', () => {
  const source='## Café 🧪\r\n\r\nrefund_eligible is true.\r\n\r\n**same** and **same**';
  const start=source.lastIndexOf('same'), out=markdown.render(source,[{start,end:start+4,id:'second-only'}]);
  assert.match(decode(out),/refund_eligible/);assert.equal((out.match(/data-item="second-only"/g)||[]).length,1);
  mapped(source,out);
});
test('nested lists and blockquotes preserve every visible source fragment', () => {
  const source='1. Parent\n   - Child **bold**\n   - Next child\n2. Second\n\n> ## Quoted heading\n> Text';
  const out=markdown.render(source);assert.match(out,/<ol start="1">/);assert.match(out,/<ul>/);assert.match(out,/<blockquote><h2>/);mapped(source,out);
});
test('hard line breaks and thematic rules are displayed', () => {
  const out=markdown.render('First  \nSecond\n\n---\n\nLast');assert.match(out,/<br>/);assert.match(out,/<hr>/);
});
test('plain source mode retains every character and escapes attributes', () => {
  const source='**literal** <img>\n| a | b |';
  const out=markdown.render(source,[{start:0,end:4,id:'" onmouseover="evil'}],false);
  assert.equal(decode(out),source);assert.doesNotMatch(out, /data-item="" onmouseover=/);mapped(source,out);
});
test('malformed tables and unmatched delimiters remain readable', () => {
  const source='**Unclosed and [broken](javascript:evil)\n\n| a | b |\n|---|\nnot a table';
  const out=markdown.render(source);assert.doesNotMatch(out,/<table>|<a /);assert.match(decode(out),/\*\*Unclosed/);mapped(source,out);
});
test('large input falls back to exact text rather than truncating evidence', () => {
  const source='*'.repeat(200001);assert.equal(decode(markdown.render(source)),source);
});
