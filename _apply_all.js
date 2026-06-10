var fs = require('fs');
var c = fs.readFileSync('index.html', 'utf8');
var lines = c.split('\n');

for (var i = 0; i < lines.length; i++) {
  var l = lines[i];

  // Fix scTxt: add .toFixed(1) to all c.payout
  if (l.indexOf('const scTxt=c?') >= 0) {
    lines[i] = "	          const scTxt=c?(c.exact?(c.odds?'🎯 '+c.stake+'×'+c.odds+'='+Number(c.payout).toFixed(1):'🎯+'+Number(c.payout).toFixed(1)):'❌'+Number(c.payout).toFixed(1)):'';";
  }

  // Fix template: remove +'分' after wdlTxt and scTxt
  if (l.indexOf("'胜平负:'+wdlTxt+'分'") >= 0) {
    lines[i] = l.replace(/'胜平负:'\+wdlTxt\+'分/g, "'胜平负:'+wdlTxt");
  }
  if (l.indexOf("'比分:'+scTxt+'分'") >= 0) {
    lines[i] = l.replace(/'比分:'\+scTxt\+'分/g, "'比分:'+scTxt");
  }

  // Fix total: remove +'分'
  if (l.indexOf("'合计: '+totalTxt+'分'") >= 0) {
    lines[i] = l.replace(/合计: '\+(totalTxt|total)都不会\+\'分'/g, "合计: '+totalTxt");
    // Simpler: just replace the known pattern
  }

  // Fix rank display: decimal in smaller font
  if (l.indexOf('${Math.round(x.balance)}分') >= 0) {
    lines[i] = l.replace(
      '${Math.round(x.balance)}分',
      "${Math.floor(x.balance)}<span style=\"font-size:9px;color:var(--text2);\">."+String((x.balance%1).toFixed(2).slice(2))+"</span>"
    );
  }
}

c = lines.join('\n');

// Fix scTxt properly using string replace for the template line
// Actually, the template lines also have '合计: '+totalTxt+'分' at the end
// Let me fix that too
c = c.replace(/'合计: '\+(totalTxt|total)都不\+\'分'/g, "'合计: '+totalTxt");

// The total line is inside a template literal return:
// '</div><span...>合计: '+totalTxt+'分</span></span>';
// I need to remove the +'分'
// Let me use a simpler regex on the whole file
c = c.replace(/'合计: '\+(totalTxt)\+'分/g, "'合计: '+$1");

fs.writeFileSync('index.html', c, 'utf8');

// Verify syntax
var m = c.match(/<script>[\s\S]*?<\/script>/);
if (m) {
  try { new Function(m[0].replace(/<\/?script>/g, '')); console.log('SYNTAX OK'); }
  catch(e) { console.log('SYNTAX ERROR:', e.message); }
} else console.log('No script found');
