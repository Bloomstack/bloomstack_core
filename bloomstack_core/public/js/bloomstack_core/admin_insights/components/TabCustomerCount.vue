<template>
  <div>
    hello from TabCustomerCount 
    </br>
    <h1>{{this.values[0]["TabCustomer.countName"]}}</h1>
  </div>
</template>
<script>
  export default {
    name:"TabCustomerCount",
    props: {
      values: Array,
      metrics: Array,
    },
    mounted () {
        console.log("TabSalesAverageInvoiceAmount............",this.values[0]["TabCustomer.countName"]);
    }
  }
</script>