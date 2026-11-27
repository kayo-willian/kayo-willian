"""The home edition in either language."""
from .common import data, e, icon, link, social
from .projects import selected_work


def opening(page):
    t = page.t
    return f'''
<section class="cover">
  <div class="frame hero">

    <div class="hero-copy">
      <p class="byline"><i></i><b>Kayo Willian</b> <span>/</span> {t['portfolio']}</p>

      <h1>GO<br>BEYOND</h1>
      <p class="kana" lang="ja">ゴー・ビヨンド</p>

      <p class="subjects">{t['subjects']}</p>
      <p class="intro">{t['intro']}</p><a class="button" href="#work">{t['explore']} {icon('down')}</a>
    </div>

    <figure class="antenna"><img src="{page.asset('art/reflector.svg')}" alt="" width="540" height="460" fetchpriority="high">
      <figcaption><span class="fig-no">Fig. A</span><span>{t['art']}</span><span class="register" aria-hidden="true">⌖</span></figcaption>
    </figure>
  </div>

  <div class="frame contacts"><span class="mono">{t['contact']}</span>
    <div>{social(t)}
    </div>
  </div>
</section>
'''


def quotation(page, index):
    q = data('quotes')[index]
    t = page.t
    cite = f'''
<figcaption>{t['by']} <span>·</span> <cite lang="en">Steel Ball Run</cite><br><small>Hirohiko Araki · <a href="https://www.shueisha.co.jp/books/items/contents.html?jdcn=08874518851126315501">{'ch.' if page.lang == 'en' else 'cap.'} 58</a> · {t['quoteNote']}</small></figcaption>
'''
    return f'''
<figure class="quote frame"><span class="quote-glyph" aria-hidden="true">“</span>
  <div><blockquote lang="en">{e(q['body'])}</blockquote>{cite}
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
<details class="lab" id="{lab['slug']}" {'open' if idx == 1 else ''}>
  <summary><span class="folio">{idx:02d}</span><span><strong>{e(lab['name'])}</strong><small>{e(v['focus'])}</small></span>{icon('plus')}</summary>
  <div class="lab-body">
    <p>{e(v['summary'])}</p>
    <p>{e(v['evidence'])}</p>{credit}
    <div class="actions">{link(v['record'],t['evidence'])}{link(v['docs'],t['labSource'])}
    </div>
  </div>
</details>
''')
    return f'''
<section class="labs-band band" id="labs">
  <div class="frame spread">
    <div class="side-heading">
      <p class="section-label">{t['labs']}</p>
      <h2>{t['labsTitle']}</h2>
      <p class="deck">{t['labsIntro']}</p>
      <div class="notebook-art" aria-hidden="true"><i></i><i></i><i></i><i></i>
      </div>
    </div>
    <div class="lab-shelf">{''.join(rows)}
    </div>
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
  <div>
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
        <p class="section-label">{t['open']}</p>
        <h2>{t['upTitle']}</h2>
      </div>
      <p class="deck">{t['upIntro']}</p>
    </div>{''.join(rows)}
  </div>
</section>
'''


def security(page):
    t = page.t
    notes = data('security')[page.lang]
    reading = ''.join(f"<article><h4>{link(r['path'], r['label'], 'right')}</h4><p>{e(r['summary'])}</p></article>" for r in notes['reading'])
    topics = ''.join(f'<div><p class="mono">{e(area)}</p><h3>{e(question)}</h3><p>{e(text)}</p></div>' for area, question, text in notes['directions'])
    return f'''
<section id="security" class="security band">
  <div class="frame">
    <div class="security-head">
      <p class="section-label">{t['securityLabel']}</p>
      <h2>{t['securityTitle']}</h2>
      <p class="deck">{t['securityIntro']}</p>
    </div>
    <div class="questions">{topics}
    </div>
    <aside class="reading-notes">
      <h3>{t['foundation']}</h3>
      <div>{reading}
      </div>
    </aside>
  </div>
</section>
'''


def home(page, projects):
    t = page.t
    body = (opening(page) + '<div class="epigraph">' + quotation(page, 0) + '</div>' +
            selected_work(page, projects) + labs(page) + upstream(page) + security(page) +
            f'<section class="closing"><div class="frame closing-contact"><h2>{t["contactTitle"]}</h2><div>{social(t)}</div></div>' + quotation(page, 1) +
            '<div class="signature frame"><span lang="ja">ゴー・ビヨンド</span><b>GO BEYOND</b></div></section>')
    return page.document('Kayo Willian', body, t['intro'])
