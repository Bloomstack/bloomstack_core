<!--
<template>
  <la-cartesian autoresize narrow stacked :data="values" :colors="colors" :padding="[0, 0, 5, 0]">
    <template v-for="metric in metrics">
      <la-bar :prop="metric" v-bind:key="metric" :width="6" :label="metric.split(',')[0]"></la-bar>
    </template>
    <la-y-axis :nbTicks="2"></la-y-axis>
    <la-x-axis prop="x" :format="dateFormatter" :interval="6"></la-x-axis>
    <la-tooltip />
  </la-cartesian>
</template>

<script>
import moment from "moment";
export default {
  name: "LineChart",
  props: {
    values: Array,
    metrics: Array,
  },
  methods: {
    dateFormatter: function (value) {
      return moment(value).format("MMM YY");
    },
  },
  data() {
    return {
      colors: [
        "#7DB3FF",
        "#49457B",
        "#FF7C78",
        "#FED3D0",
        "#6F76D9",
        "#9ADFB4",
        "#2E7987",
      ],
    };
  },
  mounted(){
    console.log("Bar Chart values",this.values),
    console.log("BarChart metrics",this.metrics)
  }
};
</script>

<style scoped>
</style>
  
-->
<script>
  import { Bar } from "vue-chartjs";
  import colour from "./colour";


  export default {
    name:"BarChart",
    props: {
    values: Array,
    metrics: Array,
    },
    extends: Bar,
    data() {
      return {
        chartData: {
          labels: this.values.map((value) => value.category),
          datasets: [{
            label: "Bar Chart",
            borderWidth: 1,
            backgroundColor: colour,
            borderColor: colour,
            pointBorderColor: "#2554FF",
            data:this.values.map((value) => value["TabBin.actualQty"])
          }]
        },
        options: {
          scales: {
            yAxes: [{
              ticks: {
                beginAtZero: true
              },
              gridLines: {
                display: true
              }
            }],
            xAxes: [{
              gridLines: {
                display: false
              }
            }]
          },
          legend: {
            display: true
          },
          responsive: true,
          maintainAspectRatio: false
        }
      }
    },
    mounted() {
      this.renderChart(this.chartData, this.options);
    }
  }
</script>