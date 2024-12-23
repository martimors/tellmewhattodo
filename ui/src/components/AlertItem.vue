<script setup lang="ts">
import { computed, ref } from 'vue'
import { dateFormatter } from './datetime'
import { BButton } from 'bootstrap-vue-next';

const bgColor = computed(() => {
  return props.acked ? '#228100' : '#e0432e'
})

const props = defineProps<{
  id: string
  name: string
  created_at: Date
  alert_type: string
  acked: boolean
  description: string
  url?: string | null
}>()

const icon = computed(() => {
  return props.alert_type == 'github' ? 'bi-github' : 'ri-questionnaire-line'
})

const just_date = computed(() => {
  return dateFormatter.format(props.created_at)
})
</script>

<template>
  <div class="item">
    <div class="name">
      <i>
        <v-icon v-bind:name="icon" />
      </i>
      <span v-if="url != null"
        ><a v-bind:href="url" target="_blank" rel="noopener">{{ name }}</a></span
      >
      <span v-else>{{ name }}</span>
      <span class="date">{{ just_date }}</span>
    </div>
    <div class="details">{{ description }}</div>
    <BButton @click="$emit('ack', props.id)">{{ props.acked ? 'unack' : 'ack' }}</BButton>
  </div>
</template>

<style scoped>
.item {
  padding: 1rem;
  margin: 1rem 0 0 0;
  position: relative;
  display: grid;
  gap: 1rem;
  border: 1rem solid v-bind(bgColor);
  border-radius: 2rem;
  background-color: v-bind(bgColor);
}

.details {
  flex: 1;
  margin-left: 1rem;
}

i {
  place-items: center;
  place-content: center;
  width: 32px;
  height: 32px;
  padding-right: 1rem;

  color: var(--color-text);
}

.name {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 0.4rem;
  color: var(--color-heading);
}

.name .date {
  font-style: italic;
  opacity: 90%;
}
</style>
