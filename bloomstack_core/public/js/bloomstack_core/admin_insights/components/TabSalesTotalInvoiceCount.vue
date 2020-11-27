<template>
  <div>
    hello from TabSalesTotalInvoiceCount 
    </br>
    <h1>{{this.values[0]["TabSalesInvoice.count"]}}</h1>
  </div>
</template>
<script>
  export default {
    name:"TabSalesTotalInvoiceCount",
    props: {
      values: Array,
      metrics: Array,
    },
    mounted () {
        // console.log("TabSalesTotalInvoiceCount............",this.values[0]["TabSalesInvoice.trueCount"]);
    }
  };
</script>