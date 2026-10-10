import './style.css';
import world from '@cublya/world-atlas/countries-110m.json';
import { geoGraticule10, geoNaturalEarth1, geoPath } from 'd3-geo';
import { feature, mesh } from 'topojson-client';
import { calculateDopplerShift } from './doppler.js';

const parseCSV = text => {
  const rows=[]; let row=[], field='', quoted=false;
  for(let i=0;i<text.length;i++){const c=text[i],n=text[i+1];if(c==='"'&&quoted&&n==='"'){field+='"';i++;}else if(c==='"'){quoted=!quoted;}else if(c===','&&!quoted){row.push(field);field='';}else if((c==='\n'||c==='\r')&&!quoted){if(c==='\r'&&n==='\n')i++;row.push(field);if(row.some(Boolean))rows.push(row);row=[];field='';}else field+=c;}
  if(field||row.length){row.push(field);rows.push(row)} const headers=rows.shift();
  return rows.map(values=>Object.fromEntries(headers.map((h,i)=>[h,values[i]??''])));
};

const parseJSONL = text => text.split(/\r?\n/).filter(Boolean).map(line => JSON.parse(line));
const esc = value => String(value ?? '').replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
const words = value => String(value ?? '').replaceAll('_',' ');
const editorialText = value => String(value ?? '')
  .replace(/\bclaims\b/gi,'statements')
  .replace(/\bclaim\b/gi,'statement')
  .replace(/\bledger\b/gi,'register')
  .replace(/\bprotocol\b/gi,'method');
const tierLabels = {
  A_dedicated_prv_eprv: 'A · Dedicated PRV/EPRV',
  B_general_high_resolution_with_rv_evidence: 'B · High-resolution with RV evidence',
  C_historical_prototype_or_specialist: 'C · Historical or specialist',
  D_funded_construction_or_commissioning: 'D · Construction or commissioning',
};

const mapProjection=geoNaturalEarth1().fitExtent([[24,24],[976,476]],{type:'Sphere'}).precision(.1);
const mapPath=geoPath(mapProjection);

function formatSigned(value, digits) {
  const number=Number(value);
  const sign=number>0?'+':number<0?'−':'';
  return `${sign}${Math.abs(number).toFixed(digits)}`;
}

function setupDopplerLab(){
  const velocityInput=document.querySelector('#rv-velocity');
  const wavelengthInput=document.querySelector('#rv-wavelength');
  const velocityOutput=document.querySelector('#rv-velocity-output');
  const observedLine=document.querySelector('#observed-line');
  const plotSummary=document.querySelector('#velocity-plot-summary');
  const presetButtons=[...document.querySelectorAll('[data-velocity]')];
  if(!velocityInput||!wavelengthInput)return;

  function render(){
    const velocity=Number(velocityInput.value);
    const wavelength=Number(wavelengthInput.value);
    const result=calculateDopplerShift({velocityMps:velocity,wavelengthNm:wavelength});
    const position=Math.max(0,Math.min(100,(velocity+100)/2));
    const directionPhrase=result.direction==='redshift'?'to the red of':result.direction==='blueshift'?'to the blue of':'aligned with';
    const exponent=result.fractionalShift===0?0:Math.floor(Math.log10(Math.abs(result.fractionalShift)));
    const mantissa=result.fractionalShift===0?0:result.fractionalShift/(10**exponent);

    velocityOutput.value=`${formatSigned(velocity,1)} m/s`;
    observedLine.style.left=`${position}%`;
    document.querySelector('#shifted-wavelength').textContent=`${result.shiftedWavelengthNm.toFixed(9)} nm`;
    document.querySelector('#wavelength-shift').textContent=`${formatSigned(result.deltaWavelengthPm,6)} pm`;
    document.querySelector('#fractional-shift').textContent=result.fractionalShift===0?'0':`${formatSigned(mantissa,3)} × 10${String(exponent).replace('-','⁻').replaceAll('0','⁰').replaceAll('1','¹').replaceAll('2','²').replaceAll('3','³').replaceAll('4','⁴').replaceAll('5','⁵').replaceAll('6','⁶').replaceAll('7','⁷').replaceAll('8','⁸').replaceAll('9','⁹')}`;
    document.querySelector('#resolution-fraction').textContent=`${result.resolutionElementPercent.toFixed(4)}% of one resolution element`;
    plotSummary.textContent=velocity===0?'Observed and rest lines are aligned.':`Observed line is ${Math.abs(velocity).toFixed(1)} m/s ${directionPhrase} the rest line.`;
    presetButtons.forEach(button=>button.setAttribute('aria-pressed',String(Number(button.dataset.velocity)===velocity)));
  }

  velocityInput.addEventListener('input',render);
  wavelengthInput.addEventListener('change',render);
  presetButtons.forEach(button=>button.addEventListener('click',()=>{velocityInput.value=button.dataset.velocity;render();velocityInput.focus();}));
  render();
}

