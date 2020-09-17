<template>
  <div>
    <GChart
      :settings="{ packages: ['corechart', 'geochart'] }"
      type="GeoChart"
      :data="chartData"
      :options="chartOptions"
    />    
  </div>
</template>

<script>
import { GChart } from "vue-google-charts";
export default {
  name: "TabLeadByCityLocation",
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
          ['Country', 'Popularity'],
          ['Germany', 200],
          ['United States', 300],
          ['Brazil', 400],
          ['Canada', 500],
          ['France', 600], 
          ['RU', 700],
          ["MUMBAI",340], 
          ...this.values.map(value=>[value.category,value["TabLead.count"]])

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
      console.log(this.values.map(value=>[value.category,value["TabLead.count"]]))
  }
};
</script>
