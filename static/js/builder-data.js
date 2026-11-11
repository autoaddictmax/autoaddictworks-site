/* Auto Addict Works build planner data.
   P: part key -> [name, why, typical parts price USD, labor hours, offroadOnly]
   PL: platforms -> tiers [whp, stage name, parts added, parts removed]; tq = est. wheel torque per tier;
   tx = automatic transmission torque zones (warn = pushing it, limit = needs a built trans). Edit freely. */
window.AAW_B=(function(){

var P={pig:["Engine tune, piggyback (independent tuner)","Gen 3 flash support is still limited, so piggyback units are common",0,0,0,1],
tune:["Engine tune (independent tuner)","Matched to your hardware and fuel",0,0,0,1],ecu:["ECU unlock (if required)","Newer ECUs need a bench unlock before tuning",0,0,0,1],
intake:["High-flow intake","Lower intake temps",420,.8],cp:["Aluminum charge pipe","Factory plastic pipe fails under boost",300,1],
dp:["Catted downpipe","Big flow gain, keeps the cats",1400,3],dpr:["Catless downpipe","Max flow, competition only",750,3,1],
fmic:["Upgraded intercooler / heat exchanger","e.g. CSF or Wagner, holds charge temps down",1050,3],plugs:["Colder spark plugs","Stops misfires at higher boost",190,1],
coils:["Upgraded ignition coils","Stronger spark on E85",400,.5],tt:["Transmission tune (independent tuner)","Raises torque limits, sharper shifts",0,0,0,1],
dct:["DCT tune (independent tuner)","Raises clutch clamping and torque limits",0,0,0,1],flex:["Flex-fuel kit","Run E85 blends or pump gas",600,1.5],
lpfp:["Low-pressure fuel pump","e.g. Spool or Fuel-It, keeps up with ethanol",680,2.5],pi:["Port injection kit","e.g. Precision Raceworks PI, needed past DI fueling limits",2100,6],
hpfp:["Upgraded HPFP","e.g. Dorch Engineering, more direct-injection fuel",1450,3],hy:["Hybrid turbo","e.g. Pure Turbos Pure800, factory fitment",4100,10],
tw:["Upgraded turbos","e.g. Pure Turbos Stage 2, stock turbos are maxed",7000,18],big:["Big single turbo kit","Manifold, turbo, gate and piping",10200,25],
cust:["Custom tune (independent tuner)","Calibrated to your exact setup",0,0,0,1],oil:["Oil cooler","Sustained boost and track heat",900,4],
rad:["Upgraded radiator","More heat to reject",780,3],inj:["Upgraded injectors","Fuel for big-turbo power",1400,4],
built:["Built engine","Forged rods and pistons",14500,40],hub:["Crank hub fix","Pinned or keyed hub before E85-level torque",650,8],
tb:["Built transmission","Pure Drivetrain, Advanced Torque Solutions (ATS), or a Dodson pack for 1,200+ hp builds",6500,18],dcc:["DCT clutch packs","Stock DCT clutches slip past this torque",4000,14],
pads:["Performance pads + fluid","Fade-resistant stopping",520,2.5],tires:["200TW tires","Grip is the first limit",1550,1.5],
align:["Performance alignment","Set for your tires and driving",0,1.5],tcool:["Transmission cooler","Keeps gearbox temps in check on track",570,3],
radials:["Drag radials","Traction off the line",1400,1.5],axles:["Upgraded axles","Launches break factory axles",2500,5],
ds:["One-piece driveshaft","Stronger for repeated launches",1900,3],catback:["Cat-back exhaust","Sound, valved for the street",2000,2.5],
harness:["Seat, harness & bar","Required by most rule books",3000,5,1]};
var PL=[
 /* Power figures are approximate WHEEL horsepower (dynojet-style), compiled from published results
    from hardware vendors and forum dyno threads.
    Confirm against your own dyno history. */
 {id:"b58f",code:"B58",gen:"Gen 1 · 2016 to 2021",name:"340i · 440i · M240i",models:"340i (2016 to 2019) · 440i (2017 to 2020) · M240i (2017 to 2021) · 540i, 740i (2017 to 2019) · X3 M40i (2018 to 2019)",fac:320,stock:300,trans:"ZF 8-speed",tlim:600,tq:[420,460,500,540,580,620,700,750,1000],stq:330,tx:{name:"ZF 8HP50",warn:600,limit:700},turbo:"b58",
  tiers:[[370,"Stage 1",["tune"]],[410,"Stage 2",["intake","dp","cp","plugs"]],[430,"Stage 2+",["fmic","tt"]],[460,"Stage 2+ E30",["flex","lpfp"]],
         [500,"Stock-Turbo E50",["hpfp","coils"]],[580,"Hybrid Turbo",["hy","cust","oil"]],[700,"Hybrid Turbo E85 + PI",["pi"]],
         [850,"Big Single",["big","rad","inj"],["hy"]],[1300,"Built Motor",["built"]]]},
 {id:"b58g",code:"B58",gen:"Gen 2 · 2019 to 2024",name:"M340i · M440i · M240i · Z4 M40i",models:"M340i (2020 to 2024) · M440i (2021 to 2024) · M240i (2022 to 2025) · Z4 M40i (2019+) · X3 M40i (2020 to 2024) · 540i (2020 to 2023) · X5 40i (2019 to 2023)",fac:382,stock:380,trans:"ZF 8-speed",tlim:600,tq:[500,520,540,580,600,620,660,750,850],stq:400,tx:{name:"ZF 8HP51",warn:600,limit:700},turbo:"b58",
  tiers:[[440,"Stage 1",["tune","ecu"]],[460,"Stage 2",["intake","dp","plugs"]],[475,"Stage 2 E30",["fmic","tt","flex"]],
         [510,"Stock-Turbo E50",["lpfp","coils"]],[540,"Stock-Turbo E60 + PI",["pi"]],[580,"Hybrid Turbo",["hy","cust","oil"]],[650,"Hybrid Turbo E85",["hpfp"]],
         [850,"Big Single",["big","rad","inj"],["hy"]],[1000,"Built Motor",["built"]]]},
 {id:"b58n",code:"B58",gen:"Gen 3 · 2023+",name:"M340i · M440i · X3 M50 · 540i",models:"M340i, M440i (2025+) · X3 M50 (2025+) · 540i (2024+) · X5, X6 40i (2024+) · X7 40i, 740i (2023+)",fac:382,stock:370,trans:"ZF 8-speed",tlim:600,gen3:1,
  tq:[480,500,530],stq:400,tx:{name:"ZF 8HP",warn:600,limit:700},turbo:"b58",
  tiers:[[430,"Stage 1",["pig"]],[455,"Stage 2",["intake","dp","plugs","tt"]],[485,"Stage 2 E30",["flex"]]]},
 {id:"s55",code:"S55",gen:"F8x · 2015 to 2021",name:"M3 · M4 · M2 Competition",models:"F80 M3 (2015 to 2018) · F82/F83 M4 (2015 to 2020) · F87 M2 Competition and CS (2019 to 2021)",fac:425,stock:400,trans:"7-speed DCT",tlim:560,dct:1,tq:[480,520,560,620,620,640],stq:400,turbo:"s55",
  tiers:[[450,"Stage 1",["tune"]],[495,"Stage 2",["dp","intake","cp","plugs"]],[545,"Stage 2+",["fmic","dct","hub"]],
         [600,"Stock-Turbo E85",["flex","lpfp","coils"]],[650,"Upgraded Turbos",["tw","cust","oil"]],[730,"Upgraded Turbos E85 + PI",["pi","hpfp"]]]},
 {id:"s58",code:"S58",gen:"G8x · 2020+",name:"M3 · M4 · M2 · X3 M",models:"G80 M3 (2021+) · G82/G83 M4 (2021+) · G87 M2 (2023+) · X3 M and X4 M (2020 to 2024)",fac:503,stock:450,trans:"ZF 8-speed M",tlim:720,tq:[560,620,675,720,800,980,1200],stq:443,tx:{name:"ZF 8HP76",warn:700,limit:780},turbo:"s58",
  tiers:[[540,"Stage 1",["tune","ecu"]],[590,"Stage 2",["dp","intake","fmic","plugs","tt"]],[660,"Stage 2 E50",["flex","lpfp"]],
         [730,"Stage 2 E85 + PI",["pi","coils"]],[900,"Upgraded Turbos",["tw","cust","oil","hpfp"]],
         [1100,"Big Single",["big","rad","inj"],["tw"]],[1400,"Built Motor",["built"]]]}];
var MODES=[["daily","Daily driver","Reliable, CEL-free",'<path d="M4 15l2-5h12l2 5v3H4z"/><circle cx="8" cy="18" r="1.6"/><circle cx="16" cy="18" r="1.6"/>'],
 ["street","Spirited street","Back roads & weekends",'<path d="M3 20c5-2 6-9 9-9s3 6 9 9"/><path d="M12 3v4"/>'],
 ["track","Track / HPDE","Heat & braking",'<path d="M4 4v16"/><path d="M4 4h12l-2 4 2 4H4"/>'],
 ["drag","Drag / roll","Launch & top end",'<path d="M3 12h13"/><path d="M12 7l5 5-5 5"/><path d="M20 5v14"/>'],
 ["show","Show & sound","Looks, sound, stance",'<path d="M4 9v6h4l5 4V5L8 9z"/><path d="M17 9a4 4 0 0 1 0 6"/>']];

var VIN=[{p:"s58",re:/\b(M3|M4)\b/,y:[2021,2099]},{p:"s58",re:/\bM2\b/,y:[2023,2099]},{p:"s58",re:/X[34]\s?M\b/,y:[2020,2099]},
 {p:"s55",re:/\b(M3|M4)\b/,y:[2015,2020]},{p:"s55",re:/\bM2\b/,y:[2019,2021]},
 {p:"b58n",re:/M340i|M440i/,y:[2025,2099]},{p:"b58n",re:/M50/,y:[2025,2099]},{p:"b58n",re:/540i|X5.*40i|X6.*40i|40i.*X[56]/,y:[2024,2099]},{p:"b58n",re:/740i|X7/,y:[2023,2099]},
 {p:"b58g",re:/M340i|M440i|Z4|M40i/,y:[2019,2024]},{p:"b58g",re:/M240i/,y:[2022,2025]},{p:"b58g",re:/540i|740i|840i|40i/,y:[2020,2023]},
 {p:"b58f",re:/340i|440i|540i|740i|M240i|M40i/,y:[2016,2021]}];
return {P:P,PL:PL,MODES:MODES,VIN:VIN};})();
