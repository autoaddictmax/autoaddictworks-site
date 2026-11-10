(function(){
  var t=document.querySelector('.nav-toggle'),n=document.getElementById('nav');
  if(t&&n)t.addEventListener('click',function(){var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o)});
  document.querySelectorAll('.dd-btn').forEach(function(b){b.addEventListener('click',function(){var d=b.parentNode,o=d.classList.toggle('open');b.setAttribute('aria-expanded',o)})});

  var cfg=window.AAW||{};
  var f=document.getElementById('contact-form');
  if(f){
    var build=null;try{build=sessionStorage.getItem('aaw-build')}catch(e){}
    if(build){
      document.getElementById('build-summary-wrap').hidden=false;
      document.getElementById('build').value=build;
      document.getElementById('reason').value='Performance build';
      try{var v=JSON.parse(sessionStorage.getItem('aaw-build-vehicle')||'""');if(v)document.getElementById('vehicle').value=v}catch(e){}
    }
  }
  document.querySelectorAll('.lead-form').forEach(function(form){
    var st=form.querySelector('.form-status')||document.getElementById('form-status');
    function say(m){st.textContent=m;st.classList.add('show')}
    form.addEventListener('submit',function(ev){
      ev.preventDefault();
      var d={};new FormData(form).forEach(function(v,k){d[k]=String(v).trim()});
      if(!d.name||!d.phone){say('Please add your name and phone number.');return}
      if(d.vin&&!/^[A-HJ-NPR-Z0-9]{17}$/i.test(d.vin)){say('That VIN should be 17 characters. Leave it blank if you are not sure.');return}
      d.type=form.dataset.kind||'Website lead';d.source='website';d.page=location.pathname;d.submittedAt=new Date().toISOString();
      if(cfg.formEndpoint){
        fetch(cfg.formEndpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)})
          .then(function(r){if(!r.ok)throw 0;say(d.type==='Call back request'?'Thanks, we will call you back shortly.':'Thanks, we got it and will be in touch shortly.');form.reset();try{sessionStorage.removeItem('aaw-build')}catch(e){}})
          .catch(function(){say('Something went wrong sending that. Please call us at '+cfg.phoneDisplay+'.')});
      }else{
        var body=Object.keys(d).filter(function(k){return d[k]}).map(function(k){return k+': '+d[k]}).join('\n');
        location.href='mailto:'+cfg.email+'?subject='+encodeURIComponent(d.type+': '+(d.vehicle||d.vin||d.name))+'&body='+encodeURIComponent(body);
        say('Opening your email app to send this request…');
      }
    });
  });
})();
