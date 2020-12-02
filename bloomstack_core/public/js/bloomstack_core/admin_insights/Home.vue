<template>
  <div class="container-fluid">
    <div style="display: flex">
      From
      <datepicker v-model="startDate" format="dd-MM-yyyy"></datepicker>
      To
      <datepicker v-model="endDate" format="dd-MM-yyyy"></datepicker>
      <select
        v-model="selectedDateRange"
        id="dateRangeSelect"
        :key="selectedDateRange.value"
      >
        <option v-for="dateRange in dateRangevalue" :value="dateRange" v-bind:key="dateRange.value">
          {{ dateRange.text }}
        </option>
      </select>
    </div>
    <div class="row">
      <div class="col-sm-5">
        <query-builder
          :cubejs-api="cubejsApi"
          :query="tabPaymentEntryMonthlyRevnue"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="tabPaymentEntryMonthlyRevnue"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
      <div class="col-sm-3">
        <query-builder
          :cubejs-api="cubejsApi"
          :query="tabPaymentEntryWeeklyRevnue"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="tabPaymentEntryWeeklyRevnue"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
      <div class="col-sm-4">
        <query-builder
          :cubejs-api="cubejsApi"
          :query="tabSalesInvoiceItemConversionRatio"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="tabSalesInvoiceItemConversionRatio"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-4">
        <query-builder
          :cubejs-api="cubejsApi"
          :query="tabPaymentEntryMonthlyAverage"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="tabPaymentEntryMonthlyAverage"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
      <div class="col-sm-4">
        <query-builder
          :cubejs-api="cubejsApi"
          :query="tabPaymentEntryWeeklyAverage"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="tabPaymentEntryWeeklyAverage"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
      <div class="col-sm-4">
        <query-builder
          :cubejs-api="cubejsApi"
          :query="tabSalesInvoiceTrueCount"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="tabSalesInvoiceTrueCount"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-4">
        <query-builder
          :cubejs-api="cubejsApi"
          :query="tabSalesInvoiceItemTrueQty"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="tabSalesInvoiceItemTrueQty"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
      <div class="col-sm-4">
        <query-builder :cubejs-api="cubejsApi" :query="tabItemProductCount">
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="tabItemProductCount"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-6">
        <query-builder :cubejs-api="cubejsApi" :query="tabSalesInvoiceRevnue">
          <template v-slot="{ loading, resultSet }">
            <Chart
              type="tabSalesInvoiceRevnue"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
      <div class="col-sm-6">
        <query-builder :cubejs-api="cubejsApi" :query="tabSalesInvoiceRevnue">
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="tabSalesInvoiceCummulativeRevnue"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-6">
        <query-builder
          :cubejs-api="cubejsApi"
          :query="tabSalesInvoiceTopCustomerByRevenue"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="tabSalesInvoiceTopCustomerByRevenue"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
      <div class="col-sm-6">
        <query-builder
          :cubejs-api="cubejsApi"
          :query="tabSalesInvoiceTopCustomerGroupByRevenue"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="tabSalesInvoiceTopCustomerGroupByRevenue"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-6">
        <query-builder
          :cubejs-api="cubejsApi"
          :query="tabSalesInvoiceTopsalesPartnerByRevenue"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="tabSalesInvoiceTopsalesPartnerByRevenue"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-6">
        <query-builder
          :cubejs-api="cubejsApi"
          :query="tabSalesInvoiceRevenueByTerritory"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="tabSalesInvoiceRevenueByTerritory"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-12">
        <query-builder
          :cubejs-api="cubejsApi"
          :query="tabSalesInvoiceWeeklySales"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="tabSalesInvoiceWeeklySales"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
    </div>
  </div>
</template>

<script>
import cubejs from "@cubejs-client/core/dist/cubejs-client-core.esm";
import { QueryBuilder } from "@cubejs-client/vue";
import Query from "./components/Query.js";
import Chart from "./components/Chart.vue";
import Datepicker from "vuejs-datepicker";
import Vue from "vue/dist/vue.js";

