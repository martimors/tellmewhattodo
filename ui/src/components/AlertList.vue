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
  const alert_ix = alertStore.value.findIndex((a) => a.id === id)
  const old_alert = alertStore.value[alert_ix]
  try {
     const new_alert = await ackAlertAlertIdPatch({
      query: {
        acked: !old_alert!.acked,
      },
      path: {
        alert_id: old_alert!.id,
      },
    })
    alertStore.value[alert_ix] = new_alert.data!
  } catch {
    console.error(`Could not ack alert ${id}`)
  }
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
        :last_acked_name="al.last_acked_name ?? ''"
      />
    </template>
  </BListGroup>
</template>
