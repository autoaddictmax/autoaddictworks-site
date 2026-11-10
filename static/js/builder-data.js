/* Auto Addict Works build planner data.
   P: part key -> [name, why, typical parts price USD, labor hours, offroadOnly]
   PL: platforms -> tiers [hp, stage name, parts added, parts removed]. Edit freely. */
window.AAW_B=(function(){

var P={tune:["ECU flash tune","bootmod3 / MHD map for your hardware",1000,1.5],ecu:["ECU unlock (if required)","Newer ECUs need a bench unlock",900,1.5],
intake:["High-flow intake","Lower intake temps",420,.8],cp:["Aluminum charge pipe","Factory plastic pipe fails under boost",300,1],
dp:["Catted downpipe","Big flow gain, keeps the cats",1400,3],dpr:["Catless downpipe","Max flow, competition only",750,3,1],
fmic:["Upgraded intercooler","Holds charge temps down",1050,3],plugs:["Colder spark plugs","Stops misfires at higher boost",190,1],
coils:["Upgraded ignition coils","Stronger spark on E85",400,.5],tt:["ZF8 transmission tune","Raises torque limits, sharper shifts",600,1],
dct:["DCT tune","Clutch clamping and torque limits",600,1],flex:["Flex-fuel kit","Run E85 blends or pump gas",600,1.5],
lpfp:["Low-pressure fuel pump","Keeps up with ethanol demand",680,2.5],pi:["Port injection kit","More fuel than DI alone can deliver",2100,6],
hpfp:["High-pressure fuel pump","More DI pressure headroom",1450,3],hy:["Hybrid turbo","Factory fitment, much bigger flow",4100,10],
tw:["Upgraded twin turbos","Stock turbos are maxed",7000,18],big:["Big single turbo kit","Manifold, turbo, gate and piping",10200,25],
cust:["Custom dyno tune","Calibrated to your exact setup",1550,3],oil:["Oil cooler","Sustained boost and track heat",900,4],
rad:["Upgraded radiator","More heat to reject",780,3],inj:["Upgraded injectors","Fuel for big-turbo power",1400,4],
built:["Built engine","Forged rods and pistons",14500,40],hub:["Crank hub fix","S55 hub can spin past this torque",650,8],
tb:["Built transmission","Clutch packs for this torque",5500,18],dcc:["DCT clutch packs","Stock DCT clutches slip past this torque",4000,14],
pads:["Performance pads + fluid","Fade-resistant stopping",520,2.5],tires:["200TW tires","Grip is the first limit",1550,1.5],
align:["Performance alignment","Set for your tires and driving",0,1.5],tcool:["Transmission cooler","Keeps gearbox temps in check on track",570,3],
radials:["Drag radials","Traction off the line",1400,1.5],axles:["Upgraded axles","Launches break factory axles",2500,5],
ds:["One-piece driveshaft","Stronger for repeated launches",1900,3],catback:["Cat-back exhaust","Sound, valved for the street",2000,2.5],
harness:["Seat, harness & bar","Required by most rule books",3000,5,1]};
var PL=[
 {id:"b58f",code:"B58",gen:"Gen 1 · 2016 to 2019",name:"340i / 440i",models:"F30 340i, F32 440i, M240i, G30 540i",stock:320,trans:"ZF 8-speed",tlim:650,
  tiers:[[400,"Stage 1",["tune","cp"]],[440,"Stage 2",["intake","dp","plugs"]],[480,"Stage 2+",["fmic","tt"]],[540,"Stage 2+ E85",["flex","lpfp"]],[600,"Port Injection",["pi","coils"]],[720,"Hybrid Turbo",["hy","cust","oil","hpfp"]],[900,"Big Single",["big","rad","inj"],["hy"]],[1300,"Built Motor",["built"]]]},
 {id:"b58g",code:"B58",gen:"Gen 2 · 2020+",name:"M340i / M440i",models:"G20 M340i, G22 M440i, Z4 M40i, X3 M40i",stock:382,trans:"ZF 8-speed",tlim:700,
  tiers:[[460,"Stage 1",["tune","ecu"]],[500,"Stage 2",["intake","dp","plugs"]],[540,"Stage 2+",["fmic","tt"]],[600,"Stage 2+ E85",["flex","lpfp"]],[660,"Port Injection",["pi","coils"]],[760,"Hybrid Turbo",["hy","cust","oil","hpfp"]],[950,"Big Single",["big","rad","inj"],["hy"]],[1300,"Built Motor",["built"]]]},
 {id:"s55",code:"S55",gen:"F8x · 2015 to 2021",name:"M3 / M4 / M2C",models:"F80 M3, F82 M4, M2 Competition",stock:425,trans:"7-speed DCT",tlim:640,dct:1,
  tiers:[[520,"Stage 1",["tune","cp"]],[570,"Stage 2",["dp","intake","fmic","plugs","dct"]],[640,"Stage 2 E85",["flex","lpfp","hub"]],[700,"Port Injection",["pi","coils"]],[820,"Upgraded Turbos",["tw","cust","oil","hpfp"]],[950,"Built Motor",["built","inj","rad"]]]},
 {id:"s58",code:"S58",gen:"G8x · 2021+",name:"M3 / M4 / M2",models:"G80 M3, G82 M4, G87 M2, X3 M",stock:473,trans:"ZF 8-speed M",tlim:720,
  tiers:[[580,"Stage 1",["tune","ecu"]],[640,"Stage 2",["dp","intake","fmic","plugs","tt"]],[720,"Stage 2 E85",["flex","lpfp"]],[780,"Port Injection",["pi","coils"]],[920,"Hybrid Turbos",["tw","cust","oil","hpfp"]],[1100,"Built Motor",["built","inj","rad"]]]}];
var MODES=[["daily","Daily driver","Reliable, CEL-free",'<path d="M4 15l2-5h12l2 5v3H4z"/><circle cx="8" cy="18" r="1.6"/><circle cx="16" cy="18" r="1.6"/>'],
 ["street","Spirited street","Back roads & weekends",'<path d="M3 20c5-2 6-9 9-9s3 6 9 9"/><path d="M12 3v4"/>'],
 ["track","Track / HPDE","Heat & braking",'<path d="M4 4v16"/><path d="M4 4h12l-2 4 2 4H4"/>'],
 ["drag","Drag / roll","Launch & top end",'<path d="M3 12h13"/><path d="M12 7l5 5-5 5"/><path d="M20 5v14"/>'],
 ["show","Show & sound","Looks, sound, stance",'<path d="M4 9v6h4l5 4V5L8 9z"/><path d="M17 9a4 4 0 0 1 0 6"/>']];

var VIN=[{p:"s58",re:/\b(M3|M4)\b/,y:[2021,2099]},{p:"s58",re:/\bM2\b/,y:[2023,2099]},{p:"s58",re:/X[34]\s?M\b/,y:[2020,2099]},
 {p:"s55",re:/\b(M3|M4)\b/,y:[2015,2020]},{p:"s55",re:/\bM2\b/,y:[2019,2021]},
 {p:"b58g",re:/M340i|M440i|M40i|40i/,y:[2020,2099]},{p:"b58f",re:/340i|440i|540i|M240i|M40i|40i/,y:[2016,2019]}];
return {P:P,PL:PL,MODES:MODES,VIN:VIN};})();
