<script setup>
// main A-B-C, feature branch D-E, collaborator's F on main, then merge M.
// step: 0 base, 1 branch + D, 2 E, 3 F lands on main, 4 merge commit.
defineProps({ step: { type: Number, default: 0 } })
</script>

<template>
  <svg viewBox="0 0 1000 250" class="bg">
    <line x1="60" y1="80" x2="260" y2="80" class="edge" />
    <circle cx="60" cy="80" r="17" class="node" /><circle cx="160" cy="80" r="17" class="node" /><circle cx="260" cy="80" r="17" class="node" />
    <text x="60" y="122" class="lbl">A</text><text x="160" y="122" class="lbl">B</text><text x="260" y="122" class="lbl">C</text>
    <text x="260" y="45" :class="['ref', 'main', { off: step >= 3 }]">main</text>
    <g :class="['st', { on: step >= 1 }]">
      <text x="600" y="222" :class="['cmd', 'fade', { off: step >= 4 }]">git switch -c new-feature</text>
      <path d="M260 80 C 310 80, 310 180, 360 180" class="edge" /><circle cx="360" cy="180" r="17" class="node feat" /><text x="360" y="222" :class="['ref', 'feat', { off: step >= 2 }]">new-feature</text>
    </g>
    <g :class="['st', { on: step >= 2 }]">
      <line x1="360" y1="180" x2="460" y2="180" class="edge" /><circle cx="460" cy="180" r="17" class="node feat" /><text x="460" y="222" class="ref feat">new-feature</text>
    </g>
    <g :class="['st', { on: step >= 3 }]">
      <line x1="260" y1="80" x2="360" y2="80" class="edge" /><circle cx="360" cy="80" r="17" class="node" /><text x="360" y="45" :class="['ref', 'main', { off: step >= 4 }]">main</text>
      <g :class="{ off: step >= 4 }" class="fade"><text x="560" y="72" class="note">meanwhile a collaborator</text><text x="560" y="96" class="note">pushed F to main</text></g>
    </g>
    <g :class="['st', { on: step >= 4 }]">
      <path d="M360 80 L560 80" class="edge" /><path d="M460 180 C 510 180, 510 80, 560 80" class="edge" />
      <circle cx="560" cy="80" r="17" class="node merge" /><text x="560" y="45" class="ref main">main</text><text x="560" y="122" class="lbl">M</text>
      <text x="620" y="72" class="note">M: a merge commit, two parents</text><text x="620" y="96" class="cmd">git switch main; git merge new-feature</text>
    </g>
  </svg>
</template>

<style scoped>
.bg { width: 100%; height: auto; overflow: visible; font-family: var(--mono); }
.edge { stroke: #555; stroke-width: 4; fill: none; }
.node { fill: var(--accent); stroke: #000; stroke-width: 3; }
.node.feat { fill: var(--warn); }
.node.merge { fill: var(--merge); }
.lbl { fill: var(--ink); font-size: 20px; text-anchor: middle; }
.ref { font-size: 17px; text-anchor: middle; font-weight: 700; transition: opacity 0.3s; }
.ref.main { fill: var(--accent); }
.ref.feat { fill: var(--warn); }
.ref.off { opacity: 0; }
.cmd { fill: var(--warn); font-size: 17px; }
.note { fill: var(--muted); font-size: 18px; }
.st { opacity: 0; transition: opacity 0.35s; }
.st.on { opacity: 1; }
.fade { transition: opacity 0.3s; }
.fade.off { opacity: 0; }
</style>
