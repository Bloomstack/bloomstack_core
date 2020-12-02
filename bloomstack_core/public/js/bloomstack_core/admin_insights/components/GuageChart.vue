<template>
  <div>
    <GChart
      :settings="{ packages: ['corechart', 'gauge'] }"
      type="Gauge"
      :data="chartData"
      :options="chartOptions"
    />
  </div>
</template>

<script>
// import { GChart } from "vue-google-charts";
export default {
  name: "GuageChart",
  components: {
    // GChart,
  },
  props: {
    values: Array,
    metrics: Array,
  },
  data() {
    return {
      // Array will be automatically processed with visualization.arrayToDataTable function
      chartData: [
        ["Label", "Value"],
        ["Net_Total", this.values[0]["TabSalesInvoice.trueNetTotal"]],
      ],
      chartOptions: {
        width: 400,
        height: 400,
        redFrom: 0,
        redTo: 200000,
        yellowFrom: 200000,
        yellowTo: 600000,
        greenFrom: 600000,
        greenTo: 1000000,
        minorTicks: 10,
        min: 0,
        max: 1000000,
        animation: {
          duration: 1000,
          easing: "out",
        },
      },
    };
  },
  mounted() {
    // console.log(this.values.map(value=>[value.category,value["TabBin.actualQty"]]))
  },
};
</script>
