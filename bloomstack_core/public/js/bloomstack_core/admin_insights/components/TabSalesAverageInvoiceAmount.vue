<template>
  <div>
    hello from TabSalesAverageInvoiceAmount 
    <h1>{{this.values[0]["TabSalesInvoice.AverageInvoiceAmount"]}}</h1>
  </div>
</template>
<script>
  export default {
    name:"TabSalesAverageInvoiceAmount",
    props: {
      values: Array,
      metrics: Array,
    },
    mounted () {
        // console.log("TabSalesAverageInvoiceAmount............",this.values[0]["TabSalesInvoice.AverageInvoiceAmount"]);
    }
  }
</script>