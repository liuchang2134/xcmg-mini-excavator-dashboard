function setupRadars(){
  document.querySelectorAll('.radarBox,.factorRadar').forEach(box=>{
    const current=box.querySelector('.radarCurrent');
    const selected=new Set();
    const series=[...box.querySelectorAll('.radar-series[data-product]')];
    const controls=[...box.querySelectorAll('.radarLegend [data-product]')];
    controls.filter(btn=>btn.dataset.default==='true').forEach(btn=>selected.add(btn.dataset.product));
    const label=()=>{
      if(!current) return;
      if(selected.size===0) current.textContent='当前：全部品牌';
      else if(selected.size===1) current.textContent='当前：'+[...selected][0];
      else current.textContent='当前：'+selected.size+' 个品牌对比';
    };
    const render=()=>{
      const hasSelection=selected.size>0;
      box.classList.toggle('compare',hasSelection);
      series.forEach(s=>s.classList.toggle('selected',hasSelection && selected.has(s.dataset.product)));
      controls.forEach(btn=>{
        const on=selected.has(btn.dataset.product);
        btn.classList.toggle('selected',on);
        btn.setAttribute('aria-pressed',String(on));
      });
      label();
    };
    const toggle=(product)=>{
      if(selected.size===0) selected.add(product);
      else if(selected.has(product)) selected.delete(product);
      else selected.add(product);
      render();
    };
    controls.forEach(btn=>{
      btn.setAttribute('aria-pressed','false');
      btn.addEventListener('click',()=>toggle(btn.dataset.product));
    });
    series.forEach(shape=>{
      shape.setAttribute('tabindex','0');
      shape.setAttribute('role','button');
      shape.addEventListener('click',()=>toggle(shape.dataset.product));
      shape.addEventListener('keydown',e=>{
        if(e.key==='Enter'||e.key===' '){
          e.preventDefault();
          toggle(shape.dataset.product);
        }
      });
    });
    render();
  });
}
function setupSimulators(){
  document.querySelectorAll('.simulator').forEach(sim=>{
    const xcmg=sim.dataset.xcmg;
    const rivals=(sim.dataset.rivals||'').split('|').filter(Boolean).map(x=>{const i=x.lastIndexOf(':');return {product:x.slice(0,i),score:Number(x.slice(i+1))};});
    const base=Number(sim.dataset.base||0);
    const scoreEl=sim.querySelector('.simResult strong');
    const rankEl=sim.querySelector('.simResult b');
    const gapEl=sim.querySelector('.simResult small');
    const panel=sim.querySelector('.rankPanel');
    const inputs=[...sim.querySelectorAll('input[type="checkbox"]')];
    const render=()=>{
      const score=Math.min(100, base + inputs.filter(i=>i.checked).reduce((s,i)=>s+Number(i.dataset.delta||0),0));
      const rows=[{product:xcmg,score,isX:true},...rivals].sort((a,b)=>b.score-a.score).map((r,i)=>({...r,rank:i+1}));
      const xrow=rows.find(r=>r.isX);
      const prev=rows[rows.findIndex(r=>r.isX)-1];
      scoreEl.textContent=score.toFixed(1).replace(/\.0$/,'');
      rankEl.textContent='模拟第'+xrow.rank;
      gapEl.textContent=prev ? '距前一名 '+prev.product+' 还差 '+Math.max(0,prev.score-score).toFixed(1)+' 分' : '已达到该工况第一名';
      const max=Math.max(...rows.map(r=>r.score),1);
      panel.classList.add('show');
      panel.innerHTML='<div class="bars">'+rows.map(r=>'<div class="'+(r.isX?'bar xcmg':'bar')+'"><span>'+r.rank+'</span><b>'+r.product+'</b><i><em style="width:'+(r.score/max*100).toFixed(1)+'%"></em></i><strong>'+r.score.toFixed(1).replace(/\.0$/,'')+'</strong></div>').join('')+'</div>';
    };
    inputs.forEach(i=>i.addEventListener('change',render));
    sim.querySelector('.resetSim')?.addEventListener('click',()=>{inputs.forEach(i=>i.checked=false);render();});
    render();
  });
}
function setupRawTabs(){
  document.querySelectorAll('.rawTabs button').forEach(btn=>btn.addEventListener('click',()=>{
    document.querySelectorAll('.rawTabs button').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.rawTable').forEach(t=>t.dataset.open=String(t.dataset.name===btn.dataset.table));
  }));
}
function setupPageNavigation(){
  const toggle=document.querySelector('.navToggle');
  const menu=document.querySelector('.navMenu');
  if(toggle&&menu){
    toggle.addEventListener('click',()=>{
      const open=menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded',String(open));
      toggle.textContent=open?'收起导航':'页面导航';
    });
    menu.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>{
      if(window.matchMedia('(max-width:1200px)').matches){
        menu.classList.remove('open');
        toggle.setAttribute('aria-expanded','false');
        toggle.textContent='页面导航';
      }
    }));
  }
  const backTop=document.querySelector('.backTop');
  if(backTop){
    const update=()=>backTop.classList.toggle('show',window.scrollY>640);
    window.addEventListener('scroll',update,{passive:true});
    update();
  }
}
function setupMobileDisclosures(){
  const media=window.matchMedia('(max-width:720px)');
  const apply=()=>{
    document.querySelectorAll('[data-mobile-open]').forEach(item=>{
      item.open=media.matches ? item.dataset.mobileOpen==='true' : true;
    });
  };
  apply();
  if(media.addEventListener) media.addEventListener('change',apply);
  else if(media.addListener) media.addListener(apply);
}
setupMobileDisclosures();
setupRadars();
setupSimulators();
setupRawTabs();
setupPageNavigation();
