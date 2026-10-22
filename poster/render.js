const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const [name,wcm,hcm] of [['30x40',30,40],['50x70',50,70],['A4',21,29.7]]){
 const w=300,h=Math.round(300*hcm/wcm), scale=(wcm/2.54*300)/w;
 const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:scale});
 await p.goto('file://'+__dirname+'/poster.html');
 await p.evaluate(([w,h])=>{document.documentElement.style.setProperty('--w',w+'px');document.documentElement.style.setProperty('--h',h+'px')},[w,h]);
 await p.screenshot({path:`flight-mode_${name}.png`});await p.close();}
await b.close();})();
