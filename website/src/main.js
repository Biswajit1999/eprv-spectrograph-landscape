import './style.css';

const parseCSV = text => {
  const rows=[]; let row=[], field='', quoted=false;
  for(let i=0;i<text.length;i++){const c=text[i],n=text[i+1];if(c==='"'&&quoted&&n==='"'){field+='"';i++;}else if(c==='"'){quoted=!quoted;}else if(c===','&&!quoted){row.push(field);field='';}else if((c==='\n'||c==='\r')&&!quoted){if(c==='\r'&&n==='\n')i++;row.push(field);if(row.some(Boolean))rows.push(row);row=[];field='';}else field+=c;}
  if(field||row.length){row.push(field);rows.push(row)} const headers=rows.shift();
  return rows.map(values=>Object.fromEntries(headers.map((h,i)=>[h,values[i]??''])));
};

const parseJSONL = text => text.split(/\r?\n/).filter(Boolean).map(line => JSON.parse(line));
const esc = value => String(value ?? '').replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
const words = value => String(value ?? '').replaceAll('_',' ');
const tierLabels = {
  A_dedicated_prv_eprv: 'A · Dedicated PRV/EPRV',
  B_general_high_resolution_with_rv_evidence: 'B · High-resolution with RV evidence',
  C_historical_prototype_or_specialist: 'C · Historical or specialist',
  D_funded_construction_or_commissioning: 'D · Construction or commissioning',
};

async function fetchText(path){
  const response=await fetch(path);
  if(!response.ok) throw new Error(`${path} unavailable`);
  return response.text();
}

