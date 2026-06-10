#!/usr/bin/env python3
import subprocess, re

with open(r'D:\Claude记忆\365BET\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('function showPredModal(mid){')
end = html.find('function closePredModal()', start)

if start < 0 or end < 0:
    print("ERROR: Could not find showPredModal")
    exit(1)

new_fn = r'''function showPredModal(mid){
  var m=M.find(function(x){return x.id===mid;}); if(!m) return;
  var u=cu(); if(!u){showToast('请先选择身份');showUserSelect();return;}
  var p=getPred(mid,u);
  PRED_CURRENT_MID=mid;
  document.getElementById('predModalTitle').textContent=m.home+' vs '+m.away;
  var od=getInitOdds(m.home,m.away);
  var oh=m.odds_h||od.h||2.0, odv=m.odds_d||od.d||3.0, oa=m.odds_a||od.a||3.0;
  var wdlStake=p?(p.stake||m.stake||10):10;
  var pl={'H':'胜','D':'平','A':'负'};
  var wdlPred=p?'<div style="font-size:12px;color:var(--gold);margin:4px 0;text-align:center;">✅ 已预测 '+wdlStake+'分 '+pl[p.pick]+'</div>':'';
  function ms(arr,a){
    return arr.map(function(x){return '<div class="score-item-lg" style="flex-direction:'+a+';"><span class="s-lg">'+x+'</span><input type="text" class="so-lg" value="" '+(isAdmin?'':'readonly')+'></div>';}).join('');
  }
  function skHtml(sel,id){
    return '<span class="stake-label" style="font-size:13px;">积分</span><div class="stake-btns" id="'+id+'">'+
      [10,20,30,40,50].map(function(v){return '<span class="stake-btn'+(v===sel?' active':'')+'" data-stake="'+v+'" onclick="selStake(this,'+v+')">'+v+'</span>';}).join('')+
      '</div><button class="btn btn-primary" onclick="subPredModal()" style="font-size:12px;padding:6px 12px;white-space:nowrap;">提交</button>';
  }
  document.getElementById('predModalContent').innerHTML=
    '<div style="font-size:14px;font-weight:700;margin:4px 0 6px;text-align:center;">胜平负</div>'+
    '<div class="wdl-wrap" style="margin-bottom:4px;"><div class="wdl-col" style="flex:0 0 72px;"><span class="wdl-btn '+(p&&p.pick==='H'?'active':'')+'" data-pick="H" onclick="selWdl(this,\'H\')">胜</span><span style="display:block;text-align:center;font-size:13px;color:#FFD700;font-weight:700;">'+oh+'</span></div>'+
    '<div class="wdl-col" style="flex:0 0 72px;"><span class="wdl-btn '+(p&&p.pick==='D'?'active':'')+'" data-pick="D" onclick="selWdl(this,\'D\')">平</span><span style="display:block;text-align:center;font-size:13px;color:#FFD700;font-weight:700;">'+odv+'</span></div>'+
    '<div class="wdl-col" style="flex:0 0 72px;"><span class="wdl-btn '+(p&&p.pick==='A'?'active':'')+'" data-pick="A" onclick="selWdl(this,\'A\')">负</span><span style="display:block;text-align:center;font-size:13px;color:#FFD700;font-weight:700;">'+oa+'</span></div></div>'+
    '<div class="stake-row" style="margin-bottom:4px;">'+skHtml(wdlStake,'wdl_'+mid)+'</div>'+
    wdlPred+
    '<div style="font-size:14px;font-weight:700;margin:6px 0 4px;text-align:center;">比分</div>'+
    '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:3px;">'+
      '<div><div style="font-size:11px;color:var(--primary);text-align:left;padding:2px 0;font-weight:600;">主胜</div>'+ms(['1:0','2:0','2:1','3:0','3:1','3:2','4:0','4:1','4:2','4:3'],'row')+'</div>'+
      '<div><div style="font-size:11px;color:var(--gold);text-align:left;padding:2px 0;font-weight:600;">平局</div>'+ms(['0:0','1:1','2:2','3:3','4:4'],'row')+'</div>'+
      '<div><div style="font-size:11px;color:var(--red);text-align:right;padding:2px 0;font-weight:600;">客胜</div>'+ms(['0:1','0:2','1:2','0:3','1:3','2:3','0:4','1:4','2:4','3:4'],'row-reverse')+'</div>'+
    '</div>'+
    '<div class="stake-row" style="margin-top:4px;"><span class="stake-label" style="font-size:13px;">积分</span><div class="stake-btns" id="scr_'+mid+'">'+[10,20,30,40,50].map(function(v){return '<span class="stake-btn'+(v===10?' active':'')+'" data-stake="'+v+'" onclick="selStake(this,'+v+')">'+v+'</span>';}).join('')+'</div><button class="btn btn-primary" onclick="showToast(\'比分功能待完善\')" style="font-size:12px;padding:6px 12px;white-space:nowrap;">提交</button></div>'+
    '<div style="font-size:11px;color:var(--text2);text-align:center;margin-top:4px;">比分预测功能待完善</div>';
  document.getElementById('predModal').classList.add('show');
}'''

html = html[:start] + new_fn + html[end:]

# Also update score-item-lg CSS for flex-direction support
old_css = '.score-item-lg { display:flex; align-items:center; gap:2px; padding:3px 4px; border-radius:4px; background:var(--card2); margin-bottom:2px; min-height:26px; }'
new_css = '.score-item-lg { display:flex; align-items:center; gap:2px; padding:3px 4px; border-radius:4px; background:var(--card2); margin-bottom:2px; min-height:26px; }'
# Add the so-lg CSS if not present
if '.so-lg' not in html:
    add_css = '\n.score-item-lg .s-lg { flex:1; text-align:center; font-size:12px; font-weight:600; }\n.score-item-lg .so-lg { width:36px; padding:1px 0; border-radius:3px; border:1px solid var(--border); background:var(--card2); color:var(--gold); text-align:center; font-size:10px; font-weight:600; }\n.score-item-lg .so-lg[readonly] { opacity:0.5; border-color:transparent; background:transparent; pointer-events:none; }\n'
    html = html.replace('</style>', add_css + '</style>')

with open(r'D:\Claude记忆\365BET\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

i1 = html.find('<script>')
i2 = html.find('</script>')
with open(r'C:\Users\HP\AppData\Local\Temp\bet_check.js','w',encoding='utf-8') as f:
    f.write(html[i1+8:i2])
r = subprocess.run(['node','-c',r'C:\Users\HP\AppData\Local\Temp\bet_check.js'], capture_output=True, text=True)
if r.returncode == 0:
    print('JS: PASS')
else:
    print('JS: FAIL')
    for line in r.stderr.split('\n'):
        if 'SyntaxError' in line:
            print(line[:300])
            break
