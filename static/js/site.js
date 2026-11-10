(function(){
  var t=document.querySelector('.nav-toggle'),n=document.getElementById('nav');
  if(t&&n)t.addEventListener('click',function(){var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o)});
  document.querySelectorAll('.dd-btn').forEach(function(b){b.addEventListener('click',function(){var d=b.parentNode,o=d.classList.toggle('open');b.setAttribute('aria-expanded',o)})});

  var f=document.getElementById('contact-form');
  if(!f)return;
  var cfg=window.AAW||{};
  var build=null;try{build=sessionStorage.getItem('aaw-build')}catch(e){}
  if(build){
    document.getElementById('build-summary-wrap').hidden=false;
    document.getElementById('build').value=build;
    document.getElementById('reason').value='Performance build';
    try{var v=JSON.parse(sessionStorage.getItem('aaw-build-vehicle')||'""');if(v)document.getElementById('vehicle').value=v}catch(e){}
  }
  var st=document.getElementById('form-status');
  function say(m){st.textContent=m;st.classList.add('show')}
  f.addEventListener('submit',function(ev){
    ev.preventDefault();
    var d={};new FormData(f).forEach(function(v,k){d[k]=v});
    if(!d.name||!d.phone){say('Please add your name and phone number.');return}
    d.source='website';d.page=location.pathname;d.submittedAt=new Date().toISOString();
    if(cfg.formEndpoint){
      fetch(cfg.formEndpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)})
        .then(function(r){if(!r.ok)throw 0;say('Thanks, we got it and will be in touch shortly.');f.reset();try{sessionStorage.removeItem('aaw-build')}catch(e){}})
        .catch(function(){say('Something went wrong sending that. Please call us at '+cfg.phoneDisplay+'.')});
    }else{
      var body=Object.keys(d).filter(function(k){return d[k]}).map(function(k){return k+': '+d[k]}).join('\n');
      location.href='mailto:'+cfg.email+'?subject='+encodeURIComponent('Service request: '+(d.vehicle||d.name))+'&body='+encodeURIComponent(body);
      say('Opening your email app to send this request…');
    }
  });
})();
