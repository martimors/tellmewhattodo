<script setup lang="ts">
import { computed, ref } from 'vue'
import { dateFormatter } from './datetime'
import { BButton, BListGroupItem } from 'bootstrap-vue-next'

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
  <BListGroupItem :variant="props.acked ? 'success' : 'danger'">
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
    <div class="details">
      <BButton @click="$emit('ack', props.id)">{{ props.acked ? 'unack' : 'ack' }}</BButton>
      {{ description }}
    </div>
  </BListGroupItem>
</template>

<style scoped>
.name .date {
  font-style: italic;
  opacity: 90%;
}
</style>
