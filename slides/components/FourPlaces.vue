<script setup>
// Working tree -> staging -> local repo -> remote, arrows revealed by step.
defineProps({ step: { type: Number, default: 0 } })
const BOXES = [
  ['Working tree', 'files you edit', 10],
  ['Staging area', 'the index', 260],
  ['Local repo', '.git/ history', 510],
  ['Remote', 'GitHub', 760],
]
</script>

<template>
  <svg viewBox="0 0 960 330" class="fp">
    <defs>
      <marker id="fp-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10z" fill="var(--warn)" /></marker>
      <marker id="fp-b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10z" fill="var(--theory)" /></marker>
    </defs>
    <text x="360" y="30" text-anchor="middle" class="hint">your machine</text>
    <text x="855" y="30" text-anchor="middle" class="hint">the internet</text>
    <line x1="735" y1="15" x2="735" y2="225" class="dash" />
    <g v-for="([t, s, x], i) in BOXES" :key="t">
      <rect :x="x" y="60" :width="i === 3 ? 190 : 200" height="120" :class="['box', { remote: i === 3 }]" />
      <text :x="x + (i === 3 ? 95 : 100)" y="112" text-anchor="middle" class="lbl">{{ t }}</text>
      <text :x="x + (i === 3 ? 95 : 100)" y="142" text-anchor="middle" class="hint">{{ s }}</text>
    </g>
    <g :class="['st', { on: step >= 1 }]"><path d="M210 95 L260 95" class="fw" /><text x="235" y="82" text-anchor="middle" class="cmd">git add</text></g>
    <g :class="['st', { on: step >= 2 }]"><path d="M460 95 L510 95" class="fw" /><text x="485" y="82" text-anchor="middle" class="cmd">git commit</text></g>
    <g :class="['st', { on: step >= 3 }]"><path d="M710 95 L760 95" class="fw" /><text x="735" y="82" text-anchor="middle" class="cmd">git push</text></g>
    <g :class="['st', { on: step >= 4 }]"><path d="M760 150 L710 150" class="bw" /><text x="735" y="175" text-anchor="middle" class="cmd blue">git fetch</text></g>
    <g :class="['st', { on: step >= 5 }]"><path d="M760 200 C 500 262, 300 262, 60 185" class="bw" /><text x="420" y="272" text-anchor="middle" class="cmd blue">git pull = fetch + merge into your files</text></g>
    <g :class="['st', { on: step >= 6 }]"><path d="M855 190 C 855 325, 110 325, 110 190" class="bw" /><text x="480" y="322" text-anchor="middle" class="cmd blue">git clone: first time, copies everything</text></g>
    <g :class="['st', { on: step >= 7 }]"><text x="110" y="48" text-anchor="middle" class="cmd grey">git status / git diff</text></g>
  </svg>
</template>

<style scoped>
.fp { width: 100%; height: auto; overflow: visible; font-family: var(--mono); }
.box { fill: #0a0a0a; stroke: var(--line); stroke-width: 2; rx: 10; }
.box.remote { stroke: var(--theory); }
.lbl { fill: var(--ink); font-size: 22px; font-weight: 700; }
.hint { fill: var(--muted); font-size: 15px; }
.dash { stroke: var(--line); stroke-width: 2; stroke-dasharray: 8 8; }
.cmd { fill: var(--warn); font-size: 18px; }
.cmd.blue { fill: var(--theory); }
.cmd.grey { fill: var(--muted); }
.fw { stroke: var(--warn); stroke-width: 4; fill: none; marker-end: url(#fp-a); }
.bw { stroke: var(--theory); stroke-width: 4; fill: none; marker-end: url(#fp-b); }
.st { opacity: 0; transition: opacity 0.35s; }
.st.on { opacity: 1; }
</style>
