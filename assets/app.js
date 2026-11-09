'use strict';
function calculatePosition(equity, riskPct, entry, stop, cost, minUnits) {
  const values = [equity, riskPct, entry, stop, cost, minUnits];
  if (values.some(x => !Number.isFinite(x)) || equity <= 0 || riskPct <= 0 || riskPct > 100 || entry <= 0 || stop <= 0 || stop >= entry || cost < 0 || minUnits < 1 || !Number.isInteger(minUnits)) return {error: 'اعداد معتبر وارد کن؛ توقف خرید باید کمتر از ورود باشد و حداقل واحد عدد صحیح مثبت باشد.'};
  const budget = equity * riskPct / 100;
  const units = Math.floor(Math.min(budget / (entry - stop + cost), equity / (entry + cost)));
  if (units < minUnits) return {error: 'رد معامله: حجم مجاز کمتر از حداقل ابزار است.'};
  return {budget, units, notional: units * entry, plannedLoss: units * (entry - stop + cost)};
}
if (typeof module !== 'undefined') module.exports = {calculatePosition};
if (typeof document !== 'undefined') {
  function update() {
    const ids = ['equity', 'riskPct', 'entry', 'stop', 'cost', 'minUnits'];
    const values = ids.map(id => document.getElementById(id).value.trim());
    const r = calculatePosition(...values.map(v => v === '' ? NaN : Number(v)));
    document.getElementById('result').textContent = r.error || `بودجه زیان: ${r.budget.toFixed(2)} دلار | حجم: ${r.units} واحد | مواجهه: ${r.notional.toFixed(2)} دلار | زیان تخمینی: ${r.plannedLoss.toFixed(4)} دلار`;
  }
  document.querySelectorAll('input').forEach(el => el.addEventListener('input', update));
  update();
}
