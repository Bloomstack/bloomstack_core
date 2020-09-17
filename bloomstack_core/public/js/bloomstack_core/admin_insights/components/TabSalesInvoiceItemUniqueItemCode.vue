<template>
  <div>
    hello from TabSalesInvoiceItemUniqueItemCode 
    </br>
    <h1>{{this.values[0]["TabSalesInvoiceItem.itemCodeCount"]}}</h1>
  </div>
</template>
<script>
  export default {
    name:"TabSalesInvoiceItemUniqueItemCode",
    props: {
      values: Array,
      metrics: Array,
    },
    mounted () {
        console.log("TabSalesInvoiceItemUniqueItemCode............",this.values[0]["TabSalesInvoiceItem.itemCodeCount"]);
    }
  }
</script>