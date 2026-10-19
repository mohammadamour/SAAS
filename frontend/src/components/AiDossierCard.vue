<script setup>
import { computed } from 'vue';
import { useIntelStore } from '../stores/useIntelStore';
import { 
  Brain, 
  Shield, 
  AlertTriangle, 
  Users, 
  Layers, 
  Quote, 
  ArrowUpRight, 
  Cpu 
} from 'lucide-vue-next';

const store = useIntelStore();

const aiData = computed(() => store.dossier.value?.ai_dossier || {
  brutal_truth: 'An audio streaming utility paying 70% in royalties, desperately pivoting into podcasts and audiobooks to defend gross margins.',
  moat: 'Unrivaled algorithmic discovery (Discover Weekly, Daylist) and deeply entrenched cross-platform social playlist networks.',
  vulnerability: 'Complete dependency on the big three record labels who possess catalogue veto power and royalty renegotiation leverage.',
  top_competitors: ['Apple Music', 'YouTube Music', 'Amazon Music'],
  estimated_tech_stack: ['React / Next.js', 'Java / Spring Boot microservices', 'Google Cloud BigQuery', 'Fastly Global CDN'],
});

function probeCompetitor(compName) {
  // Extract simple clean domain guess or search string
  let target = compName.toLowerCase().replace(/\s*\(.*\)/, '').trim();
  if (!target.includes('.')) {
    if (target.includes('apple')) target = 'apple.com';
    else if (target.includes('youtube')) target = 'youtube.com';
    else if (target.includes('amazon')) target = 'amazon.com';
    else if (target.includes('google')) target = 'google.com';
    else if (target.includes('jira') || target.includes('atlassian')) target = 'atlassian.com';
    else if (target.includes('github')) target = 'github.com';
    else if (target.includes('adyen')) target = 'adyen.com';
    else if (target.includes('paypal')) target = 'paypal.com';
    else target = `${target.replace(/\s+/g, '')}.com`;
  }
  store.fetchIntelligence(target);
}
</script>

<template>
  <div class="prism-card ai-card">
    <!-- Quadrant Header -->
    <div class="card-header">
      <div class="header-left">
        <span class="quadrant-badge font-mono">QUADRANT 04 // STRATEGIC INTEL</span>
        <h3 class="card-title">AI Executive Teardown</h3>
      </div>
      <div class="lpu-pill font-mono">
        <Brain :size="13" class="text-accent" />
        <span>LLM REASONING ENGINE</span>
      </div>
    </div>

    <!-- The Brutal Truth Quote Box -->
    <div class="brutal-truth-box">
      <div class="truth-header font-mono">
        <Quote :size="14" class="text-accent" />
        <span>THE UNFILTERED TRUTH:</span>
      </div>
      <p class="truth-text font-sans">
        "{{ aiData.brutal_truth }}"
      </p>
    </div>

    <!-- Moat vs Vulnerability Grid -->
    <div class="strategy-grid">
      <!-- Competitive Moat -->
      <div class="strategy-cell moat-cell">
        <div class="cell-title-row font-mono">
          <Shield :size="14" class="text-emerald" />
          <span class="cell-heading text-emerald">COMPETITIVE MOAT</span>
        </div>
        <p class="cell-body">
          {{ aiData.moat }}
        </p>
      </div>

      <!-- Strategic Vulnerability -->
      <div class="strategy-cell vuln-cell">
        <div class="cell-title-row font-mono">
          <AlertTriangle :size="14" class="text-amber" />
          <span class="cell-heading text-amber">EXISTENTIAL THREAT</span>
        </div>
        <p class="cell-body">
          {{ aiData.vulnerability }}
        </p>
      </div>
    </div>

    <!-- Top 3 Competitors Radar -->
    <div class="competitors-section">
      <div class="section-heading font-mono">
        <Users :size="13" class="text-accent" />
        <span>DIRECT MARKET CONTENDERS (CLICK TO PROBE):</span>
      </div>
      <div class="competitor-chips">
        <button
          v-for="competitor in aiData.top_competitors"
          :key="competitor"
          type="button"
          class="competitor-chip font-mono"
          @click="probeCompetitor(competitor)"
          title="Click to probe this competitor"
        >
          <span>{{ competitor }}</span>
          <ArrowUpRight :size="12" class="arrow-icon" />
        </button>
      </div>
    </div>

    <!-- Inferred Tech Stack Blueprint -->
    <div class="tech-stack-section">
      <div class="section-heading font-mono">
        <Layers :size="13" class="text-accent" />
        <span>INFERRED ARCHITECTURE & TECH STACK:</span>
      </div>
      <div class="tech-tags">
        <span
          v-for="tech in aiData.estimated_tech_stack"
          :key="tech"
          class="tech-tag font-mono"
        >
          <Cpu :size="11" class="text-accent" />
          {{ tech }}
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ai-card {
  display: flex;
  flex-direction: column;
  gap: 18px;
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

.lpu-pill {
  font-size: 0.65rem;
  letter-spacing: 0.05em;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 999px;
  background: rgba(var(--brand-primary-rgb), 0.08);
  border: 1px solid var(--brand-border);
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

.text-amber {
  color: var(--status-amber);
}

/* Brutal Truth Box */
.brutal-truth-box {
  background: rgba(var(--brand-primary-rgb), 0.05);
  border-left: 3px solid var(--brand-primary);
  padding: 14px 16px;
  border-radius: 0 10px 10px 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: border-color var(--chameleon-transition), background var(--chameleon-transition);
}

.truth-header {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--text-dim);
}

.truth-text {
  font-size: 0.92rem;
  line-height: 1.5;
  color: var(--text-white);
  font-weight: 500;
  font-style: italic;
}

/* Strategy Grid */
.strategy-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.strategy-cell {
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 12px 14px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.cell-title-row {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.68rem;
  letter-spacing: 0.06em;
  font-weight: 700;
}

.moat-cell {
  border-top: 2px solid var(--status-emerald);
}

.vuln-cell {
  border-top: 2px solid var(--status-amber);
}

.cell-body {
  font-size: 0.8rem;
  color: var(--text-dim);
  line-height: 1.45;
}

/* Competitors Section */
.competitors-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.section-heading {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 6px;
}

.competitor-chips {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.competitor-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.75rem;
  color: var(--text-dim);
  transition: all 0.2s ease;
}

.competitor-chip:hover {
  background: rgba(var(--brand-primary-rgb), 0.12);
  border-color: var(--brand-border);
  color: var(--text-white);
  transform: translateY(-1px);
}

.arrow-icon {
  color: var(--brand-primary);
  opacity: 0.6;
}

.competitor-chip:hover .arrow-icon {
  opacity: 1;
}

/* Tech Stack Section */
.tech-stack-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tech-tags {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.tech-tag {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(255, 255, 255, 0.06);
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 0.7rem;
  color: var(--text-dim);
}

@media (max-width: 600px) {
  .strategy-grid {
    grid-template-columns: 1fr;
  }
}
</style>