function renderBaseMap(){
  const countries=feature(world,world.objects.countries);
  const borders=mesh(world,world.objects.countries,(a,b)=>a!==b);
  document.querySelector('#map-sphere').setAttribute('d',mapPath({type:'Sphere'}));
  document.querySelector('#map-graticule').setAttribute('d',mapPath(geoGraticule10()));
  document.querySelector('#map-countries').setAttribute('d',mapPath(countries));
  document.querySelector('#map-borders').setAttribute('d',mapPath(borders));
}

function setupFigureViewer(){
  const dialog=document.querySelector('#figure-dialog');
  const dialogImage=document.querySelector('#figure-dialog-image');
  const dialogCaption=document.querySelector('#figure-dialog-caption');
  const close=document.querySelector('#figure-close');
  const size=document.querySelector('#figure-size');
  if(!dialog||!dialogImage||!dialogCaption||!close||!size)return;
  let opener=null;
  const setActualSize=enabled=>{
    dialog.classList.toggle('actual-size',enabled);
    size.setAttribute('aria-pressed',String(enabled));
    size.textContent=enabled?'Fit to Window':'View at 100%';
  };
  document.querySelectorAll('.figure-open').forEach(button=>button.addEventListener('click',()=>{
    const image=button.querySelector('img');
    const caption=button.closest('figure')?.querySelector('figcaption');
    if(!image)return;
    opener=button;
    dialogImage.src=image.currentSrc||image.src;
    dialogImage.alt=image.alt;
    dialogCaption.innerHTML=caption?.innerHTML||'';
    setActualSize(false);
    dialog.showModal();
  }));
  const closeDialog=()=>{dialog.close();opener?.focus();};
  close.addEventListener('click',closeDialog);
  size.addEventListener('click',()=>setActualSize(!dialog.classList.contains('actual-size')));
  dialog.addEventListener('click',event=>{if(event.target===dialog)closeDialog();});
}

async function fetchText(path){
  const response=await fetch(path);
  if(!response.ok) throw new Error(`${path} unavailable`);
  return response.text();
}

