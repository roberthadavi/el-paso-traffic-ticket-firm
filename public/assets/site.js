(function(){
  var ES=document.documentElement.lang==='es';
  // Mobile menu
  var btn=document.querySelector('.menu-btn'),menu=document.getElementById('menu');
  if(btn&&menu){btn.addEventListener('click',function(){var o=menu.classList.toggle('open');btn.setAttribute('aria-expanded',o?'true':'false');});}

  // Lazy YouTube facade
  document.querySelectorAll('.video[data-yt]').forEach(function(v){
    var b=v.querySelector('button');if(!b)return;
    b.addEventListener('click',function(){
      var f=document.createElement('iframe');
      f.src='https://www.youtube-nocookie.com/embed/'+v.dataset.yt+'?autoplay=1&rel=0';
      f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
      f.allowFullscreen=true;f.title=v.dataset.title||'Video';
      v.innerHTML='';v.appendChild(f);
    });
  });

  // Lead forms → Worker /api/contact
  document.querySelectorAll('form[data-lead]').forEach(function(form){
    form.addEventListener('submit',function(e){
      e.preventDefault();
      var msg=form.querySelector('.msg'),sub=form.querySelector('button[type=submit]');
      var data={};new FormData(form).forEach(function(v,k){data[k]=v;});
      data.page=location.pathname;data.form=form.dataset.lead;
      msg.className='msg';sub.disabled=true;var old=sub.textContent;sub.textContent=ES?'Enviando…':'Sending…';
      fetch('/api/contact',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})
        .then(function(r){return r.json().then(function(j){return {ok:r.ok&&j.ok,j:j};});})
        .then(function(r){
          if(r.ok){msg.className='msg ok';msg.textContent=ES?'¡Gracias! Recibimos su información y nos comunicaremos con usted en breve. Para atención más rápida llame al 915-200-1133.':'Thank you! We received your information and will contact you shortly. For faster service call 915-200-1133.';form.reset();}
          else{throw new Error(r.j&&r.j.error||'send_failed');}
        })
        .catch(function(){msg.className='msg err';msg.innerHTML=(ES?'Lo sentimos, el formulario no se pudo enviar en este momento. Llame al ':'Sorry, the form could not be sent right now. Please call ')+'<a href="tel:9152001133">915-200-1133</a>'+(ES?' o escriba a ':' or email ')+'<a href="mailto:help@elpasotrafficticketfirm.com">help@elpasotrafficticketfirm.com</a>.';})
        .finally(function(){sub.disabled=false;sub.textContent=old;});
    });
  });
})();
