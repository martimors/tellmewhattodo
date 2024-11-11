<script setup lang="ts">
import { onBeforeMount, onMounted, ref } from 'vue';
import AlertItem from './AlertItem.vue'
import { getAlertsGet } from '@/client';

const alertStore = ref([])

const initialLoadAlerts = async () => {
  const alerts = await getAlertsGet();
  alertStore.value = alerts.data;
}

onBeforeMount(initialLoadAlerts);

</script>

<template>
  <template v-for="al in alertStore" :key="al.id">
    <AlertItem :name="al.name" :created_at="new Date(al.created_at)" :alert_type="al.alert_type" :acked="al.acked"
      :description="al.description" :url="al.url" />
  </template></template>
