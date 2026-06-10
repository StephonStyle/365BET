const fs = require('fs');
// Read file into buffer for byte-level replacement
function fix(fp) {
  let html = fs.readFileSync(fp, 'utf8');
  let count = 0;

  // Pattern 1: odds_d - no outline, no onchange
  // Find the unique text start
  const start = 'padding:2px 0;" value="';

  // Find all occurrences of start
  let pos = -1;
  while ((pos = html.indexOf(start, pos + 1)) >= 0) {
    const next60 = html.substring(pos, pos + 60);
    // Check if this is odds_d (contains odv)
    if (next60.includes("odv") && !next60.includes("outline")) {
      // Find the end of the tag
      const tagEnd = html.indexOf("></div>", pos);
      if (tagEnd > 0) {
        const oldPart = html.substring(pos, tagEnd + 7);
        // Build new part: same but with outline:none and onchange
        const newPart = 'padding:2px 0;outline:none;" value="'+odv+'" '+(isAdmin?'':'readonly')+' onchange="fetch(SB_URL+\'/rest/v1/matches?id=eq.\'+mid,{method:\'PATCH\',headers:{\'apikey\':SB_KEY,\'Authorization\':\'Bearer \'+SB_KEY,\'Content-Type\':\'application/json\',\'Prefer\':\'return=minimal\'},body:JSON.stringify({odds_d:parseFloat(this.value)||3.0})}).catch(function(e){})"></div>';
        html = html.substring(0, pos) + newPart + html.substring(tagEnd + 7);
        console.log(fp + ': odds_d fixed');
        count++;
        break;
      }
    }
  }

  // Pattern 2: odds_a - no outline, no onchange
  pos = -1;
  while ((pos = html.indexOf(start, pos + 1)) >= 0) {
    const next60 = html.substring(pos, pos + 60);
    if (next60.includes("oa") && !next60.includes("outline")) {
      const tagEnd = html.indexOf("></div></div>", pos);
      if (tagEnd > 0) {
        const oldPart = html.substring(pos, tagEnd + 15);
        const newPart = 'padding:2px 0;outline:none;" value="'+oa+'" '+(isAdmin?'':'readonly')+' onchange="fetch(SB_URL+\'/rest/v1/matches?id=eq.\'+mid,{method:\'PATCH\',headers:{\'apikey\':SB_KEY,\'Authorization\':\'Bearer \'+SB_KEY,\'Content-Type\':\'application/json\',\'Prefer\':\'return=minimal\'},body:JSON.stringify({odds_a:parseFloat(this.value)||3.0})}).catch(function(e){})"></div></div>';
        html = html.substring(0, pos) + newPart + html.substring(tagEnd + 15);
        console.log(fp + ': odds_a fixed');
        count++;
        break;
      }
    }
  }

  // Pattern 3: ms() function - update for score odds
  const msStart = 'function ms(arr,a){\n    return arr.map(function(x){return ';
  const msIdx = html.indexOf(msStart);
  if (msIdx >= 0) {
    const msOldEnd = "';}).join('');\n  }";
    const msEnd = html.indexOf(msOldEnd, msIdx);
    if (msEnd >= 0) {
      const oldMs = html.substring(msIdx, msEnd + msOldEnd.length);
      console.log(fp + ': found ms() (len=' + oldMs.length + ')');
      // Build new ms function
      const newMs =
`function ms(arr,a){
    var so=typeof m.score_odds==='string'?JSON.parse(m.score_odds):(m.score_odds||{});
    return arr.map(function(x){var ov=so[x]||'';return '<div class="score-item-lg" style="flex-direction:'+a+';';\"><span class="s-lg">'+x+'</span><input type="text" class="so-lg" value="'+ov+'" '+(isAdmin?'':'readonly')+' onchange="var s=m.score_odds||{};if(typeof s===\\'string\\')s=JSON.parse(s);s[\\''+x+'\\']=parseFloat(this.value)||1.01;fetch(SB_URL+\\'/rest/v1/matches?id=eq.\\'+mid,{method:\\'PATCH\\',headers:{\\'apikey\\':SB_KEY,\\'Authorization\\':\\'Bearer \\'+SB_KEY,\\'Content-Type\\':\\'application/json\\',\\'Prefer\\':\\'return=minimal\\'},body:JSON.stringify({score_odds:JSON.stringify(s)})}).catch(function(e){})"' + '></div>';}).join('');\n  }`;
      html = html.substring(0, msIdx) + newMs + html.substring(msEnd + msOldEnd.length);
      console.log(fp + ': ms() fixed');
      count++;
    }
  }

  if (count > 0) {
    fs.writeFileSync(fp, html, 'utf8');
    console.log(fp + ': SAVED (' + count + ' changes)');
  } else {
    console.log(fp + ': no changes needed');
  }
}

fix('D:/Claude记忆/365BET/index.html');
fix('D:/Claude记忆/DublinBet/index.html');
