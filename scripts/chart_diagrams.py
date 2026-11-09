"""Distinct illustrative charts. All numbers are teaching assumptions, not market data."""
from pathlib import Path
from html import escape
OUT=Path(__file__).resolve().parents[1]/'docs/images'

def text(x,y,t,color='#dce8f0',size=21):
    return f'<text x="{x}" y="{y}" text-anchor="middle" fill="{color}" font-size="{size}" font-family="DejaVu Sans,sans-serif">{escape(str(t))}</text>'
def rect(x,y,w,h,c='#24445c'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{c}"/>'
def line(x,y,x2,y2,c='#89aac2',dash=''):
    return f'<path d="M{x} {y}L{x2} {y2}" stroke="{c}" stroke-width="3" stroke-dasharray="{dash}"/>'
def save(n,title,body):
    s=f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="360" viewBox="0 0 1200 360">{rect(0,0,1200,360,"#101f30")}{text(600,36,title,"#ebc379",22)}{body}{text(600,338,"ILLUSTRATION ONLY / SYNTHETIC VALUES / NOT A TRADING SIGNAL", "#9db2c2",15)}</svg>'
    (OUT/f'lesson-{n:02d}.svg').write_text(s)

s=line(140,255,1050,255)
for x,p in [(220,'1.1000'),(550,'1.1001'),(880,'1.1002')]:
    s+=line(x,240,x,270)+text(x,295,p)
s+=text(385,135,'1 pip = 0.0001')+text(600,190,'1,000 EUR units × 0.0001 = USD 0.10')
s+=line(220,210,550,210,'#73d6b8')
save(4,'PIP VALUE / USD ACCOUNT EXAMPLE',s)

s=''
for x,h,v,label,c in [(180,140,'+0.50','Gross PnL','#73d6b8'),(490,182,'-0.65','Total costs','#ef9292'),(800,42,'-0.15','Net PnL','#ebc379')]:
    s+=rect(x,255-h,220,h,c)+text(x+110,100,v)+text(x+110,292,label)
save(5,'SMALL PROFIT TARGETS CAN BE CONSUMED BY COSTS',s)

s=''
for x,h,label,val in [(150,25,'1× exposure','-10'),(480,75,'5× exposure','-50'),(810,210,'20× exposure','-200')]:
    s+=rect(x,275-h,220,h,'#ef9292')+text(x+110,98,label)+text(x+110,300,val+' USD')
s+=text(600,62,'USD 1,000 equity / adverse price move 1%',size=17)
save(6,'LEVERAGE / SAME PRICE MOVE, DIFFERENT ACCOUNT LOSS',s)

s=''
for i,day in enumerate(['MON','TUE','WED','THU','FRI','SAT','SUN']):
    x=70+i*155;s+=rect(x,115,135,90,'#285846' if i<5 else '#664754')+text(x+67,165,day)
s+=text(600,245,'Illustrative week only — use the actual instrument calendar')+text(600,282,'Analysis can continue when order entry is closed', '#ebc379')
save(7,'PROCESSING AVAILABILITY IS NOT MARKET AVAILABILITY',s)

s=rect(150,120,300,120)+text(300,165,'Raw allowed size: 8')+text(300,207,'Instrument minimum: 10')+line(470,180,680,180)+rect(710,120,320,120,'#673f4b')+text(870,190,'REJECT — do not round up')
save(8,'MINIMUM SIZE MUST NOT OVERRIDE THE RISK BUDGET',s)

s=line(100,220,1100,220)
for i,(lab,c) in enumerate([('Closed t-2','#73d6b8'),('Closed t-1','#73d6b8'),('Closed t','#73d6b8'),('Next execution','#ebc379'),('Future','#ef9292')]):
    x=175+i*210;s+=rect(x-75,115,150,70,c)+text(x,159,lab,'#101f30',17)+line(x,185,x,235)
s+=text(600,290,'Features use only data available at the decision time')
save(14,'NO FUTURE INFORMATION IN A PAST DECISION',s)

s=''
for i,(label,time) in enumerate([('Published','10:00:00'),('Received','10:00:08'),('Processing done','10:00:12')]):
    x=80+i*390;s+=rect(x,100,300,140)+text(x+150,145,label)+text(x+150,200,time,'#ebc379',28)
s+=text(600,285,'A decision cannot occur before receipt and processing')
save(16,'NEWS TIMESTAMPS / AN 8-SECOND DELAY IS NOT ZERO',s)

s=rect(70,130,260,100)+text(200,185,'Primary source')
for y,label in [(75,'Channel A'),(165,'Channel B'),(255,'Channel C')]:
    s+=line(345,180,620,y+12)+rect(650,y-22,260,65)+text(780,y+18,label)
s+=text(1050,185,'1 source', '#ebc379',26)
save(20,'THREE REPOSTS ARE NOT THREE INDEPENDENT CONFIRMATIONS',s)

s=rect(60,120,300,120,'#673f4b')+text(210,169,'Untrusted message')+text(210,205,'"Ignore risk limits"',size=18)
s+=rect(450,95,280,165)+text(590,155,'Schema + policy')+text(590,205,'No tool permissions',size=18)
s+=line(375,180,430,180)+line(750,180,810,180)+rect(830,120,300,120,'#285846')+text(980,188,'NO_TRADE / LOG')
save(22,'PROMPT INJECTION MUST NOT BECOME AN ORDER',s)

s=''
prices=[235,215,225,200,210,180,195,170,155,160,140,110]
for i,p in enumerate(prices):
    x=110+i*75;prev=prices[i-1] if i else 250;c='#73d6b8' if p<prev else '#ef9292'
    s+=line(x,min(prev,p)-10,x,max(prev,p)+15,c)+rect(x-11,min(prev,p),22,max(5,abs(p-prev)),c)
s+=line(75,145,1090,145,'#ebc379','8 6')+text(880,80,'Previous 10-bar high', '#ebc379',18)+text(600,300,'Illustrative breakout — not actual EUR/USD data')
save(27,'TURN A VISUAL IDEA INTO A PRECISE RULE',s)

s=''
for y,label,c in [(100,'Target: 1.1040','#ebc379'),(175,'Entry: 1.1000','#73d6b8'),(245,'Stop: 1.0980','#ef9292')]:
    s+=line(100,y,850,y,c,'8 5')+text(1010,y+5,label,c,18)
s+=text(500,290,'Time exit is a separate rule, not shown by a price line')
save(29,'PRICE EXIT AND TIME EXIT ARE DIFFERENT CONDITIONS',s)

s=''
for x,lab in [(70,'Robot A'),(450,'Robot B'),(830,'Robot C')]:
    s+=rect(x,80,300,65)+text(x+150,122,lab)+line(x+150,150,600,210)
s+=rect(340,215,520,75,'#285846')+text(600,262,'ONE SHARED PORTFOLIO RISK LIMIT')
save(31,'SEVERAL ROBOTS DO NOT CREATE SEVERAL INDEPENDENT BUDGETS',s)

s=''
for x,lab,c in [(60,'SENT','#24445c'),(450,'UNKNOWN','#673f4b'),(840,'RECONCILE','#285846')]:
    s+=rect(x,110,300,105,c)+text(x+150,173,lab)
s+=line(375,165,430,165)+line(765,165,820,165)+text(600,285,'Timeout is not proof of rejection — query before retry')
save(34,'ORDER STATE / PREVENT DUPLICATE SUBMISSION',s)

s=''
for x,lab,c in [(80,'Pause new entries','#24445c'),(460,'Manage pending','#5b4e35'),(840,'Emergency exit','#673f4b')]:
    s+=rect(x,100,280,130,c)+text(x+140,173,lab,size=18)
s+=text(600,290,'Stopping a process does not automatically close a position')
save(39,'THE KILL SWITCH HAS DISTINCT, TESTABLE ACTIONS',s)

s=''
for row in range(3):
    for col in range(6):
        x=160+col*150;y=75+row*66
        color='#285846' if col<row+2 else '#916f3e' if col==row+2 else '#263747'
        s+=rect(x,y,135,48,color)
    s+=text(90,106+row*66,'Fold '+str(row+1),size=16)
s+=text(600,300,'Green: past training | Gold: next test | Grey: not yet seen',size=18)
save(42,'WALK-FORWARD / TRAIN ONLY ON THE PAST',s)

s=''
for row in range(3):
    for col in range(3):
        x=330+col*180;y=65+row*70
        vals=[[.4,.1,-.2],[.2,-.1,-.4],[-.1,-.3,-.7]];v=vals[row][col]
        s+=rect(x,y,160,55,'#285846' if v>0 else '#673f4b')+text(x+80,y+36,f'{v:+.1f} R')
s+=text(600,310,'Synthetic sensitivity grid: higher cost → | higher delay ↓',size=18)
save(45,'STRESS TEST / DO NOT SELECT ONLY THE BEST CELL',s)
print('Created 16 distinct chart and process illustrations.')
