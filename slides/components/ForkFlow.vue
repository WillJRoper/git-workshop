<script setup>
// upstream -> fork -> clone -> push -> pull request.
defineProps({ step: { type: Number, default: 0 } })
</script>

<template>
  <svg viewBox="0 0 960 300" class="ff">
    <defs>
      <marker id="ff-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10z" fill="var(--warn)" /></marker>
      <marker id="ff-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10z" fill="var(--accent)" /></marker>
    </defs>
    <rect x="40" y="30" width="280" height="90" class="box remote" /><text x="180" y="68" class="lbl">upstream</text><text x="180" y="98" class="hint">github.com/WillJRoper/&lt;repo&gt;</text>
    <g :class="['st', { on: step >= 1 }]">
      <rect x="640" y="30" width="280" height="90" class="box remote" /><text x="780" y="68" class="lbl">your fork</text><text x="780" y="98" class="hint">github.com/YOU/&lt;repo&gt;</text>
      <path d="M320 65 L640 65" class="fw" /><text x="480" y="52" class="cmd">Fork (button on GitHub)</text>
    </g>
    <g :class="['st', { on: step >= 2 }]">
      <rect x="640" y="190" width="280" height="90" class="box" /><text x="780" y="228" class="lbl">your laptop</text><text x="780" y="258" class="hint">local clone</text>
      <path d="M810 120 L810 190" class="fw" /><text x="880" y="160" class="cmd">git clone</text>
    </g>
    <g :class="['st', { on: step >= 3 }]">
      <path d="M750 190 L750 120" class="fw" /><text x="690" y="160" class="cmd">git push</text>
    </g>
    <g :class="['st', { on: step >= 4 }]">
      <path d="M640 100 L320 100" class="gw" /><text x="480" y="142" class="cmd green">Pull Request: "please merge my branch"</text>
      <text x="310" y="222" class="note">A PR is a <tspan fill="var(--warn)">conversation</tspan> around a branch:</text>
      <text x="310" y="252" class="note grey">diff, review, automated tests, then merge.</text>
    </g>
  </svg>
</template>

<style scoped>
.ff { width: 100%; height: auto; overflow: visible; font-family: var(--mono); }
.box { fill: #0a0a0a; stroke: var(--line); stroke-width: 2; rx: 10; }
.box.remote { stroke: var(--theory); }
.lbl { fill: var(--ink); font-size: 22px; font-weight: 700; text-anchor: middle; }
.hint { fill: var(--muted); font-size: 15px; text-anchor: middle; }
.cmd { fill: var(--warn); font-size: 18px; text-anchor: middle; }
.cmd.green { fill: var(--accent); }
.note { fill: var(--ink); font-size: 19px; text-anchor: middle; }
.note.grey { fill: var(--muted); }
.fw { stroke: var(--warn); stroke-width: 4; fill: none; marker-end: url(#ff-a); }
.gw { stroke: var(--accent); stroke-width: 4; fill: none; marker-end: url(#ff-g); }
.st { opacity: 0; transition: opacity 0.35s; }
.st.on { opacity: 1; }
</style>
