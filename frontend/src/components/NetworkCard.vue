<script setup>
import { ref, computed } from 'vue';
import { useIntelStore } from '../stores/useIntelStore';
import { 
  Server, 
  Cloud, 
  Lock, 
  ShieldCheck, 
  ShieldAlert, 
  Zap, 
  Wifi, 
  Copy, 
  Check, 
  Radio 
} from 'lucide-vue-next';

const store = useIntelStore();
const copiedIp = ref(false);

const network = computed(() => store.dossier.value?.network || {
  cloud_host: 'Cloudflare Global Anycast Edge',
  ip_address: '104.16.132.229',
  ttfb_ms: 42.0,
  ssl_valid: true,
  ssl_days_left: 84,
  tls_version: 'TLSv1.3',
  server_header: 'cloudflare',
});

// Speed Tier Calculation
const speedTier = computed(() => {
  const ms = network.value.ttfb_ms;
  if (ms < 50) return { label: 'ULTRA-LOW LATENCY', class: 'tier-emerald' };
  if (ms < 150) return { label: 'OPTIMAL EDGE TTFB', class: 'tier-cyan' };
  if (ms < 300) return { label: 'MODERATE LATENCY', class: 'tier-amber' };
  return { label: 'HIGH TTFB DELAY', class: 'tier-crimson' };
});

// SSL Percentage remaining (based on standard 90-day Let's Encrypt / Cloudflare cycle)
const sslPercentage = computed(() => {
  const days = network.value.ssl_days_left || 0;
  return Math.min(100, Math.max(5, Math.round((days / 90) * 100)));
});

function copyIp() {
  if (!navigator.clipboard || !network.value.ip_address) return;
  navigator.clipboard.writeText(network.value.ip_address);
  copiedIp.value = true;
  setTimeout(() => {
    copiedIp.value = false;
  }, 1800);
}
</script>

<template>
  <div class="prism-card network-card">
    <!-- Quadrant Header -->
    <div class="card-header">
      <div class="header-left">
        <span class="quadrant-badge font-mono">QUADRANT 02 // TELEMETRY</span>
        <h3 class="card-title">Cloud & Network Edge</h3>
      </div>
      <div class="edge-status-pill font-mono">
        <span class="pulse-dot"></span>
        <span>EDGE PROBE ACTIVE</span>
      </div>
    </div>

    <!-- Cloud Hosting Giant Hero Box -->
    <div class="cloud-hero-box">
      <div class="cloud-icon-wrapper">
        <Cloud class="cloud-icon text-accent" :size="24" />
      </div>
      <div class="cloud-meta">
        <span class="meta-label font-mono">DETECTED CLOUD INFRASTRUCTURE</span>
        <h4 class="cloud-name font-mono">{{ network.cloud_host }}</h4>
      </div>
    </div>

    <!-- Telemetry Telemetry Matrix Grid -->
    <div class="telemetry-matrix">
      <!-- TTFB Speedometer Box -->
      <div class="matrix-cell">
        <div class="cell-top">
          <span class="cell-label font-mono">
            <Zap :size="13" class="text-accent" />
            TTFB RESPONSE
          </span>
          <span class="speed-tier-badge font-mono" :class="speedTier.class">
            {{ speedTier.label }}
          </span>
        </div>
        <div class="metric-value-row">
          <span class="metric-huge font-mono">{{ network.ttfb_ms }}</span>
          <span class="metric-unit font-mono">ms</span>
        </div>
      </div>

      <!-- Resolved IP Address Box -->
      <div class="matrix-cell">
        <div class="cell-top">
          <span class="cell-label font-mono">
            <Radio :size="13" class="text-accent" />
            PRIMARY IPv4 ANYCAST
          </span>
          <button type="button" class="copy-ip-btn font-mono" @click="copyIp">
            <Check v-if="copiedIp" :size="12" class="text-emerald" />
            <Copy v-else :size="12" />
            <span>{{ copiedIp ? 'COPIED' : 'COPY' }}</span>
          </button>
        </div>
        <div class="metric-value-row">
          <span class="metric-ip font-mono">{{ network.ip_address }}</span>
        </div>
      </div>
    </div>

    <!-- SSL/TLS Security Telemetry Section -->
    <div class="ssl-security-panel">
      <div class="ssl-header font-mono">
        <div class="ssl-title">
          <component
            :is="network.ssl_valid ? ShieldCheck : ShieldAlert"
            :size="15"
            :class="network.ssl_valid ? 'text-emerald' : 'text-crimson'"
          />
          <span>SSL/TLS ENCRYPTION INTEGRITY</span>
        </div>
        <span class="tls-version-badge font-mono">{{ network.tls_version }}</span>
      </div>

      <!-- SSL Progress Bar -->
      <div class="ssl-progress-wrapper">
        <div class="ssl-progress-track">
          <div
            class="ssl-progress-bar"
            :style="{ width: sslPercentage + '%' }"
            :class="sslPercentage < 20 ? 'bar-danger' : 'bar-healthy'"
          ></div>
        </div>
        <div class="ssl-meta-row font-mono">
          <span class="ssl-valid-status">
            {{ network.ssl_valid ? 'CERTIFICATE VALID' : 'CERTIFICATE EXPIRED / UNTRUSTED' }}
          </span>
          <span class="ssl-days-count">
            <Lock :size="11" />
            {{ network.ssl_days_left }} DAYS REMAINING
          </span>
        </div>
      </div>
    </div>

    <!-- Server Response Header Details -->
    <div class="server-header-footer font-mono">
      <span class="server-label">EDGE SERVER HEADER:</span>
      <code class="server-code">{{ network.server_header }}</code>
    </div>
  </div>