export default {
  name: "Home",
  props: {
    config: Object,
  },
  components: {
    Query,
    Chart,
    QueryBuilder,
    Datepicker,
  },
  data() {
    var startDate = new Date("2019-01-01");
    var endDate = new Date("2020-12-31");
    const cubejsApi = cubejs(this.config.CubeJsSecret, {
      apiUrl: this.config.CubeJsHost + "/cubejs-api/v1",
    });
    let selectedDateRange = { value: 1, text: null };
    const dataObj = {
      cubejsApi,
      dateRangevalue: [
        { value: 2, text: "Today" },
        { value: 3, text: "Yesterday" },
        { value: 4, text: "This week" },
        { value: 5, text: "This quarter" },
        { value: 6, text: "This year" },
        { value: 7, text: "Last 7 days" },
        { value: 8, text: "Last 30 days" },
        { value: 9, text: "Last week" },
        { value: 10, text: "Last month" },
        { value: 11, text: "Last quarter" },
        { value: 12, text: "Last year" },
      ],
      TabSalesInvoiceItemUniqueItemCode:
        Query.TabSalesInvoiceItemUniqueItemCode,
      TabCustomerCount: Query.TabCustomerCount,
      TabSalesAverageInvoiceAmount: Query.TabSalesAverageInvoiceAmount,
      tabBinPieTerritoryQuery: Query.tabBinPieTerritoryQuery,
      PieChartTerritory: Query.PieChartTerritory,
      TabSalesInvoiceItemHorizontalBarChartByItemName:
        Query.TabSalesInvoiceItemHorizontalBarChartByItemName,
      tabBinPieQuery: Query.tabBinPieQuery,
      TabCustomerBarChartByNewCustomer: Query.TabCustomerBarChartByNewCustomer,
      TabSalesInvoiceBarChartBySalesPartner:
        Query.TabSalesInvoiceBarChartBySalesPartner,
      TabSalesInvoiceCustomerGroup: Query.TabSalesInvoiceCustomerGroup,
      PieSalesInvoiceByStatus: Query.PieSalesInvoiceByStatus,
      TabSalesInvoiceItemHorizontalBarChartByItemGroup:
        Query.TabSalesInvoiceItemHorizontalBarChartByItemGroup,
      TabPurchaseInvoiceHorizontalBarChartBySupplier:
        Query.TabPurchaseInvoiceHorizontalBarChartBySupplier,
      tabBinQuery: Query.tabBinQuery,
      TabSalesInvoiceNetTotal: Query.TabSalesInvoiceNetTotal,
      TabBinItemCodeWise: Query.TabBinItemCodeWise,
      TabBinHandWareHouseWise: Query.TabBinHandWareHouseWise,
      TabLeadByCityLocation: Query.TabLeadByCityLocation,
    };
    return { ...dataObj, startDate, endDate, selectedDateRange };
  },
  watch: {
    startDate () {
      this.selectedDateRange = { value: 0, text: null };
      this.dateRange();
    },
    endDate () {
      this.selectedDateRange = { value: 0, text: null };
      this.dateRange();
    },
    methods: {
      dateRange () {
        return {
          startDate: this.startDate,
          endDate: this.endDate,
        };
      },
    },
  },
  computed: {
    tabSalesInvoiceRevnue() {
      return Query.tabSalesInvoiceRevnue(
        this.startDate,
        this.endDate,
        this.selectedDateRange.text
      );
    },

    tabSalesInvoiceTopCustomerByRevenue() {
      return Query.tabSalesInvoiceTopCustomerByRevenue(
        this.startDate,
        this.endDate,
        this.selectedDateRange.text
      );
    },

    tabSalesInvoiceTopCustomerGroupByRevenue() {
      return Query.tabSalesInvoiceTopCustomerGroupByRevenue(
        this.startDate,
        this.endDate,
        this.selectedDateRange.text
      );
    },

    tabSalesInvoiceTopsalesPartnerByRevenue() {
      return Query.tabSalesInvoiceTopsalesPartnerByRevenue(
        this.startDate,
        this.endDate,
        this.selectedDateRange.text
      );
    },

    tabSalesInvoiceRevenueByTerritory() {
      return Query.tabSalesInvoiceRevenueByTerritory(
        this.startDate,
        this.endDate,
        this.selectedDateRange.text

      );
    },

    tabSalesInvoiceWeeklySales() {
      return Query.tabSalesInvoiceWeeklySales(this.startDate, this.endDate,this.selectedDateRange.text);
    },
    tabItemProductCount() {
      return Query.tabItemProductCount;
    },

    tabSalesInvoiceItemTrueQty() {
      return Query.tabSalesInvoiceItemTrueQty;
    },

    tabSalesInvoiceTrueCount() {
      return Query.tabSalesInvoiceTrueCount;
    },

    tabPaymentEntryWeeklyAverage() {
      return Query.tabPaymentEntryWeeklyAverage;
    },

    tabPaymentEntryMonthlyAverage(){
      return Query.tabPaymentEntryMonthlyAverage;
    },

    tabSalesInvoiceItemConversionRatio(){
      return Query.tabSalesInvoiceItemConversionRatio;
    },

    tabPaymentEntryWeeklyRevnue(){
      return Query.tabPaymentEntryWeeklyRevnue;
    },

    tabPaymentEntryMonthlyRevnue(){
      return Query.tabPaymentEntryMonthlyRevnue;
    }
  },
};
</script>

<style>
html {
  -webkit-font-smoothing: antialiased;
}

body {
  padding-top: 30px;
  padding-bottom: 30px;
  background: #f5f6f7;
}
</style>
