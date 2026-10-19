<script setup>
import { ref } from 'vue';
import { useIntelStore } from '../stores/useIntelStore';
import { 
  ShieldCheck, 
  Globe, 
  ExternalLink, 
  Copy, 
  Check, 
  Palette, 
  Hash 
} from 'lucide-vue-next';

const store = useIntelStore();
const copiedColor = ref(null);

function copyHex(hex) {
  if (!navigator.clipboard) return;
  navigator.clipboard.writeText(hex);
  copiedColor.value = hex;
  setTimeout(() => {
    copiedColor.value = null;
  }, 1800);
}

function handleImageError(e) {
  // Graceful fallback to colored domain initials if logo 404s
  e.target.style.display = 'none';
  if (e.target.nextElementSibling) {
    e.target.nextElementSibling.style.display = 'flex';
  }
}
</script>

<template>
  <div class="prism-card brand-card">
    <!-- Quadrant Header -->
    <div class="card-header">
      <div class="header-left">
        <span class="quadrant-badge font-mono">QUADRANT 01 // IDENTITY</span>
        <h3 class="card-title">Brand & Footprint</h3>
      </div>
      <div class="verified-pill font-mono">
        <ShieldCheck :size="13" class="text-accent" />
        <span>VERIFIED ENTITY</span>
      </div>
    </div>

    <!-- Company Profile Lockup -->
    <div class="brand-profile">
      <div class="logo-wrapper">
        <img
          v-if="store.dossier.value?.brand?.logo_url"
          :src="store.dossier.value.brand.logo_url"
          :alt="store.dossier.value?.brand?.name"
          class="company-logo"
          @error="handleImageError"
        />
        <div class="logo-fallback font-mono" style="display: none;">
          {{ (store.dossier.value?.brand?.name || 'P').charAt(0) }}
        </div>
      </div>
      <div class="profile-details">
        <div class="name-row">
          <h2 class="company-name">{{ store.dossier.value?.brand?.name || 'Company Name' }}</h2>
          <a
            :href="'https://' + store.dossier.value?.domain"
            target="_blank"
            rel="noopener noreferrer"
            class="domain-link font-mono"
          >
            <span>{{ store.dossier.value?.domain }}</span>
            <ExternalLink :size="12" />
          </a>
        </div>
        <p class="company-bio">
          {{ store.dossier.value?.brand?.description || 'Corporate metadata synchronized via edge probe.' }}
        </p>
      </div>
    </div>

    <!-- Extracted Brand Color Spectrum -->
    <div class="palette-section">
      <div class="palette-title font-mono">
        <Palette :size="14" class="text-accent" />
        <span>EXTRACTED BRAND COLOR SPECTRUM</span>
      </div>
      <div class="swatches-grid">
        <!-- Primary Swatch -->
        <div
          class="swatch-card"
          @click="copyHex(store.dossier.value?.brand?.primary_color || '#00F0FF')"
          title="Click to copy Hex code"
        >
          <div
            class="color-preview"
            :style="{ backgroundColor: store.dossier.value?.brand?.primary_color || '#00F0FF' }"
          ></div>
          <div class="swatch-meta font-mono">
            <span class="swatch-label">PRIMARY // ACCENT</span>
            <span class="swatch-hex">
              <Hash :size="11" />
              {{ store.dossier.value?.brand?.primary_color || '#00F0FF' }}
            </span>
          </div>
          <button type="button" class="copy-icon-btn">
            <Check v-if="copiedColor === (store.dossier.value?.brand?.primary_color || '#00F0FF')" :size="13" class="text-emerald" />
            <Copy v-else :size="13" />
          </button>
        </div>

        <!-- Secondary Swatch -->
        <div
          class="swatch-card"
          @click="copyHex(store.dossier.value?.brand?.secondary_color || '#7928CA')"
          title="Click to copy Hex code"
        >
          <div
            class="color-preview"
            :style="{ backgroundColor: store.dossier.value?.brand?.secondary_color || '#7928CA' }"
          ></div>
          <div class="swatch-meta font-mono">
            <span class="swatch-label">SECONDARY // GLOW</span>
            <span class="swatch-hex">
              <Hash :size="11" />
              {{ store.dossier.value?.brand?.secondary_color || '#7928CA' }}
            </span>
          </div>
          <button type="button" class="copy-icon-btn">
            <Check v-if="copiedColor === (store.dossier.value?.brand?.secondary_color || '#7928CA')" :size="13" class="text-emerald" />
            <Copy v-else :size="13" />
          </button>
        </div>
      </div>
    </div>

    <!-- Verified Footprint Links -->
    <div class="footprint-footer">
      <div class="links-title font-mono">VERIFIED NETWORKS:</div>
      <div class="social-pills">
        <a
          v-for="(url, network) in store.dossier.value?.brand?.social_links || {}"
          :key="network"
          :href="url"
          target="_blank"
          rel="noopener noreferrer"
          class="prism-pill font-mono social-pill"
        >
          <Globe :size="12" />
          <span>{{ network.toUpperCase() }}</span>
        </a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.brand-card {
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

.verified-pill {
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

/* Brand Profile Lockup */
.brand-profile {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.logo-wrapper {
  width: 58px;
  height: 58px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--brand-border);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
  flex-shrink: 0;
  transition: border-color var(--chameleon-transition);
}

.company-logo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  padding: 6px;
}

.logo-fallback {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--brand-primary);
}

.profile-details {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
}

.name-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.company-name {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--text-white);
  letter-spacing: -0.01em;
}

.domain-link {
  font-size: 0.75rem;
  color: var(--brand-primary);
  display: inline-flex;
  align-items: center;
  gap: 4px;
  text-decoration: none;
  background: rgba(var(--brand-primary-rgb), 0.08);
  padding: 2px 8px;
  border-radius: 6px;
  border: 1px solid var(--brand-border);
  transition: all 0.2s ease;
}

.domain-link:hover {
  background: rgba(var(--brand-primary-rgb), 0.18);
  transform: translateY(-1px);
}

.company-bio {
  font-size: 0.85rem;
  color: var(--text-dim);
  line-height: 1.45;
}

/* Palette Swatches */
.palette-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: rgba(0, 0, 0, 0.25);
  padding: 14px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.04);
}

.palette-title {
  font-size: 0.7rem;
  letter-spacing: 0.08em;
  font-weight: 700;
  color: var(--text-dim);
  display: flex;
  align-items: center;
  gap: 6px;
}

.swatches-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.swatch-card {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.07);
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.swatch-card:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.15);
  transform: translateY(-1px);
}

.color-preview {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  flex-shrink: 0;
}

.swatch-meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.swatch-label {
  font-size: 0.62rem;
  color: var(--text-muted);
  letter-spacing: 0.05em;
  font-weight: 600;
}

.swatch-hex {
  font-size: 0.78rem;
  color: var(--text-white);
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 2px;
}

.copy-icon-btn {
  color: var(--text-muted);
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}

.swatch-card:hover .copy-icon-btn {
  color: var(--text-white);
}

/* Verified Footprint Links */
.footprint-footer {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  padding-top: 4px;
}

.links-title {
  font-size: 0.68rem;
  letter-spacing: 0.08em;
  color: var(--text-muted);
  font-weight: 700;
}

.social-pills {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.social-pill {
  text-decoration: none;
  font-size: 0.68rem;
  padding: 3px 10px;
  transition: all 0.2s ease;
}

.social-pill:hover {
  border-color: var(--brand-border);
  color: var(--text-white);
  transform: translateY(-1px);
}

@media (max-width: 600px) {
  .swatches-grid {
    grid-template-columns: 1fr;
  }
}
</style>
