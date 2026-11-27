"""Project index and individual reading pages."""
from .common import data, e, link, icon


def photo(page, item):
    v = item[page.lang]
    width, height = item['imageSize']
    return f'<figure class="evidence-photo"><img width="{width}" height="{height}" loading="lazy" alt="{e(v["alt"])}" src="{page.asset("images/"+item["image"])}"><figcaption>{e(v["caption"])}</figcaption></figure>'


def drawing(slug):
    # Concept illustrations of a headless audio server and a persisted message queue.
    if slug == 'soft-and-wet-homelab':
        shapes = '<path d="m27 72 99-40 83 28-100 43zM27 72v21l82 31 100-43V60M109 102v22m-66-44 45 17m-45-11 29 11"/><path d="m180 72 14-6" stroke-width="3"/>'
        return f'<svg class="study-art" viewBox="0 0 242 150" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5">{shapes}</svg>'
    if slug == 'oppy':
        shapes = ''.join(f'<path d="m{x} {y} 62-23 49 22-62 24z"/>' for x,y in [(36,94),(52,76),(68,58),(84,40)])
        return f'<svg class="study-art" viewBox="0 0 230 150" aria-hidden="true" fill="#18273b" stroke="currentColor" stroke-width="1.5">{shapes}</svg>'
    return ''


def selected_work(page, projects):
    t = page.t
    lookup = {p['id']: p for p in projects}
    lead = lookup['enterprise-noc-from-scratch']
    v = lead[page.lang]
    name = 'Enterprise NOC'
    featured = f'''
<article class="lead-case" id="{lead['id']}">{photo(page,lead)}
  <div class="lead-copy">
    <p class="section-label">{e(v['kind'])}</p>
    <h3><a href="{page.project(lead['id'])}">{name}<span>From Scratch</span></a></h3>
    <p>{e(v['summary'])}</p>{link(page.project(lead['id']),t['read'],'right','ink-button')}
  </div>
</article>
'''
    studies = []
    study_ids = ['soft-and-wet-homelab','oppy']
    for slug in study_ids:
        p = lookup[slug]
        v = p[page.lang]
        studies.append(f'''
<article class="study" id="{slug}">
  <div class="study-top">
    <p class="mono">{e(v['kind'])}</p>{drawing(slug)}
  </div>
  <h3><a href="{page.project(slug)}">{e(p['name'])}</a></h3>
  <p>{e(v['summary'])}</p>{link(page.project(slug),t['more'],'right')}
</article>
''')
    physical = lookup['arduino-linux-controller']
    v = physical[page.lang]
    device = f'''
<article class="device" id="{physical['id']}">{photo(page,physical)}
  <div>
    <p class="section-label">{e(v['kind'])}</p>
    <h3>{e(physical['name'])}</h3>
    <p>{e(v['summary'])}</p>{link(page.project(physical['id']),t['more'],'right')}
  </div>
</article>
'''
    small = []
    for p in projects:
        slug = p['id']
        if slug in [lead['id'],physical['id'],*study_ids]:
            continue
        v = p[page.lang]
        small.append(f'''
<li id="{slug}"><a href="{page.project(slug)}"><span><small>{e(v['kind'])}</small><strong>{e(p['name'])}</strong></span>{icon('right')}</a>
</li>
''')
    return f'''
<section id="work" class="work band">
  <div class="frame">
    <div class="section-intro">
      <div>
        <p class="section-label">{t['projects']}</p>
        <h2>{t['workTitle']}</h2>
      </div>
      <p class="deck">{t['workIntro']}</p>
    </div>{featured}
    <div class="study-pair">{''.join(studies)}
    </div>
    <div class="instruments">{device}
      <div class="tools">
        <h3>{t['tools']}</h3>
        <ul>{''.join(small)}
        </ul>
      </div>
    </div>
  </div>
</section>
'''


def exhibit(page, slug):
    exhibits = data('exhibits')
    if slug not in exhibits:
        return ''
    exhibit = exhibits[slug][page.lang]
    rows = ''.join(f'<div><dt>{e(term)}</dt><dd>{e(note)}</dd></div>' for term, note in exhibit['rows'])
    return f'<section class="exhibit"><h2>{e(exhibit["title"])}</h2><dl>{rows}</dl><p>{e(exhibit["note"])}</p></section>'


def project_page(page, item, next_item):
    t, v = page.t, item[page.lang]
    research = [('implementation','detail'),('evidence','finding'),('limits','scope'),('credit','credit')]
    sections = ''.join(f'<section><h2>{t[label]}</h2><p>{e(v[key])}</p></section>' for label,key in research if v.get(key))
    links = ''.join(link(l['url'],l['label']) for l in v['links'])
    visual = photo(page,item) if item.get('image') else drawing(item['id'])
    tags = ' · '.join(item['tags'])
    title = item['name']
    body = f'''
<article class="project-page">
  <div class="case-cover frame"><a class="breadcrumb" href="{page.home('#work')}">← {t['contents']}</a>
    <p class="byline"><i></i>{t['case']} <span>/</span> {e(v['kind'])}</p>
    <h1>{e(title)}</h1>
    <p class="case-deck">{e(v['summary'])}</p>
    <p class="mono case-tags">{e(tags)}</p>
  </div>
  <div class="case-paper">
    <div class="frame case-reading">
      <aside>{visual}{exhibit(page,item['id'])}
        <h2>{t['docs']}</h2>
        <div class="case-sources">{link(item['repo'],t['repo'])}{links}
        </div>
      </aside>
      <div class="case-text">{sections}
      </div>
    </div>
  </div>
</article>
<div class="frame next">
  <div><span class="mono">{t['next']}</span>{link(page.project(next_item['id']), next_item['name'],'right')}
  </div>{link(page.home('#work'),t['contents'],'up')}
</div>
'''
    return page.document(title, body, v['summary'])
