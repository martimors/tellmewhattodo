<script setup lang="ts">
import { computed } from 'vue';
import { dateFormatter } from './datetime';

const props = defineProps<{
  name: string
  created_at: Date
  alert_type: string
  acked: boolean
  description: string
  url?: (string | null)
}>();

const icon = computed(() => {
  return props.alert_type == "github" ? "bi-github" : "ri-questionnaire-line";
});

const just_date = computed(() => {
  return dateFormatter.format(props.created_at);
});

</script>

<template>
  <div class="item">
    <i>
      <v-icon v-bind:name="icon" />
    </i>
    <h3 v-if="url != null"><a v-bind:href="url" target="_blank" rel="noopener">{{ name }}</a></h3>
    <h3 v-else>{{ name }}</h3>
    <p>{{ description }}</p>
    <p>{{ just_date }}</p>
    <button>{{ acked }}</button>
  </div>
</template>

<style scoped>
.item {
  margin-top: 2rem;
  display: flex;
  position: relative;
}

.details {
  flex: 1;
  margin-left: 1rem;
}

i {
  display: flex;
  place-items: center;
  place-content: center;
  width: 32px;
  height: 32px;

  color: var(--color-text);
}

h3 {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 0.4rem;
  color: var(--color-heading);
}

@media (min-width: 1024px) {
  .item {
    margin-top: 0;
    padding: 0.4rem 0 1rem calc(var(--section-gap) / 2);
  }

  i {
    top: calc(50% - 25px);
    left: -26px;
    position: absolute;
    border: 1px solid var(--color-border);
    background: var(--color-background);
    border-radius: 8px;
    width: 50px;
    height: 50px;
  }

  .item:before {
    content: ' ';
    border-left: 1px solid var(--color-border);
    position: absolute;
    left: 0;
    bottom: calc(50% + 25px);
    height: calc(50% - 25px);
  }

  .item:after {
    content: ' ';
    border-left: 1px solid var(--color-border);
    position: absolute;
    left: 0;
    top: calc(50% + 25px);
    height: calc(50% - 25px);
  }

  .item:first-of-type:before {
    display: none;
  }

  .item:last-of-type:after {
    display: none;
  }
}
</style>
