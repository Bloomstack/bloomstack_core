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
        <pie-chart v-if="!loading && type === 'pieChart'" :values="values" :metrics="metrics" />
        <tab-sales-invoice-item-horizontal-bar-chart-by-item-name v-if="!loading && type === 'TabSalesInvoiceItemHorizontalBarChartByItemName'" :values="values" :metrics="metrics" />
        <tab-sales-invoice-item-horizontal-bar-chart-by-item-group v-if="!loading && type === 'TabSalesInvoiceItemHorizontalBarChartByItemGroup'" :values="values" :metrics="metrics" />
        <tab-purchase-invoice-horizontal-bar-chart-by-supplier v-if="!loading && type === 'TabPurchaseInvoiceHorizontalBarChartBySupplier'" :values="values" :metrics="metrics" />
        <tab-customer-bar-chart-by-new-customer v-if="!loading && type === 'TabCustomerBarChartByNewCustomer'" :values="values" :metrics="metrics" />
        <tab-sales-invoice-bar-chart-by-sales-partner v-if="!loading && type === 'TabSalesInvoiceBarChartBySalesPartner'" :values="values" :metrics="metrics" />
        <pie-chart-customer-group v-if="!loading && type === 'pieChartCustomerGroup'" :values="values" :metrics="metrics" />
        <pie-sales-invoice-by-status v-if="!loading && type === 'PieSalesInvoiceByStatus'" :values="values" :metrics="metrics" />
        <bar-chart v-if="!loading && type === 'stackedBar'" :values="values" :metrics="metrics" />
        <!-- <guage-chart v-if="!loading && type === 'GuageChart'" :values="values" :metrics="metrics" /> -->

      </div>
    </div>
  </div>
</template>

<script>
import moment from "moment";
import BarChart from "./BarChart.vue";
import TabSalesInvoiceItemUniqueItemCode from "./TabSalesInvoiceItemUniqueItemCode.vue";
import TabCustomerCount from "./TabCustomerCount.vue";
import TabSalesAverageInvoiceAmount from "./TabSalesAverageInvoiceAmount.vue";
import PieChartTerritory from "./PieChartTerritory.vue";
import TabSalesInvoiceItemHorizontalBarChartByItemName from "./TabSalesInvoiceItemHorizontalBarChartByItemName.vue";
import PieChart from "./PieChart.vue";
import TabCustomerBarChartByNewCustomer from "./TabCustomerBarChartByNewCustomer.vue";
import TabSalesInvoiceBarChartBySalesPartner from "./TabSalesInvoiceBarChartBySalesPartner.vue";
import pieChartCustomerGroup from "./PieChartCustomerGroup.vue";
import PieSalesInvoiceByStatus from "./PieSalesInvoiceByStatus.vue";
import TabSalesInvoiceItemHorizontalBarChartByItemGroup from "./TabSalesInvoiceItemHorizontalBarChartByItemGroup.vue";
import TabPurchaseInvoiceHorizontalBarChartBySupplier from "./TabPurchaseInvoiceHorizontalBarChartBySupplier.vue";
import BarChartVue from './BarChart.vue';
// import GuageChart from "./GuageChart.vue";
export default {
  components: {
    BarChart,
    TabSalesInvoiceItemUniqueItemCode,
    TabCustomerCount,
    TabSalesAverageInvoiceAmount,
    PieChartTerritory,
    PieChart,
    TabSalesInvoiceItemHorizontalBarChartByItemName,
    TabCustomerBarChartByNewCustomer,
    TabSalesInvoiceBarChartBySalesPartner,
    pieChartCustomerGroup,
    PieSalesInvoiceByStatus,
    TabSalesInvoiceItemHorizontalBarChartByItemGroup,
    TabPurchaseInvoiceHorizontalBarChartBySupplier,
    // GuageChart
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
