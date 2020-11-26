<template>
  <div>
    <GChart
      type="Table"
      :data="chartData"
      :options="chartOptions"
    />    
  </div>
</template>

<script>
// import { GChart } from "vue-google-charts";
export default {
  name: "TabBinItemCodeWise",
  components: {
    // GChart
  },
  props: {
      values: Array,
      metrics: Array,
   },
  data() {
    return {
      // Array will be automatically processed with visualization.arrayToDataTable function
      chartData:[
          ["Item Code", "ActualQuantity"],
          ...this.values.map((value) => [value.category,value[this.metrics[0]]])
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
      // console.log("aaya data",this.values[8].category),
      // console.log("aaya data",this.values[8]["TabBin.actualQty"]),
      // console.log(this.values.map(value=>[value.category,value["TabBin.actualQty"]]))
  }
};
</script>
