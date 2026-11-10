(function(){
"use strict";
var P=window.AAW_PARTS, PLATS=window.AAW_PLATFORMS, RULES=window.AAW_VIN_RULES, USES=window.AAW_USES, EXTRAS=window.AAW_EXTRAS;
var RATE=(window.AAW&&window.AAW.laborRate)||155;
var root=document.getElementById('builder'); if(!root)return;
var $=function(id){return document.getElementById(id)};
var S={p:null,t:null,u:"daily",hp:null,c:false,x:[],vin:"",vinLabel:""};
var GROUP_ORDER=["Baseline","Tune & Software","Induction & Exhaust","Ignition","Fuel","Turbo","Engine","Cooling","Drivetrain","Brakes & Chassis","Safety"];

function fmt(n){return "$"+(Math.round(n/50)*50).toLocaleString("en-US")}
function plat(id){for(var i=0;i<PLATS.length;i++)if(PLATS[i].id===id)return PLATS[i];return null}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}

/* ---------- selects ---------- */
var makes=[];PLATS.forEach(function(p){if(makes.indexOf(p.make)<0)makes.push(p.make)});
var mk=$("make"),pl=$("platform"),tr=$("trans");
mk.innerHTML='<option value="">Select make</option>'+makes.map(function(m){return '<option>'+esc(m)+'</option>'}).join("");
function fillPlatforms(make){
  var list=PLATS.filter(function(p){return p.make===make});
  pl.innerHTML='<option value="">'+(make?"Select model / engine":"—")+'</option>'+list.map(function(p){return '<option value="'+p.id+'">'+esc(p.label)+'</option>'}).join("");
  pl.disabled=!make;
}
function fillTrans(p){
  tr.innerHTML=p?p.trans.map(function(t){return '<option value="'+t.id+'">'+esc(t.n)+'</option>'}).join(""):'<option>—</option>';
  tr.disabled=!p;
}
mk.addEventListener("change",function(){fillPlatforms(mk.value);setPlatform(null)});
pl.addEventListener("change",function(){setPlatform(pl.value||null)});
tr.addEventListener("change",function(){S.t=tr.value;render()});

function setPlatform(id,keepHp){
  var p=plat(id);S.p=p?p.id:null;fillTrans(p);S.t=p?p.trans[0].id:null;
  if(p){
    var r=$("power");r.min=p.stock;r.max=p.tiers[p.tiers.length-1].hp;r.step=10;
    if(!keepHp||S.hp==null||S.hp<p.stock||S.hp>r.max)S.hp=p.tiers[0].hp;
    r.value=S.hp;$("hp-min").textContent="Stock ~"+p.stock+" hp";$("hp-max").textContent=r.max+" hp";
  }
  render();
}

/* ---------- tabs ---------- */
root.querySelectorAll('[role=tab]').forEach(function(b){b.addEventListener("click",function(){
  root.querySelectorAll('[role=tab]').forEach(function(x){x.setAttribute("aria-selected",x===b)});
  root.querySelectorAll('[data-pane]').forEach(function(p){p.hidden=p.getAttribute("data-pane")!==b.getAttribute("data-tab")});
})});

/* ---------- chips ---------- */
function chips(el,items,type,name,isOn){
  el.innerHTML=items.map(function(it){
    return '<label class="chip"'+(it.race?' data-race="1"':'')+'><input type="'+type+'" name="'+name+'" value="'+it.id+'"'+(isOn(it.id)?" checked":"")+'><span>'+esc(it.n)+'<small>'+esc(it.d)+'</small></span></label>';
  }).join("");
}
chips($("use"),USES,"radio","use",function(id){return id===S.u});
function drawExtras(){chips($("extras"),EXTRAS.filter(function(x){return !x.race||S.c}),"checkbox","extra",function(id){return S.x.indexOf(id)>=0})}
drawExtras();
$("use").addEventListener("change",function(e){S.u=e.target.value;render()});
$("extras").addEventListener("change",function(){S.x=[].slice.call(document.querySelectorAll('input[name=extra]:checked')).map(function(i){return i.value});render()});
$("compete").addEventListener("change",function(e){S.c=e.target.checked;if(!S.c)S.x=S.x.filter(function(x){return x!=="seat_harness"});drawExtras();render()});
var range=$("power");
range.addEventListener("input",function(){S.hp=+range.value;render()});

/* ---------- VIN ---------- */
$("vin-go").addEventListener("click",decode);
$("vin").addEventListener("keydown",function(e){if(e.key==="Enter"){e.preventDefault();decode()}});
function vmsg(t,c){var m=$("vin-msg");m.textContent=t;m.className="vinmsg"+(c?" "+c:"")}
function decode(){
  var v=$("vin").value.trim().toUpperCase().replace(/[^A-Z0-9]/g,"");
  if(!/^[A-HJ-NPR-Z0-9]{17}$/.test(v)){vmsg("A VIN is 17 letters and numbers (no I, O or Q).","err");return}
  vmsg("Decoding…");
  fetch("https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/"+v+"?format=json")
   .then(function(r){return r.json()}).then(function(j){
     var d=j.Results&&j.Results[0];if(!d||!d.Make){throw 0}
     var yr=+d.ModelYear||0,make=d.Make||"",txt=[d.Model,d.Series,d.Trim,d.Series2].filter(Boolean).join(" ");
     var desc=[yr||"",titleCase(make),d.Model,d.Trim||d.Series].filter(Boolean).join(" ");
     S.vin=v;S.vinLabel=desc;
     var hit=null;for(var i=0;i<RULES.length;i++){var r=RULES[i];if(r.make.test(make)&&r.re.test(txt)&&yr>=r.y[0]&&yr<=r.y[1]){hit=r.p;break}}
     if(hit){var p=plat(hit);mk.value=p.make;fillPlatforms(p.make);pl.value=p.id;setPlatform(p.id);vmsg("✓ "+desc+" — matched to "+p.label.split(" — ")[0]+".","ok")}
     else vmsg(desc+" isn't in our build planner yet — pick the closest platform, or send it to us for a custom quote.","err");
   }).catch(function(){vmsg("Couldn't decode that VIN right now. Select your model instead.","err")});
}
function titleCase(s){return s.toLowerCase().replace(/\b\w/g,function(c){return c.toUpperCase()}).replace(/^Bmw$/,"BMW")}

/* ---------- build logic ---------- */
function compute(){
  var p=plat(S.p);if(!p)return null;
  var t=p.trans.filter(function(x){return x.id===S.t})[0]||p.trans[0];
  var hp=S.hp, tierIdx=-1;
  for(var i=0;i<p.tiers.length;i++){if(p.tiers[i].hp>=hp){tierIdx=i;break}}
  if(hp<=p.stock)tierIdx=-1; else if(tierIdx<0)tierIdx=p.tiers.length-1;
  var set=[],notes=[],flags=[];
  function add(k){if(k==="dp")k=S.c?"dp_catless":"dp_catted";if(set.indexOf(k)<0)set.push(k)}
  function rem(k){var i=set.indexOf(k);if(i>=0)set.splice(i,1)}
  for(var j=0;j<=tierIdx;j++){(p.tiers[j].a||[]).forEach(add);(p.tiers[j].r||[]).forEach(rem);if(p.tiers[j].note&&j===tierIdx)notes.push(p.tiers[j].note)}
  var tier=tierIdx>=0?p.tiers[tierIdx]:null, target=tier?tier.hp:p.stock;
  var powered=tierIdx>=0;
  // transmission
  var lim=t.limit*(S.u==="drag"?0.9:1);
  if(t.type==="auto"&&powered&&tierIdx>=1)add("trans_tune");
  if(t.type==="dct"&&powered&&tierIdx>=1)add("dct_tune");
  if(t.type!=="dct")rem("dct_tune");
  if(t.type!=="auto")rem("trans_tune");
  if(target>lim){add(t.type==="auto"?"trans_built":t.type==="dct"?"dct_clutch":"clutch")}
  if(t.type==="manual"&&powered&&tierIdx>=0&&target>t.limit*0.85)add("clutch");
  // use
  var u=S.u;
  if(u==="street")add("brake_pads");
  if(u==="track"){add("brake_pads");add("tires");add("alignment");if(powered)add("oil_cooler");if(t.type!=="manual")add("trans_cooler");if(target>p.stock*1.3)add("radiator")}
  if(u==="drag"){add("drag_radials");if(target>p.stock*1.4){add("axles");if(p.rwd)add("driveshaft")}}
  if(u==="show")add("catback");
  // extras
  S.x.forEach(function(x){add(x);if(x==="coilovers")add("alignment")});
  if(powered||u==="track"||u==="drag")set.unshift("health"),set=set.filter(function(k,i){return set.indexOf(k)===i});
  // flags
  if(set.indexOf("flex")>=0)flags.push(["","Built around E85 / ethanol blends. The flex-fuel kit lets you switch between pump gas and ethanol — power drops on 93."]);
  if(S.c)flags.push(["w","Competition build: catless or emissions-modifying parts are for vehicles used off public roads only. They won't pass Massachusetts inspection. We'll ask you to sign an off-road/competition use acknowledgment."]);
  else if(powered)flags.push(["","Street build: we spec catted parts and tune to stay free of warning lights. Some performance parts aren't emissions-certified — we'll confirm what fits your registration before ordering."]);
  if(set.indexOf("turbo_big")>=0&&!S.c)flags.push(["w","Big-turbo kits generally aren't emissions-certified. Plan this as a dedicated track or competition car, or talk to us about street use first."]);
  if(set.indexOf("built_engine")>=0)flags.push(["","Built-motor builds are planned and quoted individually — this range is a starting point."]);
  if(set.indexOf("ecu_unlock")>=0)flags.push(["","Whether your ECU needs an unlock depends on build date and software; we check before quoting it."]);
  if(set.indexOf("crank_hub")>=0)flags.push(["w","S55 owners: the crank hub can spin past roughly stock-turbo E85 power. We fix it before adding that torque."]);
  if(u==="track"&&!S.x.length)flags.push(["","Track tip: coilovers and a big brake kit are the next upgrades most drivers add — select them under Extras."]);
  notes.forEach(function(n){flags.push(["",n])});
  var items=set.map(function(k){return {k:k,p:P[k]}}).filter(function(i){return i.p});
  var lo=0,hi=0,hrs=0;items.forEach(function(i){lo+=i.p.lo;hi+=i.p.hi;hrs+=i.p.hrs});
  var labor=hrs*RATE;
  return {p:p,t:t,tier:tier,target:target,items:items,lo:lo+labor*0.9,hi:hi+labor*1.15,partsLo:lo,partsHi:hi,hrs:hrs,flags:flags};
}

function render(){
  var r=compute();
  // slider fill
  var rg=$("power");var pc=rg.max>rg.min?((rg.value-rg.min)/(rg.max-rg.min))*100:0;rg.style.setProperty("--fill",pc+"%");
  if(!r){$("hp").innerHTML='—<small>HP</small>';$("r-veh").textContent="Select your car";$("r-stage").textContent="—";$("r-sub").textContent="";$("r-total").textContent="$—";
    $("r-body").innerHTML='<div class="empty">Choose your car and a power goal to see the build.</div>';saveHash();return}
  $("hp").innerHTML=S.hp+'<small>HP</small>';
  $("hp-note").textContent=r.tier?("≈ "+r.tier.n):"Stock power";
  $("r-veh").textContent=(S.vinLabel?S.vinLabel+" · ":"")+r.p.label.split(" — ")[0]+" · "+r.t.n;
  $("r-stage").textContent=r.tier?r.tier.n:"Stock power";
  var uses={};USES.forEach(function(u){uses[u.id]=u.n});
  $("r-sub").textContent=(r.tier?"~"+r.target+" hp (est. crank)":"~"+r.p.stock+" hp stock")+" · "+uses[S.u]+(S.c?" · Competition":"");
  $("r-total").textContent=r.items.length?fmt(r.lo)+" – "+fmt(r.hi):"$0";
  var mb=$("mbar");if(mb){mb.hidden=false;$("mbar-t").textContent=(r.tier?r.tier.n:"Stock")+" · "+$("r-total").textContent}
  if(!r.items.length){$("r-body").innerHTML='<div class="empty">At stock power for daily driving there\'s nothing to add — move the slider or pick a different use.</div>';saveHash();return}
  var groups={};r.items.forEach(function(i){(groups[i.p.g]=groups[i.p.g]||[]).push(i)});
  var html="";
  GROUP_ORDER.forEach(function(g){if(!groups[g])return;
    html+='<div class="pgroup"><h4>'+esc(g)+'</h4>'+groups[g].map(function(i){
      var lab=i.p.hrs*RATE, pr=(i.p.lo+i.p.hi)===0?fmt(lab)+" labor":fmt(i.p.lo+lab)+"–"+fmt(i.p.hi+lab);
      return '<div class="pitem"><div>'+esc(i.p.n)+(i.p.race?'<span class="tag">Off-road only</span>':'')+'<span class="why">'+esc(i.p.why)+'</span></div><div class="pr">'+pr+'</div></div>';
    }).join("")+'</div>'});
  html+='<div class="pgroup"><h4>Summary</h4><div class="pitem"><div>Parts</div><div class="pr">'+fmt(r.partsLo)+'–'+fmt(r.partsHi)+'</div></div><div class="pitem"><div>Labor (~'+Math.round(r.hrs)+' hrs)</div><div class="pr">'+fmt(r.hrs*RATE*0.9)+'–'+fmt(r.hrs*RATE*1.15)+'</div></div></div>';
  html+='<div class="flags">'+r.flags.map(function(f){return '<div class="flag '+f[0]+'">'+esc(f[1])+'</div>'}).join("")+'</div>';
  $("r-body").innerHTML=html;
  saveHash();
}

/* ---------- share / send ---------- */
function sheet(){
  var r=compute();if(!r)return "";
  var uses={};USES.forEach(function(u){uses[u.id]=u.n});
  var L=["AUTO ADDICT WORKS — BUILD SHEET",
    "Vehicle: "+(S.vinLabel||r.p.label)+(S.vin?" (VIN "+S.vin+")":""),
    "Platform: "+r.p.label,"Transmission: "+r.t.n,
    "Goal: "+(r.tier?r.tier.n+" ~"+r.target+" hp":"Stock power")+" · "+uses[S.u]+(S.c?" · OFF-ROAD / COMPETITION BUILD":""),
    "","Parts & work:"];
  r.items.forEach(function(i){L.push(" - "+i.p.n)});
  L.push("","Ballpark: "+fmt(r.lo)+" – "+fmt(r.hi)+" (parts + labor, before health check)","Link: "+location.href);
  return L.join("\n");
}
$("r-copy").addEventListener("click",function(){
  var s=sheet();if(!s)return;var b=this;
  (navigator.clipboard?navigator.clipboard.writeText(s):Promise.reject()).then(function(){b.textContent="Copied ✓";setTimeout(function(){b.textContent="Copy Build Sheet"},1800)})
   .catch(function(){prompt("Copy your build sheet:",s)});
});
$("r-send").addEventListener("click",function(){
  var s=sheet();if(!s){$("make").focus();return}
  try{sessionStorage.setItem("aaw-build",s);sessionStorage.setItem("aaw-build-vehicle",JSON.stringify(S.vinLabel||plat(S.p).label.split(" — ")[1]||""))}catch(e){}
  if(window.dataLayer)window.dataLayer.push({event:"build_request",platform:S.p,hp:S.hp,use:S.u,competition:S.c});
  location.href=root.getAttribute("data-contact");
});

function saveHash(){
  if(!S.p){try{history.replaceState(null,"",location.pathname+location.search)}catch(e){}return}
  var h="p="+S.p+"&t="+S.t+"&u="+S.u+"&hp="+S.hp+(S.c?"&c=1":"")+(S.x.length?"&x="+S.x.join(","):"");
  try{history.replaceState(null,"","#"+h)}catch(e){}
}
function loadHash(){
  var q={};location.hash.replace(/^#/,"").split("&").forEach(function(kv){var a=kv.split("=");if(a[0])q[a[0]]=decodeURIComponent(a[1]||"")});
  var p=plat(q.p);if(!p)return;
  S.u=q.u||"daily";S.c=q.c==="1";S.x=q.x?q.x.split(","):[];S.hp=+q.hp||null;
  $("compete").checked=S.c;chips($("use"),USES,"radio","use",function(id){return id===S.u});drawExtras();
  mk.value=p.make;fillPlatforms(p.make);pl.value=p.id;setPlatform(p.id,true);
  if(q.t){tr.value=q.t;S.t=q.t}
  render();
}
fillPlatforms("");fillTrans(null);
loadHash();render();
window.addEventListener("hashchange",function(){S.vin="";S.vinLabel="";loadHash()});
})();
