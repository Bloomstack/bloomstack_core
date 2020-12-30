<template>
  <div class="row">
    <div class="col-md-6 col-xs-12 right-chart">
      <div class="section-heading">
        <p class="heading">
          {{ this.title }}
          <span> by cummulative </span>
        </p>
        <p class="period">Year-to-Date</p>
      </div>
      <GChart type="LineChart" :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script>
// import { GChart } from "vue-google-charts";
import moment from "moment";

export default {
  name: "LineCummulativeGchart",
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
        ...this.values.map(
          (value, i, arr) => [
            moment(value.category).format("MMM YYYY"),
            (arr[parseInt(i)][this.metrics[0]] += arr[parseInt(i) - 1]
              ? arr[parseInt(i) - 1][this.metrics[0]]
              : 0),
          ]
          // if(i>0){
          // return [moment(value.category).format("MMM YYYY"),arr[i][this.metrics[0]]+arr[i-1][this.metrics[0]]]
          // }else{
          // return [moment(value.category).format("MMM YYYY"),arr[i][this.metrics[0]]]
          // }
        ),
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
  mounted() {},
};
</script>
