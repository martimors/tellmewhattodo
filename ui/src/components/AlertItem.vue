<script setup lang="ts">
import { computed, ref } from 'vue'
import { dateFormatter } from './datetime'
import { BButton, BListGroupItem } from 'bootstrap-vue-next'

const props = defineProps<{
  id: string
  name: string
  created_at: Date
  alert_type: string
  acked: boolean
  description: string
  url?: string | null
  last_acked_name?: string | null
}>()

const icon = computed(() => {
  if (props.alert_type == 'github') return 'bi-github'
  else if (props.alert_type == 'docker_helm') return 'vi-file-type-helm'
  else return 'ri-questionnaire-line'
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
      <span v-if="url != null"><a v-bind:href="url" target="_blank" rel="noopener">{{ name }}</a></span>
      <span v-else>{{ name }}</span>
      <span class="date">{{ just_date }}
        <span v-if="last_acked_name != '' && !acked">(last acked {{ last_acked_name }})</span> </span>
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
