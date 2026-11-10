(function(){"use strict";
var P=AAW_B.P,PL=AAW_B.PL,MODES=AAW_B.MODES,VIN=AAW_B.VIN;
var root=document.getElementById("builder");if(!root)return;
var CAN_PRICE=!!(window.AAW&&window.AAW.builderShowPricing);
var S={p:"b58f",m:"street",hp:470,c:false,price:false,vin:"",vinLabel:""};
var $=function(i){return document.getElementById(i)};
function fmt(n){return "$"+(Math.round(n/100)*100).toLocaleString()}
function plat(){return PL.filter(function(x){return x.id===S.p})[0]}
// platforms
$("plats").innerHTML=PL.map(function(p){return '<button class="plat" data-id="'+p.id+'"><span class="tick"></span><div class="gen">'+p.gen+'</div><div class="code">'+p.code+'</div><h3>'+p.name+'</h3><p>'+p.models+'</p><div class="stock"><span>Factory '+p.fac+' hp</span><strong>~'+p.stock+' whp</strong></div></button>'}).join("");
$("plats").onclick=function(e){var b=e.target.closest(".plat");if(!b)return;S.p=b.dataset.id;var p=plat();S.hp=p.tiers[3][0];setup();render()};
$("modes").innerHTML=MODES.map(function(m){return '<button class="mode" data-id="'+m[0]+'"><svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">'+m[3]+'</svg><b>'+m[1]+'</b><small>'+m[2]+'</small></button>'}).join("");
$("modes").onclick=function(e){var b=e.target.closest(".mode");if(!b)return;S.m=b.dataset.id;render()};
$("comp").onclick=function(){S.c=!S.c;render()};
if(CAN_PRICE){$("ptog").hidden=false;$("ptog").onclick=function(){S.price=!S.price;render()}}
$("range").oninput=function(){S.hp=+this.value;render()};
// gauge geometry
var CX=200,CY=200,R=150,A0=-225,A1=45;
function pol(a,r){a=a*Math.PI/180;return [CX+r*Math.cos(a),CY+r*Math.sin(a)]}
function arc(v0,v1,max){var a=A0+(A1-A0)*v0/max,b=A0+(A1-A0)*v1/max,p=pol(a,R),q=pol(b,R);return "M"+p[0]+" "+p[1]+" A"+R+" "+R+" 0 "+((b-a)>180?1:0)+" 1 "+q[0]+" "+q[1]}
function gmax(){var t=plat().tiers;return Math.ceil(t[t.length-1][0]/100)*100}
function setup(){var p=plat(),max=gmax(),r=$("range");r.min=p.stock;r.max=p.tiers[p.tiers.length-1][0];if(S.hp>r.max)S.hp=+r.max;if(S.hp<p.stock)S.hp=p.stock;
 $("g-track").setAttribute("d",arc(0,max,max));$("g-stock").setAttribute("d",arc(0,p.stock,max));
 var t="";for(var v=0;v<=max;v+=100){var a=A0+(A1-A0)*v/max,o=pol(a,R+14),i=pol(a,R+22),l=pol(a,R+38);t+='<line class="g-tick" x1="'+o[0]+'" y1="'+o[1]+'" x2="'+i[0]+'" y2="'+i[1]+'"/>'+((v%(max>1000?200:100)===0)?'<text class="g-lbl" x="'+l[0]+'" y="'+(l[1]+4)+'" text-anchor="middle">'+v+'</text>':'')}
 $("g-ticks").innerHTML=t;
 $("g-marks").innerHTML=p.tiers.map(function(x,i){var c=pol(A0+(A1-A0)*x[0]/max,R);return '<circle class="g-mark" data-hp="'+x[0]+'" cx="'+c[0]+'" cy="'+c[1]+'" r="6"><title>'+x[1]+' · '+x[0]+' hp</title></circle>'}).join("");
 $("stagechips").innerHTML='<button data-hp="'+p.stock+'">Stock</button>'+p.tiers.map(function(x){return '<button data-hp="'+x[0]+'">'+x[1]+'</button>'}).join("");
 // dyno grid
 var g="";for(var i=0;i<=6;i++){var y=30+i*50;g+='<line class="d-grid" x1="56" y1="'+y+'" x2="700" y2="'+y+'"/>'}
 for(var rpm=2000;rpm<=7000;rpm+=1000){var x=56+(rpm-2000)/5000*644;g+='<line class="d-grid" x1="'+x+'" y1="30" x2="'+x+'" y2="330"/><text class="d-ax" x="'+x+'" y="350" text-anchor="middle">'+rpm+'</text>'}
 $("d-grid").innerHTML=g+'<text class="d-ax" x="8" y="22">WHP</text><text class="d-ax" x="700" y="22" text-anchor="end">RPM</text><g id="d-ylab"></g>';
}
document.addEventListener("click",function(e){var b=e.target.closest("[data-hp]");if(b&&(b.closest("#stagechips")||b.closest("#g-marks"))){S.hp=+b.dataset.hp;render()}});
function curve(peak,spoolLate){var pts=[];for(var rpm=2000;rpm<=7000;rpm+=125){var x=(rpm-2000)/5000;var sp=spoolLate?0.32:0.18;var rise=1/(1+Math.exp(-(x-sp)*11));var fall=1-Math.max(0,x-0.78)*0.55;pts.push([rpm,peak*rise*fall/0.985])}return pts}
function path(pts,ymax,close){var d=pts.map(function(p,i){var x=56+(p[0]-2000)/5000*644,y=330-p[1]/ymax*300;return (i?"L":"M")+x.toFixed(1)+" "+y.toFixed(1)}).join(" ");return close?d+" L700 330 L56 330 Z":d}
function build(){var p=plat(),idx=-1;for(var i=0;i<p.tiers.length;i++){if(p.tiers[i][0]>=S.hp){idx=i;break}}if(S.hp<=p.stock)idx=-1;
 var stops=[],have=[];for(var j=0;j<=idx;j++){var t=p.tiers[j],add=[];t[2].forEach(function(k){if(k==="dp"&&S.c)k="dpr";if(have.indexOf(k)<0){have.push(k);add.push(k)}});(t[3]||[]).forEach(function(k){var a=have.indexOf(k);if(a>=0)have.splice(a,1)});stops.push({n:t[1],hp:t[0],parts:add,drop:t[3]||[]})}
 var tier=idx>=0?p.tiers[idx]:null,tgt=tier?tier[0]:p.stock,sup=[];
 if(tier&&tgt>p.tlim)sup.push(p.dct?"dcc":"tb");
 if(S.m==="street")sup.push("pads");
 if(S.m==="track"){sup.push("pads","tires","align");if(have.indexOf("oil")<0&&tier)sup.push("oil");sup.push("tcool")}
 if(S.m==="drag"){sup.push("radials");if(tgt>p.stock*1.4)sup.push("axles","ds")}
 if(S.m==="show")sup.push("catback");
 if(S.c&&(S.m==="track"||S.m==="drag"))sup.push("harness");
 var all=have.concat(sup),lo=0,hi=0,hrs=2.5;all.forEach(function(k){var x=P[k];lo+=x[2]*0.82;hi+=x[2]*1.25;hrs+=x[3]});
 return {p:p,tier:tier,tgt:tgt,stops:stops,sup:sup,lo:lo+hrs*155*.9,hi:hi+hrs*155*1.15,hrs:hrs,have:have}}
function partHTML(k){var x=P[k],race=x[4];return '<div class="part'+(race?' race':'')+'"><i></i><div>'+x[0]+(race?'<span class="rt">OFF-ROAD ONLY</span>':'')+'<small>'+x[1]+'</small></div></div>'}
function render(){var b=build(),p=b.p,max=gmax();
 document.querySelectorAll(".plat").forEach(function(e){e.classList.toggle("sel",e.dataset.id===S.p)});
 document.querySelectorAll(".mode").forEach(function(e){e.classList.toggle("sel",e.dataset.id===S.m)});
 $("comp").classList.toggle("on",S.c);$("comp").setAttribute("aria-checked",S.c);
 var r=$("range");r.value=S.hp;r.style.setProperty("--f",((S.hp-r.min)/(r.max-r.min)*100)+"%");
 // gauge
 var len=$("g-fill").getTotalLength?null:null;$("g-fill").setAttribute("d",arc(0,Math.max(S.hp,1),max));
 $("needle").style.transform="rotate("+((A1-A0)*S.hp/max+A0+90)+"deg)";
 document.querySelectorAll(".g-mark").forEach(function(m){m.classList.toggle("hit",+m.dataset.hp<=b.tgt&&b.tier)});
 document.querySelectorAll("#stagechips button").forEach(function(c){c.classList.toggle("on",+c.dataset.hp===b.tgt)});
 $("hp").textContent=S.hp.toLocaleString();$("gain").textContent=S.hp>p.stock?"+"+(S.hp-p.stock)+" whp over stock":"Stock power";
 // dyno
 var step=Math.ceil(b.tgt/5/50)*50,ymax=step*6,big=b.have.indexOf("big")>=0||b.have.indexOf("tw")>=0||b.have.indexOf("hy")>=0;
 $("d-stock").setAttribute("d",path(curve(p.stock,false),ymax));$("d-tgt").setAttribute("d",path(curve(b.tgt,big),ymax));$("d-area").setAttribute("d",path(curve(b.tgt,big),ymax,true));
 var yl="";for(var i=0;i<=6;i++){yl+='<text class="d-ax" x="48" y="'+(334-i*50)+'" text-anchor="end">'+(step*i)+'</text>'}$("d-ylab").innerHTML=yl;
 $("k1").textContent="+"+Math.round((b.tgt/p.stock-1)*100)+"%";$("k2").textContent=b.tier?b.tier[1]:"Stock";
 $("k3").textContent=b.have.indexOf("flex")>=0?"E85 / 93":"93 octane";
 // road
 var html="";b.stops.forEach(function(s,i){var fin=i===b.stops.length-1;html+='<div class="stop'+(fin?' final':'')+'" data-n="'+(i+1)+'" style="animation-delay:'+(i*60)+'ms"><div class="stop-h"><h4>'+s.n+'</h4><span>~'+s.hp+' whp</span></div><div class="parts">'+s.parts.map(partHTML).join("")+'</div></div>'});
 if(!b.stops.length)html='<div class="stop final" data-n="0"><div class="stop-h"><h4>Stock power</h4><span>'+p.stock+' hp</span></div><p style="margin:0;color:var(--muted)">Move the needle to start your build.</p></div>';
 $("road").innerHTML=html;
 $("supportwrap").innerHTML=b.sup.length?'<div class="support">Supporting mods for how you drive</div><div class="parts">'+b.sup.map(partHTML).join("")+'</div>':"";
 // summary
 var mname={};MODES.forEach(function(m){mname[m[0]]=m[1]});
 $("s-car").textContent=p.code+" "+p.gen.split(" · ")[0]+" · "+p.trans;$("s-stage").textContent=b.tier?b.tier[1]:"Stock";
 $("s-sub").textContent="~"+b.tgt+" whp · "+mname[S.m]+(S.c?" · Competition":"");
 var top=p.tiers[p.tiers.length-1][0];$("s-bar").style.width=(b.tgt/top*100)+"%";$("s-stockmark").style.left=(p.stock/top*100)+"%";
 $("s-stock").textContent="Stock "+p.stock;$("s-max").textContent="Max "+top.toLocaleString();
 $("psw").classList.toggle("on",S.price);
 $("pbody").innerHTML=(CAN_PRICE&&S.price)?'<b>'+fmt(b.lo)+' to '+fmt(b.hi)+'</b><p>Parts + ~'+Math.round(b.hrs)+' hrs labor. Final quote after a health check.</p>':'<span class="quote">Custom quote</span><p>We price every build after a pre-build health check.</p>';
 var f=[];if(b.have.indexOf("flex")>=0)f.push(["","Built around ethanol blends (E30 to E85). Flex fuel lets you run pump gas too, at lower power."]);
 if(S.c)f.push(["w","Competition build. Off-road use only, signed acknowledgment required."]);else if(b.tier)f.push(["","Street build: catted parts, tuned to stay free of warning lights."]);
 if(b.have.indexOf("hub")>=0)f.push(["w","S55 crank hub gets fixed before we add this torque."]);
 if(b.have.indexOf("built")>=0)f.push(["","Built-motor builds are quoted one-on-one. Our own B58 340i makes 1,300 hp."]);
 $("flags").innerHTML=f.map(function(x){return '<div class="flag '+x[0]+'">'+x[1]+'</div>'}).join("");
 var pr=$("prog").children;for(var k=0;k<4;k++)pr[k].classList.add("on");
 var mb=$("mbar");mb.hidden=false;$("mbar-t").textContent=(b.tier?b.tier[1]:"Stock")+" · ~"+b.tgt+" whp";
 LAST=b;saveHash();
}
var LAST=null;
function sheet(){var b=LAST,p=b.p,mname={};MODES.forEach(function(m){mname[m[0]]=m[1]});
 var L=["AUTO ADDICT WORKS BUILD SHEET","Vehicle: "+(S.vinLabel||p.code+" "+p.name)+(S.vin?" (VIN "+S.vin+")":""),"Platform: "+p.code+" "+p.gen+" · "+p.trans,
  "Goal: "+(b.tier?b.tier[1]+" ~"+b.tgt+" whp":"Stock")+" · "+mname[S.m]+(S.c?" · OFF-ROAD / COMPETITION BUILD":""),"","Build path:"];
 b.stops.forEach(function(s){L.push(" "+s.n+" (~"+s.hp+" whp): "+s.parts.map(function(k){return P[k][0]}).join(", "))});
 if(b.sup.length)L.push(" Supporting: "+b.sup.map(function(k){return P[k][0]}).join(", "));
 L.push("","Link: "+location.href);return L.join("\n")}
function copy(t,btn,label){(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){if(btn){var o=btn.textContent;btn.textContent=label||"Copied ✓";setTimeout(function(){btn.textContent=o},1800)}}).catch(function(){window.prompt("Copy this:",t)})}
$("r-copy").onclick=function(){copy(sheet(),this)};
$("r-link").onclick=function(e){e.preventDefault();copy(location.href,this,"Link copied ✓")};
$("r-send").onclick=function(){try{sessionStorage.setItem("aaw-build",sheet());sessionStorage.setItem("aaw-build-vehicle",JSON.stringify(S.vinLabel||(LAST.p.code+" "+LAST.p.name)))}catch(e){}
 if(window.dataLayer)window.dataLayer.push({event:"build_request",platform:S.p,hp:S.hp,use:S.m,competition:S.c});location.href=root.getAttribute("data-contact")};
function saveHash(){try{history.replaceState(null,"","#p="+S.p+"&m="+S.m+"&hp="+S.hp+(S.c?"&c=1":""))}catch(e){}}
function loadHash(){var q={};location.hash.replace(/^#/,"").split("&").forEach(function(kv){var a=kv.split("=");if(a[0])q[a[0]]=decodeURIComponent(a[1]||"")});
 if(q.p&&PL.some(function(x){return x.id===q.p})){S.p=q.p;S.m=q.m||S.m;S.c=q.c==="1";S.hp=+q.hp||S.hp}}
// VIN
function vmsg(t,c){var m=$("vin-msg");m.textContent=t;m.className="vinmsg"+(c?" "+c:"")}
function decode(){var v=$("vin").value.trim().toUpperCase().replace(/[^A-Z0-9]/g,"");
 if(!/^[A-HJ-NPR-Z0-9]{17}$/.test(v)){vmsg("A VIN is 17 letters and numbers (no I, O or Q).","err");return}
 vmsg("Decoding…");
 fetch("https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/"+v+"?format=json").then(function(r){return r.json()}).then(function(j){
  var d=j.Results&&j.Results[0];if(!d||!d.Make)throw 0;
  var yr=+d.ModelYear||0,txt=[d.Model,d.Series,d.Trim,d.Series2].filter(Boolean).join(" "),desc=[yr||"",d.Make==="BMW"?"BMW":d.Make,d.Model,d.Trim||d.Series].filter(Boolean).join(" ");
  S.vin=v;S.vinLabel=desc;var hit=null;
  if(/BMW/i.test(d.Make))for(var i=0;i<VIN.length;i++){var r=VIN[i];if(r.re.test(txt)&&yr>=r.y[0]&&yr<=r.y[1]){hit=r.p;break}}
  if(hit){S.p=hit;var p=PL.filter(function(x){return x.id===hit})[0];S.hp=p.tiers[Math.min(3,p.tiers.length-1)][0];setup();render();vmsg("✓ "+desc+": matched to "+p.code+" "+p.gen.split(" · ")[0]+".","ok")}
  else vmsg(desc+" isn't in the planner yet. Send it to us through the contact page for a custom quote.","err");
 }).catch(function(){vmsg("Couldn't decode that VIN right now. Pick your platform above instead.","err")})}
$("vin-go").onclick=decode;$("vin").addEventListener("keydown",function(e){if(e.key==="Enter"){e.preventDefault();decode()}});
loadHash();setup();render();

})();
