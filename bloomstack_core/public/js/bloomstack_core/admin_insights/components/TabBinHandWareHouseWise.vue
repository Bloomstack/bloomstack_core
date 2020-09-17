<template>
  <div>
    <GChart
      :settings="{ packages: ['corechart', 'table'] }"
      type="Table"
      :data="chartData"
      :options="chartOptions"
    />    
  </div>
</template>

<script>
import { GChart } from "vue-google-charts";
export default {
  name: "TabBinHandWareHouseWise",
  components: {
    GChart
  },
  props: {
      values: Array,
      metrics: Array,
   },
  data() {
    return {
      // Array will be automatically processed with visualization.arrayToDataTable function
      chartData:[
          ["Ware House", "Actual Quantity"],
          ...this.values.map(value=>[value.category,value["TabBin.actualQty"]])
  
      ],
      chartOptions: {
        chart: {
          title: "Company Performance",
          subtitle: "Sales, Expenses, and Profit: 2014-2017",
          isStacked: true
            }
        }
    };
  },
  mounted (){
      // console.log(this.values.map(value=>[value.category,value["TabBin.actualQty"]]))
  }
};
</script>
