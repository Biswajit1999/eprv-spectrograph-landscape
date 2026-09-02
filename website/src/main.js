import './style.css';

const parseCSV = text => {
  const rows=[]; let row=[], field='', quoted=false;
  for(let i=0;i<text.length;i++){const c=text[i],n=text[i+1];if(c==='"'&&quoted&&n==='"'){field+='"';i++;}else if(c==='"'){quoted=!quoted;}else if(c===','&&!quoted){row.push(field);field='';}else if((c==='\n'||c==='\r')&&!quoted){if(c==='\r'&&n==='\n')i++;row.push(field);if(row.some(Boolean))rows.push(row);row=[];field='';}else field+=c;}
  if(field||row.length){row.push(field);rows.push(row)} const headers=rows.shift();
  return rows.map(values=>Object.fromEntries(headers.map((h,i)=>[h,values[i]??''])));
};

async function main(){
const [instrumentText,claimText]=await Promise.all([
  fetch('/data/instruments.csv').then(r=>{if(!r.ok)throw new Error('instrument data unavailable');return r.text()}),
  fetch('/data/performance_claims.csv').then(r=>{if(!r.ok)throw new Error('claim data unavailable');return r.text()})
]);
const instruments=parseCSV(instrumentText), claims=parseCSV(claimText);
const statusSelect=document.querySelector('#status-filter'), bandSelect=document.querySelector('#band-filter'), search=document.querySelector('#search');
document.querySelector('#instrument-count').textContent=instruments.length;
document.querySelector('#claim-count').textContent=claims.length;
document.querySelector('#operational-count').textContent=instruments.filter(d=>d.status.startsWith('operational')).length;
[...new Set(instruments.map(d=>d.status))].sort().forEach(status=>statusSelect.add(new Option(status.replaceAll('_',' '),status)));

const esc=value=>String(value).replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
function renderInstruments(){const q=search.value.trim().toLowerCase();const filtered=instruments.filter(d=>(!q||`${d.instrument} ${d.facility}`.toLowerCase().includes(q))&&(!statusSelect.value||d.status===statusSelect.value)&&(!bandSelect.value||d.spectral_domain===bandSelect.value));document.querySelector('#table-result').textContent=`Showing ${filtered.length} of ${instruments.length} records`;document.querySelector('#instrument-body').innerHTML=filtered.map(d=>`<tr><td>${esc(d.instrument)}</td><td>${esc(d.facility)}</td><td>${esc(d.wave_min_nm)}–${esc(d.wave_max_nm)} nm</td><td>${Number(d.resolving_power).toLocaleString()}</td><td><span class="pill ${esc(d.status)}">${esc(d.status.replaceAll('_',' '))}</span></td><td>${esc(d.performance_class.replaceAll('_',' '))}</td></tr>`).join('')}
[search,statusSelect,bandSelect].forEach(el=>el.addEventListener('input',renderInstruments));renderInstruments();

const cardClass=c=>c.measurement_context.includes('requirement')?'requirement':c.measurement_context.includes('calibration')?'calibration':'sky';
document.querySelector('#claim-grid').innerHTML=claims.map(c=>`<article class="claim ${cardClass(c)}"><header><h3>${esc(c.instrument)}</h3><span class="value">${esc(c.comparison==='upper_bound'?'< ':c.comparison==='approximately'?'≈ ':'')}${esc(c.value_mps)} m/s</span></header><p>${esc(c.reported_result)}</p><p class="context">${esc(c.measurement_context.replaceAll('_',' '))}</p><details><summary>Context and source</summary><dl><dt>Metric</dt><dd>${esc(c.metric.replaceAll('_',' '))}</dd><dt>Sample</dt><dd>${esc(c.target_or_sample)}</dd><dt>Baseline</dt><dd>${esc(c.baseline)}</dd><dt>Limit</dt><dd>${esc(c.caveat)}</dd></dl><a href="${esc(c.source_url)}" rel="noreferrer">Primary source</a></details></article>`).join('');
}

main().catch(error=>{
  document.querySelector('#table-result').textContent=`Data could not be loaded: ${error.message}`;
});
