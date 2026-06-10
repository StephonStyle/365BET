#!/usr/bin/env python3
import subprocess

with open(r'D:\Claude记忆\365BET\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add getInitOdds before WC_COACHES
old = 'const WC_COACHES'
new = '''var RANK_DATA={Argentina:3,Australia:27,Austria:24,Belgium:9,Bosnia:65,Brazil:6,Canada:30,CapeVerde:69,Colombia:13,Croatia:11,Curacao:82,Czechia:41,DRCongo:46,Ecuador:23,Egypt:29,England:4,France:1,Germany:10,Ghana:74,Haiti:83,Iran:21,Iraq:57,IvoryCoast:34,Japan:18,Jordan:63,Mexico:15,Morocco:8,Netherlands:7,NewZealand:85,Norway:31,Panama:33,Paraguay:40,Portugal:5,Qatar:55,SaudiArabia:61,Scotland:43,Senegal:14,SouthAfrica:60,SouthKorea:25,Spain:2,Sweden:38,Switzerland:19,Tunisia:44,Turkey:22,USA:16,Uruguay:17,Uzbekistan:50,Algeria:28};
var CN2EN={'墨西哥':'Mexico','南非':'SouthAfrica','韩国':'SouthKorea','捷克':'Czechia','加拿大':'Canada','波黑':'Bosnia','卡塔尔':'Qatar','瑞士':'Switzerland','巴西':'Brazil','摩洛哥':'Morocco','海地':'Haiti','苏格兰':'Scotland','美国':'USA','巴拉圭':'Paraguay','澳大利亚':'Australia','土耳其':'Turkey','德国':'Germany','库拉索':'Curacao','科特迪瓦':'IvoryCoast','厄瓜多尔':'Ecuador','荷兰':'Netherlands','日本':'Japan','瑞典':'Sweden','突尼斯':'Tunisia','比利时':'Belgium','埃及':'Egypt','伊朗':'Iran','新西兰':'NewZealand','西班牙':'Spain','佛得角':'CapeVerde','沙特阿拉伯':'SaudiArabia','乌拉圭':'Uruguay','法国':'France','塞内加尔':'Senegal','伊拉克':'Iraq','挪威':'Norway','阿根廷':'Argentina','阿尔及利亚':'Algeria','奥地利':'Austria','约旦':'Jordan','葡萄牙':'Portugal','DR Congo':'DRCongo','乌兹别克斯坦':'Uzbekistan','哥伦比亚':'Colombia','英格兰':'England','克罗地亚':'Croatia','加纳':'Ghana','巴拿马':'Panama'};
function getInitOdds(h,a){
  var he=CN2EN[h]||h; var ae=CN2EN[a]||a;
  var hr=RANK_DATA[he.replace(/ /g,'')]||50, ar=RANK_DATA[ae.replace(/ /g,'')]||50, d=ar-hr;
  var h0,d0,a0;
  if(d>20){h0=1.3+(d-20)*0.01;d0=3.8+(50-d)*0.02;a0=6.0+d*0.05;}
  else if(d>10){h0=1.5+(d-10)*0.02;d0=3.5+(30-d)*0.02;a0=5.0+d*0.03;}
  else if(d>0){h0=1.7+d*0.03;d0=3.3+(20-d)*0.02;a0=4.0+d*0.03;}
  else if(d===0){h0=2.2;d0=3.2;a0=2.2;}
  else if(d>-10){h0=2.0-d*0.03;d0=3.3+d*0.02;a0=3.5-d*0.03;}
  else if(d>-20){h0=2.5-d*0.04;d0=3.5+d*0.02;a0=2.8-d*0.03;}
  else{h0=3.5-d*0.05;d0=3.8+d*0.02;a0=1.5-d*0.02;}
  return {h:Math.round(Math.max(1.1,Math.min(h0,15))*100)/100,d:Math.round(Math.max(2.5,Math.min(d0,10))*100)/100,a:Math.round(Math.max(1.1,Math.min(a0,15))*100)/100};
}
''' + old

if old in html:
    html = html.replace(old, new)
    print("1. getInitOdds added")

# 2. Find and replace the showPredModal function
start = html.find('function showPredModal(mid){')
end = html.find('function closePredModal()', start)
if start > 0 and end > 0:
    new_fn = '''function showPredModal(mid){
  var m=M.find(function(x){return x.id===mid;}); if(!m) return;
  var u=cu(); if(!u){showToast('请先选择身份');showUserSelect();return;}
  var p=getPred(mid,u);
  PRED_CURRENT_MID=mid;
  document.getElementById('predModalTitle').textContent=m.home+' vs '+m.away;
  var od=getInitOdds(m.home,m.away);
  var oh=m.odds_h||od.h||2.0, odv=m.odds_d||od.d||3.0, oa=m.odds_a||od.a||3.0;
  var skHtml=function(sel){return [10,20,30,40,50].map(function(v){return '<span class="stake-btn'+(v===sel?' active':'')+'" data-stake="'+v+'" onclick="selStake(this,'+v+')">'+v+'</span>';}).join('');};
  var ss=function(arr){return arr.map(function(x){return '<div class="score-item-lg"><span class="s-lg">'+x+'</span></div>';}).join('');};
  var wdlStake=p?(p.stake||m.stake||10):10;
  document.getElementById('predModalContent').innerHTML=
    '<div style="font-size:14px;font-weight:700;margin:4px 0 6px;text-align:center;">胜平负</div>'+
    '<div class="wdl-wrap" style="margin-bottom:4px;"><div class="wdl-col" style="flex:0 0 72px;"><span class="wdl-btn '+(p&&p.pick==='H'?'active':'')+'" data-pick="H" onclick="selWdl(this,\\'H\\')">胜</span><span style="display:block;text-align:center;font-size:13px;color:#FFD700;font-weight:700;">'+oh+'</span></div>'+
    '<div class="wdl-col" style="flex:0 0 72px;"><span class="wdl-btn '+(p&&p.pick==='D'?'active':'')+'" data-pick="D" onclick="selWdl(this,\\'D\\')">平</span><span style="display:block;text-align:center;font-size:13px;color:#FFD700;font-weight:700;">'+odv+'</span></div>'+
    '<div class="wdl-col" style="flex:0 0 72px;"><span class="wdl-btn '+(p&&p.pick==='A'?'active':'')+'" data-pick="A" onclick="selWdl(this,\\'A\\')">负</span><span style="display:block;text-align:center;font-size:13px;color:#FFD700;font-weight:700;">'+oa+'</span></div></div>'+
    '<div class="stake-row" style="margin-bottom:4px;"><span class="stake-label" style="font-size:13px;">积分</span><div class="stake-btns" id="stk_'+mid+'">'+skHtml(wdlStake)+'</div><button class="btn btn-primary" onclick="subPredModal()" style="font-size:12px;padding:6px 12px;white-space:nowrap;">提交</button></div>'+
    '<div style="font-size:14px;font-weight:700;margin:6px 0 4px;text-align:center;">比分</div>'+
    '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:3px;"><div><div style="font-size:11px;color:var(--primary);text-align:center;padding:2px 0;font-weight:600;">主胜</div>'+ss(['1:0','2:0','2:1','3:0','3:1','3:2','4:0','4:1','4:2','4:3'])+'</div>'+
    '<div><div style="font-size:11px;color:var(--gold);text-align:center;padding:2px 0;font-weight:600;">平局</div>'+ss(['0:0','1:1','2:2','3:3','4:4'])+'</div>'+
    '<div><div style="font-size:11px;color:var(--red);text-align:center;padding:2px 0;font-weight:600;">客胜</div>'+ss(['0:1','0:2','1:2','0:3','1:3','2:3','0:4','1:4','2:4','3:4'])+'</div></div>'+
    '<div class="stake-row" style="margin-top:4px;"><span class="stake-label" style="font-size:13px;">积分</span><div class="stake-btns" id="scr_stk_'+mid+'">'+skHtml(10)+'</div><button class="btn btn-primary" onclick="showToast(\'\\u6bd4\\u5206\\u9884\\u6d4b\\u529f\\u80fd\\u5f85\\u5b8c\\u5584\')" style="font-size:12px;padding:6px 12px;white-space:nowrap;">提交</button></div>';
  document.getElementById('predModal').classList.add('show');
}'''
    html = html[:start] + new_fn + html[end:]
    print("2. showPredModal updated")

# 3. Add score grid CSS if not present
if '.score-item-lg' not in html:
    css = '\n.score-item-lg { display:flex; align-items:center; gap:2px; padding:3px 4px; border-radius:4px; background:var(--card2); margin-bottom:2px; min-height:26px; }\n.score-item-lg .s-lg { flex:1; text-align:center; font-size:12px; font-weight:600; }\n.score-item-lg .so-lg { width:32px; border:none; background:transparent; color:var(--gold); text-align:center; font-size:10px; font-weight:600; }\n'
    html = html.replace('</style>', css + '\n</style>')
    print("3. Score grid CSS added")

with open(r'D:\Claude记忆\365BET\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

i1 = html.find('<script>')
i2 = html.find('</script>')
with open(r'C:\Users\HP\AppData\Local\Temp\bet_check.js','w',encoding='utf-8') as f:
    f.write(html[i1+8:i2])
r = subprocess.run(['node','-c',r'C:\Users\HP\AppData\Local\Temp\bet_check.js'], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('JS:' + ('PASS' if r.returncode == 0 else 'FAIL'))
if r.returncode != 0: print(r.stderr[:400])
