<script>
  import { Pie } from 'vue-chartjs';
  import colour from "./colour";

  export default {
    name:"PieChart",
    props: {
      values: Array,
      metrics: Array,
    },
    extends: Pie,
    // computed:{
    //   color:function(){
    //     var letters = '0123456789ABCDEF';
    //     var colorArray=[];
    //     for(var j=0;j<5;j++){
    //       var col = '#';
    //       for (var i = 0; i < 6; i++) {
    //       col += letters[Math.floor(Math.random() * 16)];
    //       }
    //       colorArray.push(col);
    //     }
    //     return colorArray;
    //   }
    // },
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
              backgroundColor:colour,
              data: this.values.map(value=>value["TabBin.actualQty"]),
              hoverBackgroundColor:["#C98D69", "#E2B230", "#9DD59F", "#34BC4E", "#ECCF01"],
            }]
        },
        options: {
          legend: {
            display: true
          },
          cutoutPercentage:50,
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


