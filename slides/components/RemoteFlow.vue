<script setup>
// One remote on GitHub, two machines. Steps: 1 add remote + first push,
// 2 clone elsewhere, 3 push from there, 4 pull back.
defineProps({ step: { type: Number, default: 0 } })
</script>

<template>
  <svg viewBox="0 0 1050 300" class="rf">
    <defs>
      <marker id="rf-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10z" fill="var(--warn)" /></marker>
      <marker id="rf-b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10z" fill="var(--theory)" /></marker>
    </defs>
    <g transform="translate(70 0)">
    <rect x="80" y="190" width="280" height="90" class="box" /><text x="220" y="228" class="lbl">your laptop</text><text x="220" y="258" class="hint">where the project started</text>
    <g :class="['st', { on: step >= 1 }]">
      <rect x="370" y="30" width="280" height="90" class="box remote" /><text x="510" y="68" class="lbl">origin</text><text x="510" y="98" class="hint">github.com/YOU/&lt;repo&gt;</text>
      <path d="M250 190 L380 120" class="fw" /><text x="235" y="150" class="cmd" style="text-anchor:end">git remote add origin &lt;url&gt;</text><text x="235" y="172" class="cmd" style="text-anchor:end">git push -u origin main</text>
    </g>
    <g :class="['st', { on: step >= 2 }]">
      <rect x="660" y="190" width="280" height="90" class="box" /><text x="800" y="228" class="lbl">your desktop</text><text x="800" y="258" class="hint">or a cluster, or a colleague</text>
      <path d="M640 120 L770 190" class="bw" /><text x="730" y="150" class="cmd blue" style="text-anchor:start">git clone &lt;url&gt;</text>
    </g>
    <g :class="['st', { on: step >= 3 }]">
      <path d="M730 190 L610 120" class="fw" /><text x="640" y="180" class="cmd" style="text-anchor:end">git push</text>
    </g>
    <g :class="['st', { on: step >= 4 }]">
      <path d="M410 120 L290 190" class="bw" /><text x="370" y="180" class="cmd blue" style="text-anchor:start">git pull</text>
    </g>
    </g>
  </svg>
</template>

<style scoped>
.rf { width: 100%; height: auto; overflow: visible; font-family: var(--mono); }
.box { fill: #0a0a0a; stroke: var(--line); stroke-width: 2; rx: 10; }
.box.remote { stroke: var(--theory); }
.lbl { fill: var(--ink); font-size: 22px; font-weight: 700; text-anchor: middle; }
.hint { fill: var(--muted); font-size: 15px; text-anchor: middle; }
.cmd { fill: var(--warn); font-size: 18px; text-anchor: middle; }
.cmd.blue { fill: var(--theory); }
.fw { stroke: var(--warn); stroke-width: 4; fill: none; marker-end: url(#rf-a); }
.bw { stroke: var(--theory); stroke-width: 4; fill: none; marker-end: url(#rf-b); }
.st { opacity: 0; transition: opacity 0.35s; }
.st.on { opacity: 1; }
</style>
