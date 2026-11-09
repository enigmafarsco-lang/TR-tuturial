// Rasterize authored diagrams; validate layout; export the actual 52-page PDF.
const {chromium}=require('playwright-core');
const binary=require('@sparticuz/chromium').default;
const fs=require('fs');
(async()=>{
 const browser=await chromium.launch({args:binary.args,executablePath:await binary.executablePath(),headless:true});
 const page=await browser.newPage({viewport:{width:1200,height:300},deviceScaleFactor:1});
 const manifest=JSON.parse(fs.readFileSync('docs/images/manifest.json','utf8'));
 for(const item of manifest.filter(i=>i.kind==='concept_diagram')){
  await page.goto('http://127.0.0.1:3000/docs/'+item.path.replace('.png','.svg'));
  await page.evaluate(()=>document.fonts.ready);
  const height=await page.evaluate(()=>Number(document.documentElement.getAttribute('height'))||300);
  await page.setViewportSize({width:1200,height});
  await page.screenshot({path:'docs/'+item.path});
 }
 await page.setViewportSize({width:1100,height:1200});
 await page.goto('http://127.0.0.1:3000/docs/TRADING_AI_GUIDE_FA.html');
 await page.evaluate(()=>document.fonts.ready);
 await page.waitForFunction(()=>Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0));
 const layout=await page.locator('.page').evaluateAll(pages=>pages.map((p,i)=>({page:i+1,height:p.clientHeight,scroll:p.scrollHeight, footerTop:p.querySelector('footer').getBoundingClientRect().top,contentBottom:p.querySelector('footer').previousElementSibling.getBoundingClientRect().bottom})))
 fs.writeFileSync('docs/layout-check.json',JSON.stringify(layout,null,2));
 const overflow=layout.filter(x=>x.scroll>x.height+1||x.contentBottom>x.footerTop-4);
 if(overflow.length) throw Error('Overflow: '+JSON.stringify(overflow));
 await page.locator('.page').nth(9).screenshot({path:'docs/images/book-page-preview.png'});
 await page.pdf({path:'docs/TRADING_AI_GUIDE_FA.pdf',printBackground:true,preferCSSPageSize:true});
 await browser.close();
 console.log('52 page layouts checked; PDF exported.');
})().catch(e=>{console.error(e);process.exit(1)});
