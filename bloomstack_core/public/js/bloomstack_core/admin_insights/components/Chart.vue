<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">{{ title }}</h5>
      <div class="card-text">
        <div class="d-flex justify-content-center text-dark">
          <div class="spinner-border" role="status" v-if="loading">
            <span class="sr-only">Loading...</span>
          </div>
        </div>
        <h1
          v-if="!loading && type === 'number'"
          height="300"
        >{{ parseFloat(values?values[0][metrics[0]]:0).toLocaleString() }}</h1>
        <tab-sales-invoice-item-unique-item-code v-if="!loading && type === 'TabSalesInvoiceItemUniqueItemCode'" :values="values" :metrics="metrics" />
        <tab-customer-count v-if="!loading && type === 'TabCustomerCount'" :values="values" :metrics="metrics" />
        <tab-sales-average-invoice-amount v-if="!loading && type === 'TabSalesAverageInvoiceAmount'" :values="values" :metrics="metrics" />
        <pie-chart-territory v-if="!loading && type === 'pieChartTerritory'" :values="values" :metrics="metrics" />
        <!-- <pie-chart-customer-group v-if="!loading && type === 'test'" :values="values" :metrics="metrics" /> -->
      </div>
    </div>
  </div>
</template>

<script>
import moment from "moment";
import TabSalesInvoiceItemUniqueItemCode from "./TabSalesInvoiceItemUniqueItemCode.vue";
import TabCustomerCount from "./TabCustomerCount.vue";
import TabSalesAverageInvoiceAmount from "./TabSalesAverageInvoiceAmount.vue";
import PieChartTerritory from "./PieChartTerritory.vue";
// import PieChartCustomerGroup from "./PieChartCustomerGroup.vue";
export default {
  components: {
    TabSalesInvoiceItemUniqueItemCode,
    TabCustomerCount,
    TabSalesAverageInvoiceAmount,
    PieChartTerritory,
    // PieChartCustomerGroup
  },
  name: "Chart",
  props: {
    resultSet: Object,
    loading: Boolean,
    title: String,
    type: String,
  },
  methods: {
    dateFormatter: function (value) {
      return moment(value).format("MMM YY");
    },
  },
  computed: {
    values: function () {
      if (this.loading) return [];
      console.log("qqqqq77777q....", this.loading, this.title, this.resultSet);
      return this.resultSet ? this.resultSet.chartPivot() : [];
    },
    metrics: function () {
      if (this.loading) return [""];
      // console.log("asaasss....", this.loading, this.title, this.type);
      return this.resultSet
        ? this.resultSet.seriesNames().map((x) => x.key)
        : [];
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
};
</script>

<style scoped>
</style>
