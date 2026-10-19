<script setup>
import { ref, watch } from 'vue';
import { useIntelStore } from '../stores/useIntelStore';
import { Search, ArrowRight, Loader2, Globe, AlertCircle, Sparkles } from 'lucide-vue-next';

const store = useIntelStore();
const inputDomain = ref(store.activeDomain.value || 'spotify.com');

// Synchronize input if activeDomain changes externally
watch(store.activeDomain, (newVal) => {
  if (newVal) inputDomain.value = newVal;
});

function handleSubmit() {
  if (!inputDomain.value.trim() || store.isLoading.value) return;
  store.fetchIntelligence(inputDomain.value);
}
</script>

<template>
  <div class="search-console-wrapper">
    <!-- Command Input Bar -->
    <form @submit.prevent="handleSubmit" class="search-form prism-card">
      <!-- Loading Radar Sweep Animation -->
      <div v-if="store.isLoading.value" class="radar-sweep-bar"></div>

      <div class="input-inner">
        <Globe class="search-icon" :size="20" />
        <input
          v-model="inputDomain"
          type="text"
          class="target-input font-mono"
          placeholder="Enter target domain or URL (e.g. stripe.com, spotify.com, github.com)..."
          autocomplete="off"
          spellcheck="false"
        />
        <button
          type="submit"
          class="analyze-btn font-mono"
          :disabled="store.isLoading.value"
        >
          <template v-if="store.isLoading.value">
            <Loader2 class="spinner" :size="16" />
            <span>ACQUIRING TELEMETRY...</span>
          </template>
          <template v-else>
            <span>PROBE TARGET</span>
            <ArrowRight :size="15" />
          </template>
        </button>
      </div>
    </form>

    <!-- Interactive 1-Click Target Chips -->
    <div class="presets-row">
      <span class="presets-label font-mono">
        <Sparkles :size="13" class="sparkle-icon" />
        QUICK TARGETS:
      </span>
      <div class="chips-container">
        <button
          v-for="preset in store.presets.value"
          :key="preset.domain"
          type="button"
          class="preset-chip font-mono"
          :class="{ 'preset-chip-active': store.activeDomain.value === preset.domain }"
          :style="{
            '--chip-color': preset.primary_color,
          }"
          @click="store.loadPreset(preset)"
        >
          <span class="chip-dot" :style="{ backgroundColor: preset.primary_color }"></span>
          <span>{{ preset.name }}</span>
        </button>
      </div>
    </div>

    <!-- Error Notice if Ingestion Fails -->
    <div v-if="store.error.value" class="error-banner font-mono">
      <AlertCircle :size="16" />
      <span>{{ store.error.value }}</span>
    </div>
  </div>
</template>

<style scoped>
.search-console-wrapper {
  margin-bottom: 32px;
  position: relative;
  z-index: 2;
}

.search-form {
  padding: 12px 16px;
  border-radius: 14px;
}

.input-inner {
  display: flex;
  align-items: center;
  gap: 14px;
  position: relative;
  z-index: 2;
}

.search-icon {
  color: var(--brand-primary);
  flex-shrink: 0;
  transition: color var(--chameleon-transition);
}

.target-input {
  flex: 1;
  background: transparent;
  border: none;
  color: var(--text-white);
  font-size: 0.95rem;
  outline: none;
  letter-spacing: 0.03em;
}

.target-input::placeholder {
  color: var(--text-muted);
}

.analyze-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--brand-primary);
  color: #05070A;
  font-weight: 700;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  padding: 10px 20px;
  border-radius: 8px;
  transition: all 0.25s ease;
  box-shadow: 0 0 15px rgba(var(--brand-primary-rgb), 0.35);
  flex-shrink: 0;
}

.analyze-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 0 25px rgba(var(--brand-primary-rgb), 0.55);
}

.analyze-btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Quick Target Preset Chips */
.presets-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 14px;
  flex-wrap: wrap;
}

.presets-label {
  font-size: 0.72rem;
  color: var(--text-dim);
  font-weight: 600;
  letter-spacing: 0.08em;
  display: flex;
  align-items: center;
  gap: 6px;
}

.sparkle-icon {
  color: var(--brand-primary);
  transition: color var(--chameleon-transition);
}

.chips-container {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.preset-chip {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  padding: 5px 12px;
  border-radius: 8px;
  font-size: 0.76rem;
  color: var(--text-dim);
  transition: all 0.25s ease;
}

.preset-chip:hover {
  background: rgba(255, 255, 255, 0.07);
  border-color: var(--chip-color);
  color: var(--text-white);
  transform: translateY(-1px);
}

.preset-chip-active {
  background: rgba(var(--brand-primary-rgb), 0.12);
  border-color: var(--brand-primary);
  color: var(--text-white);
  box-shadow: 0 0 12px rgba(var(--brand-primary-rgb), 0.25);
}

.chip-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  box-shadow: 0 0 6px currentColor;
}

/* Error Banner */
.error-banner {
  margin-top: 14px;
  padding: 10px 16px;
  border-radius: 8px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #FCA5A5;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

@media (max-width: 768px) {
  .input-inner {
    flex-direction: column;
    align-items: stretch;
  }
  .analyze-btn {
    justify-content: center;
  }
}
</style>
