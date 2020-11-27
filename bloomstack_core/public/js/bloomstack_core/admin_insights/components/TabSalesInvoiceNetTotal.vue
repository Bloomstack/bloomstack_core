<template>
  <div>
    hello from TabSalesTotalInvoiceCount 
    <h1>{{this.values[0]["TabSalesInvoice.trueNetTotal"]}}</h1>
  </div>
</template>
<script>
  export default {
    name:"TabSalesInvoiceNetTotal",
    props: {
      values: Array,
      metrics: Array,
    },
    mounted () {
        // console.log("TabSalesTotalInvoiceCount............",this.values[0]["TabSalesInvoice.trueNetTotal"]);
    }
  };
</script>