</template>

<style scoped>
.network-card {
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

.edge-status-pill {
  font-size: 0.65rem;
  letter-spacing: 0.05em;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 999px;
  background: rgba(16, 185, 129, 0.08);
  border: 1px solid rgba(16, 185, 129, 0.25);
  color: var(--text-white);
  display: flex;
  align-items: center;
  gap: 6px;
}

.text-accent {
  color: var(--brand-primary);
  transition: color var(--chameleon-transition);
}

.text-emerald {
  color: var(--status-emerald);
}

.text-crimson {
  color: var(--status-crimson);
}

/* Cloud Hosting Giant Hero Box */
.cloud-hero-box {
  display: flex;
  align-items: center;
  gap: 14px;
  background: rgba(var(--brand-primary-rgb), 0.06);
  border: 1px solid var(--brand-border);
  padding: 14px 16px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
  transition: all var(--chameleon-transition);
}

.cloud-icon-wrapper {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.cloud-meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.meta-label {
  font-size: 0.64rem;
  letter-spacing: 0.08em;
  color: var(--text-dim);
  font-weight: 600;
}

.cloud-name {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-white);
  letter-spacing: 0.02em;
}

/* Telemetry Matrix Grid */
.telemetry-matrix {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.matrix-cell {
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 12px 14px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.cell-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.cell-label {
  font-size: 0.65rem;
  letter-spacing: 0.05em;
  color: var(--text-dim);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 5px;
}

.speed-tier-badge {
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  padding: 2px 6px;
  border-radius: 4px;
}

.tier-emerald {
  background: rgba(16, 185, 129, 0.15);
  color: var(--status-emerald);
}

.tier-cyan {
  background: rgba(6, 182, 212, 0.15);
  color: var(--status-cyan);
}

.tier-amber {
  background: rgba(245, 158, 11, 0.15);
  color: var(--status-amber);
}

.tier-crimson {
  background: rgba(239, 68, 68, 0.15);
  color: var(--status-crimson);
}

.metric-value-row {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.metric-huge {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--text-white);
  line-height: 1;
}

.metric-unit {
  font-size: 0.75rem;
  color: var(--text-muted);
  font-weight: 600;
}

.metric-ip {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-white);
  letter-spacing: 0.03em;
}

.copy-ip-btn {
  font-size: 0.62rem;
  color: var(--text-dim);
  display: inline-flex;
  align-items: center;
  gap: 3px;
  padding: 2px 6px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.05);
  transition: all 0.2s;
}

.copy-ip-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-white);
}

/* SSL / TLS Panel */
.ssl-security-panel {
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 12px 14px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.ssl-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.ssl-title {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--text-dim);
  display: flex;
  align-items: center;
  gap: 6px;
}

.tls-version-badge {
  font-size: 0.65rem;
  font-weight: 700;
  background: rgba(255, 255, 255, 0.06);
  padding: 2px 6px;
  border-radius: 4px;
  color: var(--text-white);
}

.ssl-progress-track {
  width: 100%;
  height: 5px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.08);
  overflow: hidden;
}

.ssl-progress-bar {
  height: 100%;
  border-radius: 999px;
  transition: width 0.8s ease;
}

.bar-healthy {
  background: linear-gradient(90deg, var(--brand-primary), var(--status-emerald));
  box-shadow: 0 0 10px var(--status-emerald);
}

.bar-danger {
  background: var(--status-crimson);
  box-shadow: 0 0 10px var(--status-crimson);
}

.ssl-meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.65rem;
  color: var(--text-dim);
  font-weight: 600;
  margin-top: 4px;
}

.ssl-days-count {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--text-white);
}

/* Server Header Footer */
.server-header-footer {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.68rem;
  color: var(--text-muted);
}

.server-label {
  letter-spacing: 0.05em;
  font-weight: 600;
}

.server-code {
  color: var(--text-dim);
  background: rgba(255, 255, 255, 0.04);
  padding: 2px 6px;
  border-radius: 4px;
}

@media (max-width: 600px) {
  .telemetry-matrix {
    grid-template-columns: 1fr;
  }
}
</style>
