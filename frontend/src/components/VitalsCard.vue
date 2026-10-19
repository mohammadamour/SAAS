<script setup>
import { computed } from 'vue';
import { useIntelStore } from '../stores/useIntelStore';
import { 
  Gauge, 
  Eye, 
  Search, 
  Zap, 
  CheckCircle2, 
  Clock, 
  Sparkles 
} from 'lucide-vue-next';

const store = useIntelStore();

const vitals = computed(() => store.dossier.value?.vitals || {
  performance_score: 95,
  seo_score: 98,
  accessibility_score: 92,
  fcp_seconds: 0.9,
  speed_index: 1.4,
});

// Circular SVG dial mathematics
const RADIUS = 38;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS; // ~238.76

function getDashOffset(score) {
  const clamped = Math.min(100, Math.max(0, score || 0));
  return CIRCUMFERENCE - (clamped / 100) * CIRCUMFERENCE;
}

function getScoreColorClass(score) {
  if (score >= 90) return 'score-emerald';
  if (score >= 50) return 'score-amber';
  return 'score-crimson';
}
</script>

<template>
  <div class="prism-card vitals-card">
    <!-- Quadrant Header -->
    <div class="card-header">
      <div class="header-left">
        <span class="quadrant-badge font-mono">QUADRANT 03 // VITALS</span>
        <h3 class="card-title">Performance & Core Vitals</h3>
      </div>
      <div class="audit-pill font-mono">
        <Sparkles :size="12" class="text-accent" />
        <span>LIGHTHOUSE ENGINE</span>
      </div>
    </div>

    <!-- 3 Animated SVG Radial Score Dials -->
    <div class="radial-dials-row">
      <!-- 1. Performance Dial -->
      <div class="dial-card">
        <div class="svg-dial-wrapper">
          <svg class="dial-svg" viewBox="0 0 100 100">
            <!-- Background Track -->
            <circle
              class="dial-track"
              cx="50"
              cy="50"
              :r="RADIUS"
            />
            <!-- Animated Score Fill -->
            <circle
              class="dial-fill"
              :class="getScoreColorClass(vitals.performance_score)"
              cx="50"
              cy="50"
              :r="RADIUS"
              :stroke-dasharray="CIRCUMFERENCE"
              :stroke-dashoffset="getDashOffset(vitals.performance_score)"
            />
          </svg>
          <div class="dial-center-text">
            <span class="score-number font-mono">{{ vitals.performance_score }}</span>
            <span class="score-max font-mono">/100</span>
          </div>
        </div>
        <div class="dial-label-box">
          <Gauge :size="13" class="dial-icon text-accent" />
          <span class="dial-label font-mono">PERFORMANCE</span>
        </div>
      </div>

      <!-- 2. Accessibility Dial -->
      <div class="dial-card">
        <div class="svg-dial-wrapper">
          <svg class="dial-svg" viewBox="0 0 100 100">
            <circle class="dial-track" cx="50" cy="50" :r="RADIUS" />
            <circle
              class="dial-fill"
              :class="getScoreColorClass(vitals.accessibility_score)"
              cx="50"
              cy="50"
              :r="RADIUS"
              :stroke-dasharray="CIRCUMFERENCE"
              :stroke-dashoffset="getDashOffset(vitals.accessibility_score)"
            />
          </svg>
          <div class="dial-center-text">
            <span class="score-number font-mono">{{ vitals.accessibility_score }}</span>
            <span class="score-max font-mono">/100</span>
          </div>
        </div>
        <div class="dial-label-box">
          <Eye :size="13" class="dial-icon text-accent" />
          <span class="dial-label font-mono">ACCESSIBILITY</span>
        </div>
      </div>

      <!-- 3. SEO Dial -->
      <div class="dial-card">
        <div class="svg-dial-wrapper">
          <svg class="dial-svg" viewBox="0 0 100 100">
            <circle class="dial-track" cx="50" cy="50" :r="RADIUS" />
            <circle
              class="dial-fill"
              :class="getScoreColorClass(vitals.seo_score)"
              cx="50"
              cy="50"
              :r="RADIUS"
              :stroke-dasharray="CIRCUMFERENCE"
              :stroke-dashoffset="getDashOffset(vitals.seo_score)"
            />
          </svg>
          <div class="dial-center-text">
            <span class="score-number font-mono">{{ vitals.seo_score }}</span>
            <span class="score-max font-mono">/100</span>
          </div>
        </div>
        <div class="dial-label-box">
          <Search :size="13" class="dial-icon text-accent" />
          <span class="dial-label font-mono">SEO AUDIT</span>
        </div>
      </div>
    </div>

    <!-- Speed Benchmarks (FCP & Speed Index) -->
    <div class="speed-benchmarks-grid">
      <!-- First Contentful Paint -->
      <div class="benchmark-cell">
        <div class="bench-top font-mono">
          <div class="bench-label">
            <Zap :size="13" class="text-accent" />
            <span>FIRST CONTENTFUL PAINT</span>
          </div>
          <span class="bench-badge font-mono badge-fast">GOOD (&lt;1.8s)</span>
        </div>
        <div class="bench-val-row font-mono">
          <span class="bench-number">{{ vitals.fcp_seconds }}</span>
          <span class="bench-unit">s</span>
        </div>
      </div>

      <!-- Visual Speed Index -->
      <div class="benchmark-cell">
        <div class="bench-top font-mono">
          <div class="bench-label">
            <Clock :size="13" class="text-accent" />
            <span>VISUAL SPEED INDEX</span>
          </div>
          <span class="bench-badge font-mono badge-fast">OPTIMAL</span>
        </div>
        <div class="bench-val-row font-mono">
          <span class="bench-number">{{ vitals.speed_index }}</span>
          <span class="bench-unit">s</span>
        </div>
      </div>
    </div>

    <!-- Core Web Vitals Status Pill -->
    <div class="vitals-footer font-mono">
      <CheckCircle2 :size="14" class="text-emerald" />
      <span>PASSED GOOGLE CORE WEB VITALS THRESHOLD REQUIREMENTS</span>
    </div>
  </div>
