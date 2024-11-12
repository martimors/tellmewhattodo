<script setup lang="ts">
import { onBeforeMount, onMounted, ref, type Ref } from 'vue';
import AlertItem from './AlertItem.vue'
import { ackAlertAlertIdPatch, getAlertsGet, type Alert } from '@/client';

const alertStore: Ref<Array<Alert>> = ref([])

const initialLoadAlerts = async () => {
  try {
    const alerts = await getAlertsGet();
    if (alerts.data) {
      // API call successful, store the data
      alertStore.value = alerts.data;
    } else if (alerts.error) {
      console.error(alerts.error);
    }
  } catch (err) {
    console.error(err);
  }
}

const ackAlert = async (alert: Alert) => {
  try {
    await ackAlertAlertIdPatch({
      query: {
        acked: !alert.acked
      },
      path: {
        alert_id: alert.id
      }
    });
  } catch {
    console.error(`Could not ack alert ${alert.id}`)
  }
}

onBeforeMount(initialLoadAlerts);

</script>

<template>
  <template v-for="al in alertStore" :key="al.id">
    <AlertItem :name="al.name" :created_at="new Date(al.created_at)" :alert_type="al.alert_type"
      :acked="al.acked ?? false" :description="al.description ?? ''" :url="al.url" />
  </template>
</template>
