<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useIntelStore } from '../stores/useIntelStore';
import { Terminal, Cpu, Database, Activity } from 'lucide-vue-next';

const { cacheStats } = useIntelStore();

// Live UTC Zulu Clock
const zuluTime = ref('');
let timer = null;

function updateClock() {
  const now = new Date();
  zuluTime.value = now.toISOString().substring(11, 19) + ' UTC';
}

onMounted(() => {
  updateClock();
  timer = setInterval(updateClock, 1000);
});

onUnmounted(() => {
  if (timer) clearInterval(timer);
});
</script>

<template>
  <header class="prism-header">
    <!-- Brand Terminal Identifier -->
    <div class="brand-lockup">
      <div class="logo-box">
        <Terminal class="logo-icon" :size="20" />
      </div>
      <div class="brand-text">
        <div class="title-row">
          <span class="brand-title">PRISM // OS</span>
          <span class="version-tag">v2.4-PROBE</span>
        </div>
        <span class="brand-sub">Autonomous Corporate & Infrastructure Intelligence</span>
      </div>
    </div>

    <!-- Telemetry Status Pills -->
    <div class="hud-telemetry">
      <!-- Live UTC Clock -->
      <div class="prism-pill font-mono clock-pill">
        <Activity :size="13" class="pill-icon text-accent" />
        <span>{{ zuluTime }}</span>
      </div>

      <!-- Redis In-Memory Telemetry Pill -->
      <div class="prism-pill font-mono redis-pill">
        <span class="pulse-dot"></span>
        <Database :size="13" class="pill-icon text-accent" />
        <span class="redis-text">
          {{ cacheStats.engine.toUpperCase() }}
        </span>
        <span class="cache-badge">{{ cacheStats.cached_dossiers_count }} INDEXED</span>
      </div>
    </div>
  </header>
</template>

<style scoped>
.prism-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 0 28px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
  margin-bottom: 32px;
  position: relative;
  z-index: 2;
}

.brand-lockup {
  display: flex;
  align-items: center;
  gap: 14px;
}

.logo-box {
  width: 42px;
  height: 42px;
  border-radius: 10px;
  background: rgba(var(--brand-primary-rgb), 0.12);
  border: 1px solid var(--brand-border);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--brand-primary);
  box-shadow: var(--brand-glow-sm);
  transition: all var(--chameleon-transition);
}

.title-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-title {
  font-size: 1.15rem;
  font-weight: 800;
  letter-spacing: 0.1em;
  color: var(--text-white);
  font-family: var(--font-mono);
}

.version-tag {
  font-size: 0.65rem;
  font-family: var(--font-mono);
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
  background: rgba(var(--brand-primary-rgb), 0.15);
  color: var(--brand-primary);
  border: 1px solid var(--brand-border);
  letter-spacing: 0.05em;
  transition: all var(--chameleon-transition);
}

.brand-sub {
  font-size: 0.78rem;
  color: var(--text-dim);
  font-weight: 500;
}

.hud-telemetry {
  display: flex;
  align-items: center;
  gap: 12px;
}

.text-accent {
  color: var(--brand-primary);
  transition: color var(--chameleon-transition);
}

.redis-pill {
  background: rgba(16, 185, 129, 0.08);
  border-color: rgba(16, 185, 129, 0.25);
  color: var(--text-white);
}

.cache-badge {
  font-size: 0.65rem;
  background: rgba(255, 255, 255, 0.08);
  padding: 1px 6px;
  border-radius: 4px;
  color: var(--text-dim);
}

@media (max-width: 768px) {
  .prism-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  .hud-telemetry {
    width: 100%;
    justify-content: space-between;
  }
}
</style>
