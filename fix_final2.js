const fs = require('fs');

function fix(fp) {
  let html = fs.readFileSync(fp, 'utf8');
  let count = 0;

  // Use backtick strings to avoid quote escaping issues
  // The target patterns contain single quotes and double quotes

  // 1. Fix odds_d - find the input with padding:2px 0;" value="'+odv+'"
  // and add outline:none + onchange handler
  const dOld = `padding:2px 0;" value="'+odv+'" '+(isAdmin?'':'readonly')+'></div>'+`;
  const dNew = `padding:2px 0;outline:none;" value="'+odv+'" '+(isAdmin?'':'readonly')+' onchange="fetch(SB_URL+'/rest/v1/matches?id=eq.'+mid,{method:'PATCH',headers:{'apikey':SB_KEY,'Authorization':'Bearer '+SB_KEY,'Content-Type':'application/json','Prefer':'return=minimal'},body:JSON.stringify({odds_d:parseFloat(this.value)||3.0})}).catch(function(e){})"></div>'+`;

  if (html.includes(dOld)) {
    html = html.replace(dOld, dNew);
    console.log(fp + ': odds_d fixed');
    count++;
  } else {
    console.log(fp + ': odds_d NOT FOUND');
    // Debug: find what's at that position
    const idx = html.indexOf(`padding:2px 0;" value="'+odv+'"`);
    if (idx >= 0) console.log('  Found partial match at', idx, 'got:', JSON.stringify(html.substring(idx, idx+80)));
  }

  // 2. Fix odds_a - same pattern for odds_a
  const aOld = `padding:2px 0;" value="'+oa+'" '+(isAdmin?'':'readonly')+'></div></div>'+`;
  const aNew = `padding:2px 0;outline:none;" value="'+oa+'" '+(isAdmin?'':'readonly')+' onchange="fetch(SB_URL+'/rest/v1/matches?id=eq.'+mid,{method:'PATCH',headers:{'apikey':SB_KEY,'Authorization':'Bearer '+SB_KEY,'Content-Type':'application/json','Prefer':'return=minimal'},body:JSON.stringify({odds_a:parseFloat(this.value)||3.0})}).catch(function(e){})"></div></div>'+`;

  if (html.includes(aOld)) {
    html = html.replace(aOld, aNew);
    console.log(fp + ': odds_a fixed');
    count++;
  } else {
    console.log(fp + ': odds_a NOT FOUND');
  }

  // 3. Fix ms() function for score odds
  const msFunc = html.match(/function ms\(arr,a\)\{[\s\S]*?return arr\.map\(function\(x\)\{[\s\S]*?\}\);\n  \}/);
  if (msFunc) {
    const oldMs = msFunc[0];
    const newMs = `function ms(arr,a){
    var so=typeof m.score_odds==='string'?JSON.parse(m.score_odds):(m.score_odds||{});
    return arr.map(function(x){var ov=so[x]||'';return '<div class="score-item-lg" style="flex-direction:'+a+';';\"><span class="s-lg">'+x+'</span><input type="text" class="so-lg" value="'+ov+'" '+(isAdmin?'':'readonly')+' onchange="var s=m.score_odds||{};if(typeof s===\\'string\\')s=JSON.parse(s);s[\\''+x+'\\']=parseFloat(this.value)||1.01;fetch(SB_URL+\\'/rest/v1/matches?id=eq.\\'+mid,{method:\\'PATCH\\',headers:{\\'apikey\\':SB_KEY,\\'Authorization\\':\\'Bearer \\'+SB_KEY,\\'Content-Type\\':\\'application/json\\',\\'Prefer\\':\\'return=minimal\\'},body:JSON.stringify({score_odds:JSON.stringify(s)})}).catch(function(e){})"' + '></div>';}).join('');\n  }`;
    html = html.replace(oldMs, newMs);
    console.log(fp + ': ms() fixed');
    count++;
  } else {
    console.log(fp + ': ms() NOT FOUND');
  }

  if (count > 0) {
    fs.writeFileSync(fp, html, 'utf8');
    console.log(fp + ': SAVED (' + count + ' changes)');
  }
}

fix('D:/Claude记忆/365BET/index.html');
fix('D:/Claude记忆/DublinBet/index.html');
