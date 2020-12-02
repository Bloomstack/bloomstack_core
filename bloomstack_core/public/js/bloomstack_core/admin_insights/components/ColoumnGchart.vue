<template>
  <div>
    <div class="section-heading">
      <p class="heading">
        {{ this.title }}
        <span> by Revenue </span>
      </p>
      <p class="period"></p>
    </div>
    <GChart type="ColumnChart" :data="chartData" :options="chartOptions" />
  </div>
</template>

<script>
// import { GChart } from "vue-google-charts";
import moment from "moment";

export default {
  name: "ColoumnGchart",
  components: {
    // GChart
  },
  props: {
    values: Array,
    metrics: Array,
    title: String,
    description: String,
    xname: String,
    yname: String,
  },
  data() {
    return {
      // Array will be automatically processed with visualization.arrayToDataTable function
      chartData: [
        [this.xname, this.yname],
        ...this.values.map((value, i, arr) => [value.category, value[this.metrics[0]]]),
      ],
      chartOptions: {
        chart: {
          title: "Company Performance",
          subtitle: "Sales, Expenses, and Profit: 2014-2017",
          isStacked: true,
        },
      },
    };
  },
  mounted() {
    // console.log("aaya data",this.values[8].category),
    // console.log("aaya data",this.values[8]["TabBin.actualQty"]),
    // console.log(this.values.map(value=>[value.category,value["TabBin.actualQty"]]))
  },
};
</script>
