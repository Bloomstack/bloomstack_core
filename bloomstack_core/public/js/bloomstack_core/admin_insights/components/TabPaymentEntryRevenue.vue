<template>
  <div>

    <h1 v-if="this.values[0][this.metrics[0]] === null">$ 0.00</h1>
    <h1 v-else>$ {{this.values[0][this.metrics[0]]}}</h1>
    <h3>{{title}}</h3>
    {{description}}
  </div>
</template>
<script>
  export default {
    name:"TabPaymentEntryRevnue",
    props: {
      values: Array,
      metrics: Array,
      title:String,
      description:String
    },
    mounted () {
        console.log("TabPaymentEntryMonthlyRevnue values............",this.values);
        console.log("TabPaymentEntryMonthlyRevnue metrics............",this.metrics[0]);
    }
  }
</script>