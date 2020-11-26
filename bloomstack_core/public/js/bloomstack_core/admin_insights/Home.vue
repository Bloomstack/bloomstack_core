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
          :query="TabPaymentEntryMonthlyRevnue"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="TabPaymentEntryMonthlyRevnue"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
      <div class="col-sm-3">
        <query-builder
          :cubejs-api="cubejsApi"
          :query="TabPaymentEntryWeeklyRevnue"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="TabPaymentEntryWeeklyRevnue"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
      <div class="col-sm-4">
        <query-builder
          :cubejs-api="cubejsApi"
          :query="TabSalesInvoiceItemConversionRatio"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="TabSalesInvoiceItemConversionRatio"
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
          :query="TabPaymentEntryMonthlyAverage"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="TabPaymentEntryMonthlyAverage"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
      <div class="col-sm-4">
        <query-builder
          :cubejs-api="cubejsApi"
          :query="TabPaymentEntryWeeklyAverage"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="TabPaymentEntryWeeklyAverage"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
      <div class="col-sm-4">
        <query-builder
          :cubejs-api="cubejsApi"
          :query="TabSalesInvoiceTrueCount"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="TabSalesInvoiceTrueCount"
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
          :query="TabSalesInvoiceItemTrueQty"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="TabSalesInvoiceItemTrueQty"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
      <div class="col-sm-4">
        <query-builder :cubejs-api="cubejsApi" :query="TabItemProductCount">
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="TabItemProductCount"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-6">
        <query-builder :cubejs-api="cubejsApi" :query="TabSalesInvoiceRevnue">
          <template v-slot="{ loading, resultSet }">
            <Chart
              type="TabSalesInvoiceRevnue"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
      <div class="col-sm-6">
        <query-builder :cubejs-api="cubejsApi" :query="TabSalesInvoiceRevnue">
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="TabSalesInvoiceCummulativeRevnue"
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
          :query="TabSalesInvoiceTopCustomerByRevenue"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="TabSalesInvoiceTopCustomerByRevenue"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
      <div class="col-sm-6">
        <query-builder
          :cubejs-api="cubejsApi"
          :query="TabSalesInvoiceTopCustomerGroupByRevenue"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="TabSalesInvoiceTopCustomerGroupByRevenue"
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
          :query="TabSalesInvoiceTopsalesPartnerByRevenue"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="TabSalesInvoiceTopsalesPartnerByRevenue"
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
          :query="TabSalesInvoiceRevenueByTerritory"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="TabSalesInvoiceRevenueByTerritory"
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
          :query="TabSalesInvoiceWeeklySales"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              type="TabSalesInvoiceWeeklySales"
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
import query from "./components/Query.js";
import Chart from "./components/Chart.vue";
import Datepicker from "vuejs-datepicker";
import Vue from "vue/dist/vue.js";

export default {
  name: "Home",
  props: {
    config: Object,
  },
  components: {
    query,
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
        query.TabSalesInvoiceItemUniqueItemCode,
      TabCustomerCount: query.TabCustomerCount,
      TabSalesAverageInvoiceAmount: query.TabSalesAverageInvoiceAmount,
      tabBinPieTerritoryQuery: query.tabBinPieTerritoryQuery,
      PieChartTerritory: query.PieChartTerritory,
      TabSalesInvoiceItemHorizontalBarChartByItemName:
        query.TabSalesInvoiceItemHorizontalBarChartByItemName,
      tabBinPieQuery: query.tabBinPieQuery,
      TabCustomerBarChartByNewCustomer: query.TabCustomerBarChartByNewCustomer,
      TabSalesInvoiceBarChartBySalesPartner:
        query.TabSalesInvoiceBarChartBySalesPartner,
      TabSalesInvoiceCustomerGroup: query.TabSalesInvoiceCustomerGroup,
      PieSalesInvoiceByStatus: query.PieSalesInvoiceByStatus,
      TabSalesInvoiceItemHorizontalBarChartByItemGroup:
        query.TabSalesInvoiceItemHorizontalBarChartByItemGroup,
      TabPurchaseInvoiceHorizontalBarChartBySupplier:
        query.TabPurchaseInvoiceHorizontalBarChartBySupplier,
      tabBinQuery: query.tabBinQuery,
      TabSalesInvoiceNetTotal: query.TabSalesInvoiceNetTotal,
      TabBinItemCodeWise: query.TabBinItemCodeWise,
      TabBinHandWareHouseWise: query.TabBinHandWareHouseWise,
      TabLeadByCityLocation: query.TabLeadByCityLocation,
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
    TabSalesInvoiceRevnue() {
      return query.TabSalesInvoiceRevnue(
        this.startDate,
        this.endDate,
        this.selectedDateRange.text
      );
    },

    TabSalesInvoiceTopCustomerByRevenue() {
      return query.TabSalesInvoiceTopCustomerByRevenue(
        this.startDate,
        this.endDate,
        this.selectedDateRange.text
      );
    },

    TabSalesInvoiceTopCustomerGroupByRevenue() {
      return query.TabSalesInvoiceTopCustomerGroupByRevenue(
        this.startDate,
        this.endDate,
        this.selectedDateRange.text
      );
    },

    TabSalesInvoiceTopsalesPartnerByRevenue() {
      return query.TabSalesInvoiceTopsalesPartnerByRevenue(
        this.startDate,
        this.endDate,
        this.selectedDateRange.text
      );
    },

    TabSalesInvoiceRevenueByTerritory() {
      return query.TabSalesInvoiceRevenueByTerritory(
        this.startDate,
        this.endDate,
        this.selectedDateRange.text

      );
    },

    TabSalesInvoiceWeeklySales() {
      return query.TabSalesInvoiceWeeklySales(this.startDate, this.endDate,this.selectedDateRange.text);
    },
    TabItemProductCount() {
      return query.TabItemProductCount;
    },

    TabSalesInvoiceItemTrueQty() {
      return query.TabSalesInvoiceItemTrueQty;
    },

    TabSalesInvoiceTrueCount() {
      return query.TabSalesInvoiceTrueCount;
    },

    TabPaymentEntryWeeklyAverage() {
      return query.TabPaymentEntryWeeklyAverage;
    },

    TabPaymentEntryMonthlyAverage(){
      return query.TabPaymentEntryMonthlyAverage;
    },

    TabSalesInvoiceItemConversionRatio(){
      return query.TabSalesInvoiceItemConversionRatio;
    },

    TabPaymentEntryWeeklyRevnue(){
      return query.TabPaymentEntryWeeklyRevnue;
    },

    TabPaymentEntryMonthlyRevnue(){
      return query.TabPaymentEntryMonthlyRevnue;
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
