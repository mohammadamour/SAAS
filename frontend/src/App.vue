<script setup>
import { onMounted } from 'vue';
import { useIntelStore } from './stores/useIntelStore';
import HeaderBar from './components/HeaderBar.vue';
import SearchConsole from './components/SearchConsole.vue';
import BrandCard from './components/BrandCard.vue';
import NetworkCard from './components/NetworkCard.vue';
import VitalsCard from './components/VitalsCard.vue';
import AiDossierCard from './components/AiDossierCard.vue';

const store = useIntelStore();

onMounted(() => {
  store.fetchCacheTelemetry();
});
</script>

<template>
  <!-- Cybernetic Dynamic Ambient Aura Orbs (Morphs with active company colors) -->
  <div class="ambient-aura ambient-aura-primary" aria-hidden="true"></div>
  <div class="ambient-aura ambient-aura-secondary" aria-hidden="true"></div>

  <!-- Master Application Shell -->
  <main class="terminal-shell">
    <!-- Top HUD Navigation Bar -->
    <HeaderBar />

    <!-- Search & Recon Console -->
    <SearchConsole />

    <!-- 4-Quadrant High-Density Intelligence Bento Grid -->
    <section class="prism-grid-2x2">
      <!-- Quadrant 1: Brand & Identity -->
      <BrandCard />

      <!-- Quadrant 2: Cloud Infrastructure & SSL -->
      <NetworkCard />

      <!-- Quadrant 3: Performance & Core Vitals -->
      <VitalsCard />

      <!-- Quadrant 4: AI Strategic Teardown -->
      <AiDossierCard />
    </section>
  </main>
</template>

<style scoped>
.terminal-shell {
  width: 100%;
  position: relative;
  z-index: 1;
}
</style>
