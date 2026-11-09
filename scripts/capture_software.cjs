// Requires playwright-core and @sparticuz/chromium in NODE_PATH.
// Real browser screenshots, not generated illustrations. Never persist auth tokens.
const fs = require('fs');
const path = require('path');
const {chromium} = require('playwright-core');
const binary = require('@sparticuz/chromium').default;
(async()=>{
 const browser = await chromium.launch({args: binary.args, executablePath: await binary.executablePath(), headless:true});
 const page = await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});
 const token=fs.readFileSync('/tmp/atlas-jupyter-token','utf8').trim();
 await page.goto(`http://127.0.0.1:8888/lab/tree/notebooks/01_research_lab.ipynb?token=${token}`);
 await page.locator('.jp-Notebook .jp-Cell').first().waitFor({timeout:60000});
 // Discard token from address before any screenshot; screenshots capture viewport, not browser chrome.
 await page.evaluate(()=>history.replaceState(null,'',location.pathname));
 const consent=page.getByRole('button',{name:'No',exact:true});
 if(await consent.count()) await consent.click();
 const cells=page.locator('.jp-Notebook .jp-Cell');
 for(const [name,index] of [['jupyter-overview',0],['jupyter-validation',2],['jupyter-chart',4],['jupyter-sizing',6],['jupyter-news',8],['jupyter-results',10],['jupyter-journal',12]]){
  await cells.nth(index).scrollIntoViewIfNeeded();
  if(index === 0) await page.screenshot({path:`docs/images/${name}.png`});
  else await cells.nth(index+1).screenshot({path:`docs/images/${name}.png`});
 }
 await page.goto('http://127.0.0.1:3000/docs/software/backtest-report.html');
 await page.locator('.bk-root, .bk-Canvas, canvas').first().waitFor({timeout:30000}).catch(()=>{});
 await page.waitForFunction(()=>document.body.innerText.includes('SYNTHETIC'));
 await page.screenshot({path:'docs/images/backtesting-report.png',fullPage:true});
 await browser.close();
 console.log('Captured 7 JupyterLab views and 1 Backtesting.py/Bokeh report.');
})();
