<script setup>
// 64 commits on a line. Each step tests a commit and halves the range.
// step 0: nothing tested. steps 1..6: tests. step 7: culprit found.
// Deliberately not the same numbers as the exercise repo.
import { computed } from 'vue'
const props = defineProps({ step: { type: Number, default: 0 } })
const N = 64, CULPRIT = 41
const TESTS = [[32, 'good'], [48, 'bad'], [40, 'good'], [44, 'bad'], [42, 'bad'], [41, 'bad']]
const X = (i) => 30 + 900 * (i - 1) / (N - 1)
const state = computed(() => {
  let lo = 1, hi = N
  const tested = {}
  for (let s = 0; s < Math.min(props.step, TESTS.length); s++) {
    const [i, v] = TESTS[s]
    tested[i] = v
    if (v === 'good') lo = i; else hi = i
  }
  return { lo, hi, tested }
})
const cls = (i) => {
  const { lo, hi, tested } = state.value
  if (i === 1) return 'good'
  if (i === N) return 'bad'
  if (tested[i]) return tested[i]
  if (i < lo || i > hi) return 'dim'
  return ''
}
</script>

<template>
  <svg viewBox="0 0 960 190" class="bs">
    <line x1="30" y1="70" x2="930" y2="70" class="edge" />
    <circle v-for="i in N" :key="i" :cx="X(i)" cy="70" r="6" :class="['node', cls(i)]" />
    <text :x="X(1)" y="115" class="tag good">v0.1 good</text>
    <text :x="X(N)" y="115" class="tag bad">HEAD bad</text>
    <g :class="['st', { on: step >= 7 }]">
      <line :x1="X(CULPRIT)" y1="85" :x2="X(CULPRIT)" y2="150" class="pin" />
      <text :x="X(CULPRIT)" y="175" class="found">{{ CULPRIT }} is the first bad commit</text>
    </g>
    <text x="480" y="150" :class="['hint', { gone: step >= 7 }]">
      {{ step === 0 ? '64 commits. Where did it break?' : `${state.hi - state.lo - 1} ${state.hi - state.lo - 1 === 1 ? 'commit' : 'commits'} left to check` }}
    </text>
    <text x="480" y="20" class="log"><tspan v-for="([i, v], s) in TESTS" :key="s" :class="[v, { hidden: step < s + 1 }]">{{ s + 1 }}: {{ i }} {{ v }}&#160;&#160;&#160;</tspan></text>
  </svg>
</template>

<style scoped>
.bs { width: 100%; height: auto; overflow: visible; font-family: var(--mono); }
.edge { stroke: #444; stroke-width: 3; }
.node { fill: #777; stroke: #000; stroke-width: 2; transition: fill 0.3s; }
.node.good { fill: var(--accent); }
.node.bad { fill: var(--bad); }
.node.dim { fill: #222; }
.tag { font-size: 15px; text-anchor: middle; font-weight: 700; }
.tag.good { fill: var(--accent); }
.tag.bad { fill: var(--bad); }
.pin { stroke: var(--bad); stroke-width: 3; }
.found { fill: var(--bad); font-size: 20px; font-weight: 700; text-anchor: middle; }
.log { font-size: 15px; text-anchor: middle; }
.log .good { fill: var(--accent); }
.log .bad { fill: var(--bad); }
.log .hidden { fill: transparent; }
.hint { fill: var(--muted); font-size: 17px; text-anchor: middle; transition: opacity 0.3s; }
.hint.gone { opacity: 0; }
.st { opacity: 0; transition: opacity 0.35s; }
.st.on { opacity: 1; }
</style>
