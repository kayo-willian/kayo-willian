"""The home edition in either language."""
from .common import data, e, icon, link, social
from .projects import selected_work


def opening(page):
    t = page.t
    return f'''
<section class="cover">
  <div class="frame hero">
    <div class="hero-copy">
      <h1>Kayo Willian</h1>
      <p class="subjects">{t['subjects']}</p>
      <p class="intro">{t['intro']}</p>
      <div class="hero-links">{social(t)}</div>
      <a class="button" href="#work">{t['explore']} {icon('down')}</a>
    </div>
    <div class="hero-brand spiral-brand"><img class="golden-spiral" width="640" height="400" src="{page.asset('art/golden-spiral.svg')}" alt="{e(t['spiralAlt'])}"></div>
  </div>
</section>
'''


def quotation(page, index):
    q = data('quotes')[index]
    t = page.t
    cite = f'''
<figcaption>{e(q['byPt'] if page.lang == 'pt' else q['by'])} <span>·</span> <cite lang="en">Steel Ball Run</cite><br><small>Hirohiko Araki · <a href="{e(q['source'])}">{'ch.' if page.lang == 'en' else 'cap.'} {q['chapter']}</a> · {t['quoteNote']}</small></figcaption>
'''
    return f'''
<figure class="quote frame"><span class="quote-glyph" aria-hidden="true">“</span>
  <div><blockquote lang="{'pt-BR' if page.lang == 'pt' else 'en'}">{e(q['pt'] if page.lang == 'pt' else q['body'])}</blockquote>{cite}
  </div>
</figure>
'''


def labs(page):
    t = page.t
    rows = []
    for idx, lab in enumerate(data('labs'), 1):
        v = lab[page.lang]
        credit = f'<p class="fine">{e(v["credit"])}</p>' if v['credit'] else ''
        rows.append(f'''
<article class="lab" id="{lab['slug']}">
  <div class="lab-head"><span class="folio">{idx:02d}</span><div><h3>{e(lab['name'])}</h3><small>{e(v['focus'])}</small></div></div>
  <div class="lab-body"><p>{e(v['summary'])}</p><p>{e(v['evidence'])}</p>{credit}
    <div class="actions">{link(v['record'],t['evidence'])}{link(v['docs'],t['labSource'])}</div>
  </div>
</article>
''')
    return f'''
<section class="labs-band band" id="labs">
  <div class="frame">
    <div class="section-intro"><div><p class="section-label">02 / {t['labs']}</p><h2>{t['labsTitle']}</h2></div><p class="deck">{t['labsIntro']}</p></div>
    <div class="lab-grid">{''.join(rows)}</div>
    <p class="continuity">{t['labContinuation']}</p>
  </div>
</section>
'''


def upstream(page):
    t = page.t
    en = page.lang == 'en'
    rows = []
    for project in data('contributions'):
        entries = []
        for item in project['items']:
            v = item[page.lang]
            kind = 'PR' if item['type'] == 'pr' else ('Issue' if en else 'Relato')
            state = item['state'] if en else {'open':'em aberto','merged':'integrado','closed':'encerrado'}[item['state']]
            entries.append(f'''
<li>
  <div class="record-meta"><span>{kind} #{item['number']}</span><span class="status {item['state']}">{state}</span>
  </div>
  <h4>{link(item['url'],v['title'])}</h4>
  <p>{e(v['summary'])}</p>
</li>
''')
        rows.append(f'''
<article class="up-project">
  <div class="up-summary">
    <p class="up-owner">{e(project['owner'])} /</p>
    <h3>{e(project['project'])}</h3>
    <p>{e(project[page.lang]['forkNote'])}</p>
    <div class="actions">{link(project['upstream'], 'Upstream' if en else 'Projeto original')}{link(project['fork'], 'My fork' if en else 'Meu fork')}
    </div>
  </div>
  <ul class="records">{''.join(entries)}
  </ul>
</article>
''')
    return f'''
<section id="oss" class="band open-band">
  <div class="frame">
    <div class="section-intro">
      <div>
        <p class="section-label">03 / {t['open']}</p>
        <h2>{t['upTitle']}</h2>
      </div>
      <p class="deck">{t['upIntro']}</p>
    </div>{''.join(rows)}
    <p class="continuity">{t['ossContinuation']}</p>
  </div>
</section>
'''


def security(page):
    t = page.t
    notes = data('security')[page.lang]
    topics = ''.join(f'<article><h3>{e(area)}</h3><p>{e(text)}</p></article>' for area, text in notes['areas'])
    reading = ''.join(f'<li>{link(r["path"],r["label"],"right")}</li>' for r in notes['reading'])
    return f'''
<section id="security" class="security band">
  <div class="frame">
    <div class="security-head"><p class="section-label">04 / {t['securityLabel']}</p><h2>{t['securityTitle']}</h2><p class="deck">{t['securityIntro']}</p></div>
    <div class="security-map">{topics}</div>
    <div class="security-records"><div><h3>{t['securityRecordTitle']}</h3><p>{t['securityRecordNote']}</p></div><div><h3>{t['securityFoundation']}</h3><ul>{reading}</ul></div></div>
  </div>
</section>
'''


def home(page, projects):
    t = page.t
    body = (opening(page) + '<div class="epigraph">' + quotation(page, 0) + '</div>' +
            selected_work(page, projects) + labs(page) + upstream(page) + security(page) +
            f'<section class="closing"><div class="frame closing-contact"><h2>{t["contactTitle"]}</h2><div>{social(t)}</div></div>' + quotation(page, 1) +
            '</section>')
    return page.document('Kayo Willian', body, t['intro'])