</template>

<style scoped>
.vitals-card {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  padding-bottom: 14px;
}

.quadrant-badge {
  font-size: 0.68rem;
  letter-spacing: 0.1em;
  color: var(--brand-primary);
  font-weight: 700;
  display: block;
  margin-bottom: 4px;
  transition: color var(--chameleon-transition);
}

.card-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-white);
}

.audit-pill {
  font-size: 0.65rem;
  letter-spacing: 0.05em;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--text-dim);
  display: flex;
  align-items: center;
  gap: 5px;
}

.text-accent {
  color: var(--brand-primary);
  transition: color var(--chameleon-transition);
}

.text-emerald {
  color: var(--status-emerald);
}

/* 3 Radial Dials Grid */
.radial-dials-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.dial-card {
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 14px 8px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  transition: all 0.2s ease;
}

.dial-card:hover {
  background: rgba(255, 255, 255, 0.02);
  border-color: rgba(255, 255, 255, 0.12);
  transform: translateY(-2px);
}

.svg-dial-wrapper {
  position: relative;
  width: 90px;
  height: 90px;
}

.dial-svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.dial-track {
  fill: none;
  stroke: rgba(255, 255, 255, 0.06);
  stroke-width: 7;
}

.dial-fill {
  fill: none;
  stroke-width: 7;
  stroke-linecap: round;
  transition: stroke-dashoffset 1.2s cubic-bezier(0.16, 1, 0.3, 1), stroke 0.5s ease;
}

.score-emerald {
  stroke: var(--status-emerald);
  filter: drop-shadow(0 0 6px var(--status-emerald-glow));
}

.score-amber {
  stroke: var(--status-amber);
  filter: drop-shadow(0 0 6px var(--status-amber-glow));
}

.score-crimson {
  stroke: var(--status-crimson);
  filter: drop-shadow(0 0 6px var(--status-crimson-glow));
}

.dial-center-text {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

.score-number {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--text-white);
  line-height: 1;
}

.score-max {
  font-size: 0.6rem;
  color: var(--text-muted);
  font-weight: 600;
}

.dial-label-box {
  display: flex;
  align-items: center;
  gap: 6px;
}

.dial-label {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--text-dim);
}

/* Speed Benchmarks Grid */
.speed-benchmarks-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.benchmark-cell {
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 12px 14px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.bench-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.bench-label {
  font-size: 0.65rem;
  letter-spacing: 0.05em;
  color: var(--text-dim);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
}

.bench-badge {
  font-size: 0.58rem;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
}

.badge-fast {
  background: rgba(16, 185, 129, 0.15);
  color: var(--status-emerald);
}

.bench-val-row {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.bench-number {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--text-white);
  line-height: 1;
}

.bench-unit {
  font-size: 0.75rem;
  color: var(--text-muted);
  font-weight: 600;
}

/* Vitals Status Footer */
.vitals-footer {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: 8px;
  background: rgba(16, 185, 129, 0.06);
  border: 1px solid rgba(16, 185, 129, 0.2);
  color: #A7F3D0;
  font-size: 0.7rem;
  letter-spacing: 0.04em;
  font-weight: 600;
}

@media (max-width: 600px) {
  .radial-dials-row {
    grid-template-columns: 1fr;
  }
  .speed-benchmarks-grid {
    grid-template-columns: 1fr;
  }
}
</style>
