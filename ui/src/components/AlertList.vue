<script setup lang="ts">
import { onBeforeMount, ref, type Ref } from 'vue'
import AlertItem from './AlertItem.vue'
import { ackAlertAlertIdPatch, getAlertsGet, type Alert } from '@/client'
import { BListGroup } from 'bootstrap-vue-next'

const alertStore: Ref<Array<Alert>> = ref([])

const initialLoadAlerts = async () => {
  try {
    const alerts = await getAlertsGet()
    if (alerts.data) {
      // API call successful, store the data
      alertStore.value = alerts.data
    } else if (alerts.error) {
      console.error(alerts.error)
    }
  } catch (err) {
    console.error(err)
  }
}

const sortAlerts = () => {
  console.log("Sortin'")
  alertStore.value.sort((a, b) => {
    if (a.acked !== b.acked) {
      return Number(a.acked) - Number(b.acked)
    }
    if (a.created_at !== b.created_at) {
      return b.created_at.localeCompare(a.created_at)
    }
    return a.name.localeCompare(b.name)
  })
}

const ackAlert = async (id: string) => {
  const alert_ = alertStore.value.find((a) => a.id === id)
  try {
    await ackAlertAlertIdPatch({
      query: {
        acked: !alert_!.acked,
      },
      path: {
        alert_id: alert_!.id,
      },
    })
  } catch {
    console.error(`Could not ack alert ${id}`)
  }
  alert_!.acked = !alert_!.acked
  sortAlerts()
}

onBeforeMount(initialLoadAlerts)
</script>

<template>
  <BListGroup>
    <template v-for="al in alertStore" :key="al.id">
      <AlertItem
        @ack="ackAlert"
        :id="al.id"
        :name="al.name"
        :created_at="new Date(al.created_at)"
        :alert_type="al.alert_type"
        :acked="al.acked ?? false"
        :description="al.description ?? ''"
        :url="al.url"
      />
    </template>
  </BListGroup>
</template>
