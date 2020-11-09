<script>
  import { HorizontalBar } from 'vue-chartjs';
  import colour from "./colour";


  export default {
    name:"TabSalesInvoiceItemHorizontalBarChartByItemName",
    props: {
    values: Array,
    metrics: Array,
    },
    extends: HorizontalBar,
    data() {
      return {
        chartData: {
          labels: this.values.map(value=>value.category),
          datasets: [{
            label: 'HorizontalBar',
            borderWidth: 1,
            backgroundColor: colour,
            borderColor: colour,
            pointBorderColor: '#2554FF',
            data:this.values.map(value=>value["TabSalesInvoiceItem.amount"])
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
      this.renderChart(this.chartData, this.options)
    }
  }
</script>