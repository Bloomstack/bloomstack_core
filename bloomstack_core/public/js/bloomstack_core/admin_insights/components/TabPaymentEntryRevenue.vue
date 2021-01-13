<template>
  <div class="col-md-4 col-xs-12 total-weekly-revenue row">
    <div class="container">
      <span class="amount" v-if="this.values[0][this.metrics[0]] === null"
        >$ 0.00</span
      >
      <span class="amount" v-else>$ {{ this.values[0][this.metrics[0]] }}</span>
      <span class="name">{{ title }}</span>
      <span class="description">{{ description }}</span>
    </div>
  </div>
</template>
<script>
export default {
  name: "TabPaymentEntryRevnue",
  props: {
    values: Array,
    metrics: Array,
    title: String,
    description: String,
  },
};
</script>
