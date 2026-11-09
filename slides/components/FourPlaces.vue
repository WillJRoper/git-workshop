<script setup>
// Working tree -> staging -> local repo -> remote, arrows revealed by step.
// 1 add, 2 commit, 3 push, 4 fetch, 5 pull, 6 clone, 7 status/diff.
defineProps({ step: { type: Number, default: 0 } })
const BOXES = [
  ['Working tree', 'files you edit', 10],
  ['Staging area', 'the index', 275],
  ['Local repo', '.git/ history', 540],
  ['Remote', 'GitHub', 805],
]
</script>

<template>
  <svg viewBox="0 0 960 340" class="fp">
    <defs>
      <marker id="fp-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10z" fill="var(--warn)" /></marker>
      <marker id="fp-b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10z" fill="var(--theory)" /></marker>
    </defs>
    <text x="355" y="22" class="hint">your machine</text>
    <line x1="10" y1="32" x2="700" y2="32" class="rule" />
    <text x="877" y="22" class="hint blue">the internet</text>
    <line x1="805" y1="32" x2="950" y2="32" class="rule blue" />
    <g v-for="([t, s, x], i) in BOXES" :key="t">
      <rect :x="x" y="70" :width="i === 3 ? 145 : 160" height="110" :class="['box', { remote: i === 3 }]" />
      <text :x="x + (i === 3 ? 72 : 80)" y="117" class="lbl">{{ t }}</text>
      <text :x="x + (i === 3 ? 72 : 80)" y="147" class="hint">{{ s }}</text>
    </g>
    <!-- forward: add, commit, push (upper lane, labels above) -->
    <g :class="['st', { on: step >= 1 }]"><path d="M172 100 L273 100" class="fw" /><text x="222" y="88" class="cmd">git add</text></g>
    <g :class="['st', { on: step >= 2 }]"><path d="M437 100 L538 100" class="fw" /><text x="487" y="88" class="cmd">git commit</text></g>
    <g :class="['st', { on: step >= 3 }]"><path d="M702 100 L803 100" class="fw" /><text x="752" y="88" class="cmd">git push</text></g>
    <!-- fetch: lower lane in the same gap, label below -->
    <g :class="['st', { on: step >= 4 }]"><path d="M803 150 L702 150" class="bw" /><text x="752" y="176" class="cmd blue">git fetch</text></g>
    <!-- pull: routed under the boxes -->
    <g :class="['st', { on: step >= 5 }]">
      <path d="M850 180 V232 H110 V186" class="bw" />
      <text x="470" y="258" class="cmd blue">git pull  =  fetch, then merge into your files</text>
    </g>
    <!-- clone: routed lower still -->
    <g :class="['st', { on: step >= 6 }]">
      <path d="M920 180 V292 H50 V186" class="bw" />
      <text x="480" y="318" class="cmd blue">git clone  =  first time only, copies the whole history</text>
    </g>
    <g :class="['st', { on: step >= 7 }]"><text x="90" y="58" class="cmd grey">git status / git diff</text></g>
  </svg>
</template>

<style scoped>
.fp { width: 100%; height: auto; overflow: visible; font-family: var(--mono); }
.box { fill: #0a0a0a; stroke: var(--line); stroke-width: 2; rx: 10; }
.box.remote { stroke: var(--theory); }
.lbl { fill: var(--ink); font-size: 20px; font-weight: 700; text-anchor: middle; }
.hint { fill: var(--muted); font-size: 15px; text-anchor: middle; }
.hint.blue { fill: var(--theory); }
.rule { stroke: var(--line); stroke-width: 1; }
.rule.blue { stroke: var(--theory); opacity: 0.5; }
.cmd { fill: var(--warn); font-size: 16px; text-anchor: middle; }
.cmd.blue { fill: var(--theory); }
.cmd.grey { fill: var(--muted); }
.fw { stroke: var(--warn); stroke-width: 4; fill: none; marker-end: url(#fp-a); }
.bw { stroke: var(--theory); stroke-width: 4; fill: none; marker-end: url(#fp-b); stroke-linejoin: round; }
.st { opacity: 0; transition: opacity 0.35s; }
.st.on { opacity: 1; }
</style>