async function main(){
  const [instrumentText,claimText,censusText,facilityText,challengeText,dossierText,exohspecPaperText,expresPaperText,harpsPaperText,espressoPaperText,harpsnPaperText,neidPaperText,beginnerText]=await Promise.all([
    fetchText('./data/instruments.csv'),
    fetchText('./data/performance_claims.csv'),
    fetchText('./data/census_registry.jsonl'),
    fetchText('./data/facilities.jsonl'),
    fetchText('./data/challenge_profiles.json'),
    fetchText('./data/instrument_dossiers.json'),
    fetchText('./data/exohspec_papers.csv'),
    fetchText('./data/expres_papers.csv'),
    fetchText('./data/harps_papers.csv'),
    fetchText('./data/espresso_papers.csv'),
    fetchText('./data/harpsn_papers.csv'),
    fetchText('./data/neid_papers.csv'),
    fetchText('./data/beginner_guide.json'),
  ]);
  const instruments=parseCSV(instrumentText), claims=parseCSV(claimText);
  const census=parseJSONL(censusText), facilities=parseJSONL(facilityText), challenges=JSON.parse(challengeText);
  const dossiers=JSON.parse(dossierText), papers=[...parseCSV(exohspecPaperText),...parseCSV(expresPaperText),...parseCSV(harpsPaperText),...parseCSV(espressoPaperText),...parseCSV(harpsnPaperText),...parseCSV(neidPaperText)];
  const beginner=JSON.parse(beginnerText);
  const dossiersById=new Map(dossiers.map(item=>[item.instrument_id,item]));
  const facilitiesById=new Map(facilities.map(item=>[item.facility_id,item]));
  document.querySelector('#census-count').textContent=census.length;
  document.querySelector('#claim-count').textContent=claims.length;
  document.querySelector('#facility-count').textContent=new Set(census.map(d=>d.facility_id)).size;
  document.querySelector('#verified-count').textContent=census.filter(d=>d.verification_state==='verified').length;

  document.querySelector('#measurement-flow').innerHTML=beginner.steps.map(step=>`<article><span>${esc(step.number)}</span><h3>${esc(step.title)}</h3><p>${esc(step.plain_language)}</p><details><summary>Technical note and source</summary><p>${esc(step.technical_note)}</p><a href="${esc(step.source_url)}" rel="noreferrer">${esc(step.source_label)}</a></details></article>`).join('');
  document.querySelector('#equation-grid').innerHTML=beginner.equations.map(item=>`<article><span>${esc(item.name)}</span><strong>${esc(item.expression)}</strong><p>${esc(item.meaning)}</p></article>`).join('');
  document.querySelector('#technique-grid').innerHTML=beginner.techniques.map(item=>`<article><h4>${esc(item.name)}</h4><dl><dt>Reference path</dt><dd>${esc(item.reference_path)}</dd><dt>What it solves</dt><dd>${esc(item.what_it_solves)}</dd><dt>Trade-off</dt><dd>${esc(item.tradeoff)}</dd><dt>Example</dt><dd>${esc(item.example)}</dd></dl><a href="${esc(item.source_url)}" rel="noreferrer">Method source</a></article>`).join('');
  document.querySelector('#taxonomy-boundary').textContent=beginner.boundary;
  document.querySelector('#taxonomy-body').innerHTML=beginner.taxonomy.map(item=>`<tr><td>${esc(item.class_name)}</td><td>${esc(item.example)}</td><td>${esc(item.typical_scale)}</td><td><span class="scope-badge ${item.belongs_in_census?'inside':'outside'}">${item.belongs_in_census?'Yes':'Comparator only'}</span></td></tr>`).join('');
  document.querySelector('#space-comparators').innerHTML=beginner.comparators.map(item=>`<article><span>Space comparison</span><h4>${esc(item.name)}</h4><p>${esc(item.why_here)}</p><p><b>Published scope:</b> ${esc(item.fact)}</p><a href="${esc(item.source_url)}" rel="noreferrer">Official documentation</a></article>`).join('');

  const mappedFacilities=facilities.filter(item=>Number.isFinite(item.latitude_deg)&&Number.isFinite(item.longitude_deg)&&census.some(row=>row.facility_id===item.facility_id));
  document.querySelector('#world-map').insertAdjacentHTML('beforeend',mappedFacilities.map(item=>{const left=(item.longitude_deg+180)/360*100;const top=(90-item.latitude_deg)/180*100;const count=census.filter(row=>row.facility_id===item.facility_id).length;return `<button type="button" class="map-marker" style="left:${left}%;top:${top}%" aria-label="${esc(item.official_name)}, ${esc(item.site)}; ${count} instrument records" title="${esc(item.official_name)} · ${count} records" onclick="focusFacility('${esc(item.facility_id)}')"><span>${count}</span></button>`}).join(''));
  document.querySelector('#map-summary').textContent=`${mappedFacilities.length} of ${facilities.filter(item=>census.some(row=>row.facility_id===item.facility_id)).length} represented facilities currently have a source-linked coordinate.`;
  document.querySelector('#map-sites').innerHTML=mappedFacilities.map(item=>`<article><b>${esc(item.official_name)}</b><span>${esc(item.latitude_deg.toFixed(4))}, ${esc(item.longitude_deg.toFixed(4))}</span><a href="${esc(item.coordinate_source_url)}" rel="noreferrer">Coordinate source</a></article>`).join('');

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
    const keys=[item.acronym,item.official_name,...(item.aliases||[])].filter(Boolean).map(v=>v.toLowerCase());
    return claims.filter(claim=>keys.some(key=>claim.instrument.toLowerCase()===key || key.includes(claim.instrument.toLowerCase())));
  }
  function depthFor(item){
    const dossier=dossiersById.get(item.instrument_id);
    if(dossier)return {label:`Selected reading note · ${dossier.paper_count} papers`,className:'full'};
    if(matchingClaims(item).length)return {label:'Numbers from published studies',className:'quantitative'};
    return {label:'Source-linked instrument note',className:'source'};
  }
  function renderDossier(dossier){
    if(!dossier)return '';
    const selected=papers.filter(paper=>dossier.paper_ids.includes(paper.paper_id));
    const project=dossier.future_analysis;
    return `<section class="dossier-block"><div class="dossier-label">Selected reading note · ${esc(dossier.paper_count)} sources · reviewed through ${esc(dossier.reviewed_through)}</div><h3>${esc(dossier.title)}</h3><p>${esc(dossier.short_summary)}</p><p class="reading-boundary"><b>Reading boundary:</b> ${esc(dossier.reading_boundary)}</p><h4>What the latest source changes</h4><p>${esc(dossier.latest_problem)}</p><a href="${esc(dossier.latest_problem_source)}" rel="noreferrer">Read the latest primary or official source</a><h4>Five lessons from the reading path</h4><ol>${dossier.lessons.map(item=>`<li>${esc(item)}</li>`).join('')}</ol><h4>Selected sources, in time order</h4><div class="paper-list">${selected.map(paper=>`<article><div><span>${esc(paper.year)} · ${esc(paper.paper_type)}</span><h5>${esc(paper.title)}</h5><p>${esc(paper.what_was_studied)}</p><p><b>Reported:</b> ${esc(paper.numerical_result)}</p><p><b>Still open:</b> ${esc(paper.remaining_question)}</p></div><a href="${esc(paper.source_url)}" rel="noreferrer">Primary or official source</a></article>`).join('')}</div><div class="project-note"><span class="dossier-label">Future analysis question</span><h4>${esc(project.title)}</h4><p><b>Question:</b> ${esc(project.question)}</p><p>${esc(project.basis)}</p><p class="reading-boundary"><b>Boundary:</b> ${esc(project.status)}.</p><h5>Possible checks</h5><ol>${project.steps.map(item=>`<li>${esc(item)}</li>`).join('')}</ol></div></section>`;
  }
  function openProfile(id,updateHistory=true){
    const item=census.find(row=>row.instrument_id===id); if(!item)return;
    const related=matchingClaims(item);
    const depth=depthFor(item), dossier=dossiersById.get(item.instrument_id);
    const unresolved=item.unresolved_fields?.length?`<section class="profile-warning"><h3>Still unresolved</h3><ul>${item.unresolved_fields.map(value=>`<li>${esc(value)}</li>`).join('')}</ul></section>`:'';
    const evidence=related.length?`<section><h3>Published quantitative evidence in this release</h3>${related.map(claim=>`<article class="profile-claim"><strong>${esc(claim.reported_result)}</strong><p>${esc(words(claim.measurement_context))}; ${esc(claim.target_or_sample)}; ${esc(claim.baseline)}.</p><p><b>Limit:</b> ${esc(claim.caveat)}</p><a href="${esc(claim.source_url)}" rel="noreferrer">Read the primary source</a></article>`).join('')}</section>`:`<section><h3>Performance evidence</h3><p>No claim-level precision record has passed this release's extraction gate. The census row is not a performance claim.</p></section>`;
    dialogContent.innerHTML=`<h2 id="dialog-title">${esc(item.acronym||item.official_name)}</h2><p class="profile-name">${esc(item.official_name)}</p><div class="profile-meta"><div><span>Facility</span><b>${esc(item.site)}</b></div><div><span>Telescope</span><b>${esc(item.telescope)}</b></div><div><span>Status</span><b>${esc(words(item.current_status))}${item.status_as_of?` · ${esc(item.status_as_of)}`:''}</b></div><div><span>Research status</span><b>${esc(depth.label)}</b></div></div><section><h3>What I could verify</h3><p>${esc(item.notes)}</p></section>${renderDossier(dossier)}${evidence}${unresolved}<section><h3>Sources and instrument pages</h3><div class="source-links"><a href="${esc(item.primary_source_url)}" rel="noreferrer">Primary paper or technical source</a><a href="${esc(item.official_instrument_url)}" rel="noreferrer">Official instrument page</a>${item.status_source_url?`<a href="${esc(item.status_source_url)}" rel="noreferrer">Dated status source</a>`:''}</div></section>`;
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
    }).sort((a,b)=>Number(b.instrument_id==='tno-exohspec')-Number(a.instrument_id==='tno-exohspec'));
    document.querySelector('#census-result').textContent=`Showing ${filtered.length} of ${census.length} physical-instrument records`;
    document.querySelector('#census-grid').innerHTML=filtered.map(item=>{const depth=depthFor(item);const facility=facilitiesById.get(item.facility_id);const dated=Boolean(item.status_source_url&&item.status_as_of&&item.current_status!=='not_verified');const located=Boolean(facility&&Number.isFinite(facility.latitude_deg));return `<article class="census-card"><div class="card-top"><span class="tier">${esc(tierLabels[item.inclusion_tier])}</span></div><h3>${esc(item.acronym||item.official_name)}</h3><p>${esc(item.official_name)}</p><div class="evidence-checks" aria-label="Evidence checks"><span class="checked">Existence source</span><span class="${dated?'checked':'open'}">${dated?'Dated status':'Status check open'}</span><span class="${located?'checked':'open'}">${located?'Mapped':'Coordinate open'}</span></div><span class="depth ${esc(depth.className)}">${esc(depth.label)}</span><dl><dt>Site</dt><dd>${esc(item.site)}</dd><dt>Status</dt><dd>${esc(words(item.current_status))}</dd></dl><button type="button" onclick="openInstrumentProfile('${esc(item.instrument_id)}')">Read note and sources</button></article>`}).join('');
  }
  [censusSearch,tierFilter,verificationFilter].forEach(el=>el.addEventListener('input',renderCensus));
  renderCensus();
  window.focusFacility=id=>{const facility=facilitiesById.get(id);if(!facility)return;censusSearch.value=facility.site;renderCensus();document.querySelector('#census').scrollIntoView();};

  const statusSelect=document.querySelector('#status-filter'), bandSelect=document.querySelector('#band-filter'), search=document.querySelector('#search');
  [...new Set(instruments.map(d=>d.status))].sort().forEach(status=>statusSelect.add(new Option(words(status),status)));
  function renderInstruments(){const q=search.value.trim().toLowerCase();const filtered=instruments.filter(d=>(!q||`${d.instrument} ${d.facility}`.toLowerCase().includes(q))&&(!statusSelect.value||d.status===statusSelect.value)&&(!bandSelect.value||d.spectral_domain===bandSelect.value));document.querySelector('#table-result').textContent=`Showing ${filtered.length} of ${instruments.length} performance-core records`;document.querySelector('#instrument-body').innerHTML=filtered.map(d=>`<tr><td>${esc(d.instrument)}</td><td>${esc(d.facility)}</td><td>${esc(d.wave_min_nm)}–${esc(d.wave_max_nm)} nm</td><td>${Number(d.resolving_power).toLocaleString()}</td><td><span class="pill ${esc(d.status)}">${esc(words(d.status))}</span></td><td>${esc(words(d.performance_class))}</td></tr>`).join('')}
  [search,statusSelect,bandSelect].forEach(el=>el.addEventListener('input',renderInstruments));renderInstruments();

  const cardClass=c=>c.measurement_context.includes('requirement')?'requirement':c.measurement_context.includes('calibration')?'calibration':'sky';
  document.querySelector('#claim-grid').innerHTML=claims.map(c=>`<article class="claim ${cardClass(c)}"><header><h3>${esc(c.instrument)}</h3><span class="value">${esc(c.comparison==='upper_bound'?'< ':c.comparison==='approximately'?'≈ ':'')}${esc(c.value_mps)} m/s</span></header><p>${esc(c.reported_result)}</p><p class="context">${esc(words(c.measurement_context))}</p><details><summary>Context and source</summary><dl><dt>Metric</dt><dd>${esc(words(c.metric))}</dd><dt>Sample</dt><dd>${esc(c.target_or_sample)}</dd><dt>Baseline</dt><dd>${esc(c.baseline)}</dd><dt>Limit</dt><dd>${esc(c.caveat)}</dd></dl><a href="${esc(c.source_url)}" rel="noreferrer">Primary source</a></details></article>`).join('');

  document.querySelector('#barrier-articles').innerHTML=challenges.map((item,index)=>`<article class="barrier-article" id="${esc(item.id)}"><header><span>${String(index+1).padStart(2,'0')}</span><div><h3>${esc(item.title)}</h3><p>${esc(item.question)}</p></div></header><div class="barrier-body"><section><h4>Physical mechanism</h4><p>${esc(item.mechanism)}</p></section><section><h4>Published example</h4><p>${esc(item.evidence)}</p></section><section><h4>Mitigation and remaining limit</h4><p>${esc(item.mitigation)}</p><p><b>Residual:</b> ${esc(item.residual)}</p></section><div class="source-links">${item.sources.map(source=>`<a href="${esc(source.url)}" rel="noreferrer">${esc(source.label)}</a>`).join('')}</div></div></article>`).join('');

  const exohspec=dossiersById.get('tno-exohspec');
  document.querySelector('#current-focus-card').innerHTML=`<header><span class="eyebrow">Current reading focus</span><h2>EXOhSPEC: what the selected sources establish</h2><p>Design goals, laboratory measurements, deployment history and current status are kept separate. No selected source is used to claim completed stellar-RV performance for the Thai instrument.</p></header><div class="dossier-index"><article><span>${esc(exohspec.paper_count)} selected sources</span><h3>${esc(exohspec.title)}</h3><p>${esc(exohspec.short_summary)}</p><p class="reading-boundary"><b>Status boundary:</b> ${esc(exohspec.current_status)}</p><button type="button" class="button primary" onclick="openInstrumentProfile('tno-exohspec')">Read the EXOhSPEC note</button></article></div>`;
  document.querySelector('#featured-dossier').innerHTML=`<header><span class="eyebrow">Instrument reading notes</span><h2>From published measurements to open analysis questions</h2><p>Each note follows a selected source trail, keeps measurement contexts separate, and ends with a future analysis question—not a claim of completed research or endorsement.</p></header><div class="dossier-index">${dossiers.map(dossier=>`<article><span>${esc(dossier.paper_count)} selected sources</span><h3>${esc(dossier.title)}</h3><p>${esc(dossier.short_summary)}</p><button type="button" class="button primary" onclick="openInstrumentProfile('${esc(dossier.instrument_id)}')">Read sources and analysis checks</button></article>`).join('')}</div>`;

  const hash=decodeURIComponent(location.hash);
  if(hash.startsWith('#instrument=')) openProfile(hash.slice(12),false);
}

main().catch(error=>{
  document.querySelector('#census-result').textContent=`Data could not be loaded: ${error.message}`;
});
