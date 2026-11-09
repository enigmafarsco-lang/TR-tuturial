"""Build the canonical Markdown and its identical paginated HTML companion."""
from pathlib import Path
import html
import json
import re
import markdown
from book_content import PAGES

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT/'docs'
SOURCES = {
 'S1': ('OANDA: instrument trading hours', 'https://www.oanda.com/bvi-en/cfds/hours-of-operation/'),
 'S2': ('OANDA: platform minimum trade size', 'https://help.oanda.com/sg/en/faqs/minimum-trade-size.htm'),
 'S3': ('Freqtrade: strategy customization and lookahead', 'https://www.freqtrade.io/en/stable/strategy-customization/'),
 'S4': ('Backtesting.py: project documentation', 'https://kernc.github.io/backtesting.py/'),
 'S5': ('Binance Spot API: filters', 'https://developers.binance.com/docs/binance-spot-api-docs/filters'),
 'S6': ('CFTC: AI trading bot advisory', 'https://www.cftc.gov/PressRoom/PressReleases/8854-24'),
 'S7': ('JupyterLab: user guide and notebooks', 'https://jupyterlab.readthedocs.io/en/stable/user/notebook.html'),
 'S8': ('Telegram: Bot API', 'https://core.telegram.org/bots/api'),
}

def flow_svg(number, page):
    e=html.escape
    s='<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300"><rect width="1200" height="300" rx="18" fill="#101f30"/><style>text{font-family:DejaVu Sans,sans-serif;text-anchor:middle;fill:#e6edf4;font-size:25px}</style>'
    s+=f'<text x="600" y="42" style="font-size:17px;fill:#ebc379">ATLAS / LESSON {number:02d} / CONCEPT DIAGRAM</text>'
    for i,label in enumerate(page['labels']):
        x=820-i*380
        s+=f'<rect x="{x}" y="90" width="340" height="122" rx="14" fill="#1b344a" stroke="#41637e"/><text x="{x+170}" y="162" direction="rtl">{e(label)}</text>'
    s+='<g fill="#ebc379"><path d="M760 150l22 -13v9h18v8h-18v9z"/><path d="M380 150l22 -13v9h18v8h-18v9z"/></g>'
    s+='<text x="600" y="266" style="font-size:17px;fill:#a9bbcc" direction="rtl">شکل مفهومی آموزشی — نه نمودار بازار یا تصویر نرم‌افزار</text></svg>'
    return s

chunks=[]
manifest=[]
for i,p in enumerate(PAGES,1):
    screenshot=p['screenshot']
    image=f"images/{screenshot}.png" if screenshot else f"images/lesson-{i:02d}.png"
    if not screenshot:
        (DOCS/f'images/lesson-{i:02d}.svg').write_text(flow_svg(i,p))
    caption=(f"اسکرین‌شات واقعی {'Backtesting.py / Bokeh' if screenshot=='backtesting-report' else 'JupyterLab'}؛ داده و نتیجه ساختگی آموزشی، بدون اتصال کارگزار. "
             + {'jupyter-overview':'ستون چپ فایل‌ها؛ میانه سلول‌ها؛ پایین نام kernel.',
                'jupyter-validation':'خروجی True فقط کنترل‌های اولیه همین سلول را نشان می‌دهد.',
                'jupyter-chart':'آبی قیمت ساختگی و نارنجی میانگین؛ نمودار پایین سلول رسم شده است.',
                'jupyter-sizing':'مقادیر ورودی بالا و بودجه و حجم محاسبه‌شده در خروجی‌اند.',
                'jupyter-news':'فیلد verified برابر False و تصمیم NO_TRADE است.',
                'jupyter-results':'خلاصه نمایش داده می‌شود؛ این اعداد عملکرد بازار واقعی نیستند.',
                'jupyter-journal':'جدول خروجی شامل زمان، حجم، قیمت و سود/زیان شبیه‌سازی است.',
                'backtesting-report':'بالا منحنی سرمایه؛ پایین قیمت و مسیر معاملات؛ ابزار زوم در راست.'}[screenshot]) if screenshot else 'شکل مفهومی اختصاصی این درس؛ از راست به چپ بخوانید. این تصویر اسکرین‌شات نرم‌افزار نیست.'
    if i in {4,5,6,7,8,14,16,20,22,27,29,31,34,39,42,45}:
        caption='نمودار یا طرح توضیحی با اعداد و وضعیت‌های فرضی؛ نه داده بازار و نه اسکرین‌شات نرم‌افزار. برچسب‌های فنی داخل شکل انگلیسی‌اند.'
    text=p['text']
    for key,(_,url) in SOURCES.items(): text=text.replace(f'[{key}]',f'[{key}]({url})')
    chunk=f'<!-- PAGE {i:02d} -->\n\n<a id="lesson-{i:02d}"></a>\n\n## درس {i:02d} — {p["title"]}\n\n**هدف:** {p["goal"]}\n\n{text}\n\n![شکل {i:02d}: {p["title"]}]({image})\n\n*شکل {i:02d} — {caption}*\n\n### مراحل عملی\n\n'
    chunk+='\n'.join(f'{n}. {step}' for n,step in enumerate(p['steps'],1))+'\n\n'
    if p['code']: chunk+='```text\n'+p['code']+'\n```\n\n'
    chunk+='### تمرین و خروجی قابل بررسی\n\n'+p['exercise']+'\n\n'
    if i==52:
        chunk+='### پیوندهای مرجع\n\n'+'\n'.join(f'- [{k}: {title}]({url})' for k,(title,url) in SOURCES.items())+'\n\n'
    chunk+='---\n'
    chunks.append(chunk)
    manifest.append({'lesson':i,'title':p['title'],'path':image,'kind':'real_software_screenshot' if screenshot else 'concept_diagram','data':'synthetic / training only','caption':caption})