async function main(){
  renderBaseMap();
  setupDopplerLab();
  setupFigureViewer();
  const paperFiles=['exohspec','expres','harps','espresso','harpsn','neid','kpf','maroonx','carmenes','hpf','spirou','nirps','pfs','sophie','apf','ishell','ird','parvi','paras2','harps3','andes','gclef','hires','uves','chiron','fies','ghost','veloce','hermes','ucles','espadons','tres','igrins','coralie','feros','fideos','pepsi','hds','boes','cafe','ces','coravel','het_hrs','hamilton','tull','elodie','hides','nres','paras','salt_hrs'];
  const [instrumentText,claimText,censusText,facilityText,challengeText,dossierText,paperTexts,beginnerText]=await Promise.all([
    fetchText('./data/instruments.csv'),
    fetchText('./data/performance_claims.csv'),
    fetchText('./data/census_registry.jsonl'),
    fetchText('./data/facilities.jsonl'),
    fetchText('./data/challenge_profiles.json'),
    fetchText('./data/instrument_dossiers.json'),
    Promise.all(paperFiles.map(name=>fetchText(`./data/${name}_papers.csv`))),
    fetchText('./data/beginner_guide.json'),
  ]);
  const instruments=parseCSV(instrumentText), claims=parseCSV(claimText);
  const census=parseJSONL(censusText), facilities=parseJSONL(facilityText), challenges=JSON.parse(challengeText);
  const dossiers=JSON.parse(dossierText), papers=paperTexts.flatMap(parseCSV);
  const beginner=JSON.parse(beginnerText);
  const dossiersById=new Map(dossiers.map(item=>[item.instrument_id,item]));
  const facilitiesById=new Map(facilities.map(item=>[item.facility_id,item]));
  document.querySelector('#census-count').textContent=census.length;
  document.querySelector('#claim-count').textContent=claims.length;
  document.querySelector('#facility-count').textContent=new Set(census.map(d=>d.facility_id)).size;
  document.querySelector('#verified-count').textContent=census.filter(d=>d.verification_state==='verified').length;

  document.querySelector('#measurement-flow').innerHTML=beginner.steps.map(step=>`<article><span>${esc(step.number)}</span><h3>${esc(step.title)}</h3><p>${esc(step.plain_language)}</p><details><summary>Technical note and source</summary><p>${esc(step.technical_note)}</p><a href="${esc(step.source_url)}" rel="noreferrer">${esc(step.source_label)}</a></details></article>`).join('');
  document.querySelector('#equation-grid').innerHTML=beginner.equations.map(item=>`<article><span>${esc(item.name)}</span><div class="display-equation" aria-label="${esc(item.expression)}">${item.mathml}</div><p>${esc(item.meaning)}</p></article>`).join('');
  document.querySelector('#technique-grid').innerHTML=beginner.techniques.map(item=>`<article><h4>${esc(item.name)}</h4><dl><dt>Reference path</dt><dd>${esc(item.reference_path)}</dd><dt>What it solves</dt><dd>${esc(item.what_it_solves)}</dd><dt>Trade-off</dt><dd>${esc(item.tradeoff)}</dd><dt>Example</dt><dd>${esc(item.example)}</dd></dl><a href="${esc(item.source_url)}" rel="noreferrer">Method source</a></article>`).join('');
  document.querySelector('#taxonomy-boundary').textContent=beginner.boundary;
  document.querySelector('#taxonomy-body').innerHTML=beginner.taxonomy.map(item=>`<tr><td>${esc(item.class_name)}</td><td>${esc(item.example)}</td><td>${esc(item.typical_scale)}</td><td><span class="scope-badge ${item.belongs_in_census?'inside':'outside'}">${item.belongs_in_census?'Yes':'Comparator only'}</span></td></tr>`).join('');
  document.querySelector('#space-comparators').innerHTML=beginner.comparators.map(item=>`<article><span>Space comparison</span><h4>${esc(item.name)}</h4><p>${esc(item.why_here)}</p><p><b>Published scope:</b> ${esc(item.fact)}</p><a href="${esc(item.source_url)}" rel="noreferrer">Official documentation</a></article>`).join('');

  const mappedFacilities=facilities.filter(item=>Number.isFinite(item.latitude_deg)&&Number.isFinite(item.longitude_deg)&&census.some(row=>row.facility_id===item.facility_id));
  const mapDetail=document.querySelector('#map-detail');
  const facilityInstruments=id=>census.filter(row=>row.facility_id===id);
  document.querySelector('#world-map').insertAdjacentHTML('beforeend',mappedFacilities.map(item=>{const [x,y]=mapProjection([item.longitude_deg,item.latitude_deg]);const left=x/10;const top=y/5;const count=facilityInstruments(item.facility_id).length;const size=26+Math.min(18,(count-1)*4);return `<button type="button" class="map-marker" data-facility="${esc(item.facility_id)}" data-label="${esc(item.official_name)}" style="left:${left.toFixed(3)}%;top:${top.toFixed(3)}%;--marker-size:${size}px" aria-label="${esc(item.official_name)}, ${esc(item.site)}; ${count} instrument records"><span>${count}</span></button>`}).join(''));
  document.querySelector('#map-summary').textContent=`${mappedFacilities.length} of ${facilities.filter(item=>census.some(row=>row.facility_id===item.facility_id)).length} represented facilities currently have a source-linked coordinate.`;
  document.querySelector('#map-sites').innerHTML=mappedFacilities.sort((a,b)=>a.official_name.localeCompare(b.official_name)).map(item=>`<article><button type="button" data-facility-index="${esc(item.facility_id)}">${esc(item.official_name)}</button><span>${esc(item.site)} · ${esc(item.latitude_deg.toFixed(4))}, ${esc(item.longitude_deg.toFixed(4))}</span><a href="${esc(item.coordinate_source_url)}" rel="noreferrer">Coordinate source</a></article>`).join('');
  function selectFacility(id,scrollToDirectory=false){
    const facility=facilitiesById.get(id);if(!facility)return;
    const represented=facilityInstruments(id);
    document.querySelectorAll('.map-marker').forEach(marker=>marker.setAttribute('aria-pressed',String(marker.dataset.facility===id)));
    mapDetail.innerHTML=`<span class="eyebrow">Selected Observatory</span><h3>${esc(facility.official_name)}</h3><p>${esc(facility.site)} · ${esc(facility.latitude_deg.toFixed(4))}, ${esc(facility.longitude_deg.toFixed(4))}</p><div class="map-instrument-list">${represented.map(item=>`<button type="button" onclick="openInstrumentProfile('${esc(item.instrument_id)}')">${esc(item.acronym||item.official_name)}</button>`).join('')}</div><div class="map-detail-links"><a href="${esc(facility.coordinate_source_url)}" rel="noreferrer">Coordinate source</a><button type="button" id="map-filter-directory">Show These Instruments in the Directory</button></div>`;
    document.querySelector('#map-filter-directory').addEventListener('click',()=>{censusSearch.value=facility.site;renderCensus();document.querySelector('#census').scrollIntoView();});
    if(scrollToDirectory){censusSearch.value=facility.site;renderCensus();document.querySelector('#census').scrollIntoView();}
  }
  document.querySelectorAll('.map-marker').forEach(marker=>marker.addEventListener('click',()=>selectFacility(marker.dataset.facility)));
  document.querySelectorAll('[data-facility-index]').forEach(button=>button.addEventListener('click',()=>selectFacility(button.dataset.facilityIndex)));

  const censusSearch=document.querySelector('#census-search');
  const tierFilter=document.querySelector('#tier-filter');
  const verificationFilter=document.querySelector('#verification-filter');
  Object.entries(tierLabels).forEach(([value,label])=>tierFilter.add(new Option(label,value)));
  const dialog=document.querySelector('#instrument-dialog');
  const dialogContent=document.querySelector('#dialog-content');
  const closeDialog=()=>{dialog.close();history.replaceState(null,'',location.pathname+location.search+'#census')};
  document.querySelector('#dialog-close').addEventListener('click',closeDialog);
  dialog.addEventListener('click',event=>{if(event.target===dialog)closeDialog()});

  function matchingClaims(item){
    const normalize=value=>String(value??'').toLowerCase().replace(/[^a-z0-9]/g,'');
    const keys=[item.acronym,item.official_name,...(item.aliases||[])].filter(Boolean).map(normalize);
    return claims.filter(claim=>keys.includes(normalize(claim.instrument)));
  }
  function depthFor(item){
    const dossier=dossiersById.get(item.instrument_id);
    if(dossier)return {label:`Research note · ${dossier.paper_count} papers`,className:'full'};
    if(matchingClaims(item).length)return {label:'Numbers from published studies',className:'quantitative'};
    return {label:'Source-linked instrument note',className:'source'};
  }
  function proposedNextCheck(paper,project,index){
    const text=`${paper.what_was_studied} ${paper.remaining_question}`.toLowerCase();
    if(/not been built|requirement|design study|future milestone|construction/.test(text))return 'Compare the published requirement with a dated as-built acceptance or commissioning measurement using the same metric and configuration.';
    if(/status|availability|available|operat|decommission|first light/.test(text))return 'Locate a dated observatory operations record and separate physical installation, commissioning, offered availability and routine science use.';
    if(/internal uncertainty|formal uncertainty|rms|scatter|different quantities|sample/.test(text))return 'Report formal uncertainty, repeatability and residual RMS side by side for a common target set and an explicitly stated time baseline.';
    if(/calibrat|wavelength|drift|comb|etalon|metalon/.test(text))return 'Test whether the calibration diagnostic predicts held-out stellar or solar velocities across nights, instrument states and maintenance eras.';
    if(/activity|line shape|planet|kepler|stellar signal/.test(text))return 'Use time-blocked validation and injected Keplerian signals to measure correction bias, signal recovery and false positives.';
    if(/fibre|fiber|modal|illumination|scrambl|throughput/.test(text))return 'Measure stability and throughput together across illumination, fibre and agitation states so that a gain in one quantity does not hide a loss in another.';
    if(/pipeline|template|reduction|algorithm|method/.test(text))return 'Freeze the software and calibration inputs, then compare methods on the same exposures with blinded or held-out epochs.';
    if(/telluric|atmospher|water|airmass/.test(text))return 'Compare masking and forward modelling on matched spectra spanning airmass and water-vapour conditions, with wavelength-dependent residuals reported.';
    if(/long-term|year|era|maintenance|temperature|thermal/.test(text))return 'Define instrument eras before fitting and validate on complete held-out time blocks that include maintenance or environmental transitions.';
    return project?.steps?.[index%project.steps.length]||'Reproduce the reported number from identified data and configuration records before extending the analysis.';
  }
  function renderDossier(dossier){
    if(!dossier)return '';
    const selected=papers.filter(paper=>dossier.paper_ids.includes(paper.paper_id));
    const project=dossier.future_analysis;
    const text=value=>esc(editorialText(value));
    return `<section class="dossier-block"><div class="dossier-label">Research note · ${esc(dossier.paper_count)} sources · reviewed through ${esc(dossier.reviewed_through)}</div><h3>${text(dossier.title)}</h3><p class="dossier-summary">${text(dossier.short_summary)}</p><p class="reading-boundary"><b>Scope:</b> ${text(dossier.reading_boundary)}</p><div class="latest-reading"><span class="eyebrow">Latest Source</span><h4>What changes in the current picture?</h4><p>${text(dossier.latest_problem)}</p><a href="${esc(dossier.latest_problem_source)}" rel="noreferrer">Read the latest primary or official source</a></div><h4>Cross-Paper Synthesis</h4><ol class="synthesis-list">${dossier.lessons.map(item=>`<li>${text(item)}</li>`).join('')}</ol><div class="paper-section-head"><div><span class="eyebrow">Paper-by-Paper</span><h4>Questions, Results and Remaining Tests</h4></div><p>Each note separates the team's published result from my proposed next check.</p></div><div class="paper-list">${selected.map((paper,index)=>`<details class="paper-note" ${index===0?'open':''}><summary><span>${esc(paper.year)} · ${text(paper.paper_type)}</span><strong>${text(paper.title)}</strong><small>${text(paper.authors)}</small></summary><div class="paper-qa"><section><h5>Question Addressed</h5><p>${text(paper.what_was_studied)}</p></section><section><h5>What the Team Reported</h5><p>${text(paper.numerical_result)}</p></section><section><h5>What Remains Unresolved</h5><p>${text(paper.remaining_question)}</p></section><section class="author-check"><h5>Author's Next Check</h5><p>${text(proposedNextCheck(paper,project,index))}</p><small>Interpretation by Biswajit Jana; not an endorsed recommendation from the paper's authors or instrument team.</small></section><a href="${esc(paper.source_url)}" rel="noreferrer">Open Primary or Official Source</a></div></details>`).join('')}</div><div class="project-note"><span class="dossier-label">Proposed Research Extension</span><h4>${text(project.title)}</h4><p><b>Research question:</b> ${text(project.question)}</p><p>${text(project.basis)}</p><p class="reading-boundary"><b>Status:</b> ${text(project.status)}.</p><h5>Tests That Would Make the Result Stronger</h5><ol>${project.steps.map(item=>`<li>${text(item)}</li>`).join('')}</ol></div></section>`;
  }
  function openProfile(id,updateHistory=true){
    const item=census.find(row=>row.instrument_id===id); if(!item)return;
    const related=matchingClaims(item);
    const depth=depthFor(item), dossier=dossiersById.get(item.instrument_id);
    const unresolved=item.unresolved_fields?.length?`<section class="profile-warning"><h3>Still unresolved</h3><ul>${item.unresolved_fields.map(value=>`<li>${esc(editorialText(value))}</li>`).join('')}</ul></section>`:'';
    const evidence=related.length?`<section><h3>Published Numerical Evidence in This Release</h3>${related.map(record=>`<article class="profile-claim"><strong>${esc(editorialText(record.reported_result))}</strong><p>${esc(words(record.measurement_context))}; ${esc(editorialText(record.target_or_sample))}; ${esc(editorialText(record.baseline))}.</p><p><b>Limit:</b> ${esc(editorialText(record.caveat))}</p><a href="${esc(record.source_url)}" rel="noreferrer">Read the primary source</a></article>`).join('')}</section>`:`<section><h3>Performance Evidence</h3><p>No source-linked precision record is included in this release. The directory entry establishes the instrument record, not an achieved performance value.</p></section>`;
    dialogContent.innerHTML=`<h2 id="dialog-title">${esc(item.acronym||item.official_name)}</h2><p class="profile-name">${esc(item.official_name)}</p><div class="profile-meta"><div><span>Facility</span><b>${esc(item.site)}</b></div><div><span>Telescope</span><b>${esc(item.telescope)}</b></div><div><span>Status</span><b>${esc(words(item.current_status))}${item.status_as_of?` · ${esc(item.status_as_of)}`:''}</b></div><div><span>Research status</span><b>${esc(depth.label)}</b></div></div><section><h3>What I could verify</h3><p>${esc(editorialText(item.notes))}</p></section>${renderDossier(dossier)}${evidence}${unresolved}<section><h3>Sources and instrument pages</h3><div class="source-links"><a href="${esc(item.primary_source_url)}" rel="noreferrer">Primary paper or technical source</a><a href="${esc(item.official_instrument_url)}" rel="noreferrer">Official instrument page</a>${item.status_source_url?`<a href="${esc(item.status_source_url)}" rel="noreferrer">Dated status source</a>`:''}</div></section>`;
    if(!dialog.open)dialog.showModal();
    if(updateHistory)history.replaceState(null,'',`#instrument=${encodeURIComponent(id)}`);
  }
  window.openInstrumentProfile=openProfile;

  function renderCensus(){
    const query=censusSearch.value.trim().toLowerCase();
    const filtered=census.filter(item=>{
      const haystack=[item.official_name,item.acronym,item.telescope,item.site,item.physical_country_or_territory,item.facility_id,...(item.aliases||[])].join(' ').toLowerCase();
      const hasDatedStatus=Boolean(item.status_source_url&&item.status_as_of&&item.current_status!=='not_verified');
      const statusMatches=!verificationFilter.value||(verificationFilter.value==='dated'?hasDatedStatus:!hasDatedStatus);
      return (!query||haystack.includes(query))&&(!tierFilter.value||item.inclusion_tier===tierFilter.value)&&statusMatches;
    }).sort((a,b)=>(a.acronym||a.official_name).localeCompare(b.acronym||b.official_name));
    document.querySelector('#census-result').textContent=`Showing ${filtered.length} of ${census.length} physical-instrument records`;
    document.querySelector('#census-grid').innerHTML=filtered.map(item=>{const depth=depthFor(item);const facility=facilitiesById.get(item.facility_id);const dated=Boolean(item.status_source_url&&item.status_as_of&&item.current_status!=='not_verified');const located=Boolean(facility&&Number.isFinite(facility.latitude_deg));return `<article class="census-card"><div class="card-top"><span class="tier">${esc(tierLabels[item.inclusion_tier])}</span></div><h3>${esc(item.acronym||item.official_name)}</h3><p>${esc(item.official_name)}</p><div class="evidence-checks" aria-label="Evidence checks"><span class="checked">Existence source</span><span class="${dated?'checked':'open'}">${dated?'Dated status':'Status check open'}</span><span class="${located?'checked':'open'}">${located?'Mapped':'Coordinate open'}</span></div><span class="depth ${esc(depth.className)}">${esc(depth.label)}</span><dl><dt>Site</dt><dd>${esc(item.site)}</dd><dt>Status</dt><dd>${esc(words(item.current_status))}</dd></dl><button type="button" onclick="openInstrumentProfile('${esc(item.instrument_id)}')">Read note and sources</button></article>`}).join('');
  }
  [censusSearch,tierFilter,verificationFilter].forEach(el=>el.addEventListener('input',renderCensus));
  renderCensus();
  window.focusFacility=id=>selectFacility(id,true);

  const statusSelect=document.querySelector('#status-filter'), bandSelect=document.querySelector('#band-filter'), search=document.querySelector('#search');
  [...new Set(instruments.map(d=>d.status))].sort().forEach(status=>statusSelect.add(new Option(words(status),status)));
  function renderInstruments(){const q=search.value.trim().toLowerCase();const filtered=instruments.filter(d=>(!q||`${d.instrument} ${d.facility}`.toLowerCase().includes(q))&&(!statusSelect.value||d.status===statusSelect.value)&&(!bandSelect.value||d.spectral_domain===bandSelect.value));document.querySelector('#table-result').textContent=`Showing ${filtered.length} of ${instruments.length} performance-core records`;document.querySelector('#instrument-body').innerHTML=filtered.map(d=>`<tr><td>${esc(d.instrument)}</td><td>${esc(d.facility)}</td><td>${esc(d.wave_min_nm)}–${esc(d.wave_max_nm)} nm</td><td>${Number(d.resolving_power).toLocaleString()}</td><td><span class="pill ${esc(d.status)}">${esc(words(d.status))}</span></td><td>${esc(words(d.performance_class))}</td></tr>`).join('')}
  [search,statusSelect,bandSelect].forEach(el=>el.addEventListener('input',renderInstruments));renderInstruments();

  const cardClass=c=>c.measurement_context.includes('requirement')?'requirement':c.measurement_context.includes('calibration')?'calibration':'sky';
  document.querySelector('#claim-grid').innerHTML=claims.map(c=>`<article class="claim ${cardClass(c)}"><header><h3>${esc(c.instrument)}</h3><span class="value">${esc(c.comparison==='upper_bound'?'< ':c.comparison==='approximately'?'≈ ':'')}${esc(c.value_mps)} m/s</span></header><p>${esc(editorialText(c.reported_result))}</p><p class="context">${esc(words(c.measurement_context))}</p><details><summary>Context and source</summary><dl><dt>Metric</dt><dd>${esc(words(c.metric))}</dd><dt>Sample</dt><dd>${esc(editorialText(c.target_or_sample))}</dd><dt>Baseline</dt><dd>${esc(editorialText(c.baseline))}</dd><dt>Limit</dt><dd>${esc(editorialText(c.caveat))}</dd></dl><a href="${esc(c.source_url)}" rel="noreferrer">Primary source</a></details></article>`).join('');

  document.querySelector('#barrier-articles').innerHTML=challenges.map((item,index)=>`<article class="barrier-article" id="${esc(item.id)}"><header><span>${String(index+1).padStart(2,'0')}</span><div><h3>${esc(editorialText(item.title))}</h3><p>${esc(editorialText(item.question))}</p></div></header><div class="barrier-body"><section><h4>Physical mechanism</h4><p>${esc(editorialText(item.mechanism))}</p></section><section><h4>Published example</h4><p>${esc(editorialText(item.evidence))}</p></section><section><h4>Mitigation and remaining limit</h4><p>${esc(editorialText(item.mitigation))}</p><p><b>Residual:</b> ${esc(editorialText(item.residual))}</p></section><div class="source-links">${item.sources.map(source=>`<a href="${esc(source.url)}" rel="noreferrer">${esc(editorialText(source.label))}</a>`).join('')}</div></div></article>`).join('');

  const exohspec=dossiersById.get('tno-exohspec');
  document.querySelector('#current-focus-card').innerHTML=`<header><span class="eyebrow">Current Research Context</span><h2>EXOhSPEC: Earlier Work and the Present System</h2><p>EXOhSPEC is the practical origin of this literature study. The collected sources describe earlier designs, prototypes and subsystem experiments; they do not validate the present instrument configuration or establish completed stellar-RV performance for the Thai instrument.</p></header><div class="dossier-index"><article><span>${esc(exohspec.paper_count)} selected sources</span><h3>${esc(editorialText(exohspec.title))}</h3><p>${esc(editorialText(exohspec.short_summary))}</p><button type="button" class="button primary" onclick="openInstrumentProfile('tno-exohspec')">Open the Concise EXOhSPEC Note</button></article></div>`;
  document.querySelector('#featured-dossier').innerHTML=`<header><span class="eyebrow">Instrument Research Notes</span><h2>From Published Measurements to Testable Questions</h2><p>Each note reconstructs a selected source trail paper by paper: the question addressed, the reported result, the unresolved limitation, and a clearly labelled next check proposed by this synthesis.</p></header><div class="dossier-index">${dossiers.filter(dossier=>dossier.instrument_id!=='tno-exohspec').map(dossier=>`<article><span>${esc(dossier.paper_count)} selected sources</span><h3>${esc(editorialText(dossier.title))}</h3><p>${esc(editorialText(dossier.short_summary))}</p><button type="button" class="button primary" onclick="openInstrumentProfile('${esc(dossier.instrument_id)}')">Open Research Note</button></article>`).join('')}</div>`;

  const hash=decodeURIComponent(location.hash);
  if(hash.startsWith('#instrument=')) openProfile(hash.slice(12),false);
}

main().catch(error=>{
  document.querySelector('#census-result').textContent=`Data could not be loaded: ${error.message}`;
});
