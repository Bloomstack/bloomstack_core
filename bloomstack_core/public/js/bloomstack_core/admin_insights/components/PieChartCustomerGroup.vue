<script>
  import { Pie } from 'vue-chartjs'

  export default {
    name:"PieChartCustomerGroup",
    props: {
      values: Array,
      metrics: Array,
    },
    extends: Pie,
    data () {
      return {
        chartData: {
          labels: this.values.map(value=>value.category),
          datasets: [{
              borderWidth: 1,
              borderColor: [
              'rgba(255,99,132,1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)'            
              ],
              backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',                
              ],
              data: this.values.map(value=>value["TabSalesInvoice.netTotal"])
            }]
        },
        options: {
          legend: {
            display: true
          },
          responsive: true,
          maintainAspectRatio: false
        }
      }
    },
    mounted () {
      this.renderChart(this.chartData, this.options)
    }
  }
</script>