(DOCS/'TRADING_AI_GUIDE_FA.md').write_text('\n'.join(chunks))
(DOCS/'images/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
css='''@font-face{font-family:Book;src:url(fonts/DejaVuSans.ttf)}
*{box-sizing:border-box}html{background:#dce3ea}body{margin:0;color:#172c40;font:14px/1.95 Book,sans-serif;direction:rtl}.page{background:white;width:210mm;height:267mm;margin:24px auto;padding:11mm 15mm 12mm;position:relative;box-shadow:0 3px 15px #9daeb9}.page header{color:#52687c;font-size:10px;border-bottom:1px solid #cad5df;padding-bottom:7px}h2{font-size:22px;line-height:1.7;color:#173d56;margin:15px 0 12px}h3{font-size:14px;color:#235d75;margin:12px 0 5px}p{margin:8px 0}img{display:block;width:100%;max-height:210px;object-fit:contain;margin:12px auto 5px}img[src*="jupyter"],img[src*="backtesting"]{max-height:340px}p:has(img)+p{font-size:10px;line-height:1.7;color:#465e70}ol,ul{margin:5px 0;padding-right:24px}li{margin:3px 0}pre{direction:ltr;text-align:left;white-space:pre-wrap;font:11px/1.6 monospace;background:#edf3f7;padding:10px;border-radius:8px}a{color:#155c86;overflow-wrap:anywhere}hr{display:none}.page footer{position:absolute;bottom:5mm;left:15mm;right:15mm;border-top:1px solid #cad5df;font-size:10px;display:flex;justify-content:space-between;color:#52687c}.toolbar{max-width:794px;margin:20px auto;text-align:center}.toolbar a,.toolbar button{font:14px Book;padding:10px;background:#173d56;color:white;border:0;border-radius:8px;margin:6px;display:inline-block;text-decoration:none}.page:last-child{font-size:12px}.page:last-child h2{font-size:20px}.page:last-child img{max-height:140px}.page:last-child li{margin:1px 0}.page:last-child h3{margin:7px 0 3px}.page:last-child p{margin:5px 0}@page{size:A4;margin:15mm 0} @media print{html,body{background:white}.toolbar{display:none}.page{margin:0;box-shadow:none;break-after:page}.page:last-child{break-after:auto}a{text-decoration:none}}'''
sections=[]
for i,chunk in enumerate(chunks,1):
    sections.append(f'<section class="page" id="lesson-{i:02d}"><header>ATLAS / کتاب کار ساخت سامانه معاملاتی چندبازاری · EUR/USD PILOT</header>'+markdown.markdown(chunk,extensions=['fenced_code','tables'])+f'<footer><span>آموزشی · بدون سفارش زنده · مثال‌های ساختگی</span><span dir="ltr">{i} / 52</span></footer></section>')
(DOCS/'TRADING_AI_GUIDE_FA.html').write_text('<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>کتاب کار ۵۲ صفحه‌ای سامانه معاملاتی هوشمند</title><style>'+css+'</style></head><body><div class="toolbar"><a href="TRADING_AI_GUIDE_FA.md">متن اصلی Markdown</a><a href="TRADING_AI_GUIDE_FA.pdf">دانلود PDF</a><button onclick="print()">چاپ</button></div>'+''.join(sections)+'</body></html>')
print('Built Markdown, HTML and manifest for 52 authored lessons.')
