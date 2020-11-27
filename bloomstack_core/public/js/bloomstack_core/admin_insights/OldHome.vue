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
    <!-- <div class="row">
      <div class="col-sm-4">
        <query-builder :cubejs-api="cubejsApi" :query="TabSalesInvoiceItemUniqueItemCode">
          <template v-slot="{loading, resultSet }">
            <Chart
              title="Tab Sales Invoice Item Unique Item Code query 11"
              type="TabSalesInvoiceItemUniqueItemCode"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
      <div class="col-sm-4">
        <query-builder :cubejs-api="cubejsApi" :query="TabCustomerCount">
          <template v-slot="{loading, resultSet }">
            <Chart
              title="Tab Customer Count query 10"
              type="TabCustomerCount"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
      <div class="col-sm-4">
        <query-builder :cubejs-api="cubejsApi" :query="TabSalesAverageInvoiceAmount">
          <template v-slot="{loading, resultSet }">
            <Chart
              title="Tab Sales Average Invoice Amount query 5"
              type="TabSalesAverageInvoiceAmount"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-6">
        <query-builder :cubejs-api="cubejsApi" :query="tabBinPieTerritoryQuery">
          <template v-slot="{loading, resultSet }">
            <Chart
              title="Tab Bin pie Territory query 4"
              type="pieChartTerritory"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
      <div class="col-sm-6">
        <query-builder :cubejs-api="cubejsApi" :query="tabBinPieQuery">
          <template v-slot="{loading, resultSet }">
            <Chart
              title="Tab Bin pie query"
              type="pieChart"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-6">
        <query-builder :cubejs-api="cubejsApi" :query="TabSalesInvoiceCustomerGroup">
          <template v-slot="{loading, resultSet }">
            <Chart
              title="Tab Sales Customer Group query 17  "
              type="pieChartCustomerGroup"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
      <div class="col-sm-6">
        <query-builder :cubejs-api="cubejsApi" :query="PieSalesInvoiceByStatus">
          <template v-slot="{loading, resultSet }">
            <Chart
              title="Pie Sales Invoice By Status query 20"
              type="PieSalesInvoiceByStatus"
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
          :query="TabSalesInvoiceItemHorizontalBarChartByItemName"
        >
          <template v-slot="{loading, resultSet }">
            <Chart
              title="Tab Sales Invoice Item Horizontal Bar Chart By Item Name query 7"
              type="TabSalesInvoiceItemHorizontalBarChartByItemName"
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
          :query="TabPurchaseInvoiceHorizontalBarChartBySupplier"
        >
          <template v-slot="{loading, resultSet }">
            <Chart
              title="Tab Purchase Invoice Horizontal Bar Chart By Supplier query 19"
              type="TabPurchaseInvoiceHorizontalBarChartBySupplier"
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
          :query="TabSalesInvoiceItemHorizontalBarChartByItemGroup"
        >
          <template v-slot="{loading, resultSet }">
            <Chart
              title="Tab Sales Invoice Item Horizontal Bar Chart By Item Group query 8"
              type="TabSalesInvoiceItemHorizontalBarChartByItemGroup"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-12">
        <query-builder :cubejs-api="cubejsApi" :query="TabCustomerBarChartByNewCustomer">
          <template v-slot="{ loading, resultSet }">
            <Chart
              title="Tab Customer Bar Chart By New Customer query 13"
              type="TabCustomerBarChartByNewCustomer"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-12">
        <query-builder :cubejs-api="cubejsApi" :query="TabSalesInvoiceBarChartBySalesPartner">
          <template v-slot="{ loading, resultSet }">
            <Chart
              title="Tab Sales Invoice Bar Chart By Sales Partner query 14"
              type="TabSalesInvoiceBarChartBySalesPartner"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-12">
        <query-builder :cubejs-api="cubejsApi" :query="tabBinQuery">
          <template v-slot="{ loading, resultSet }">
            <Chart
              title="Tab Bin query"
              type="stackedBar"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-12">
        <query-builder :cubejs-api="cubejsApi" :query="TabSalesInvoiceNetTotal">
          <template v-slot="{ loading, resultSet }">
            <Chart
              title="GuageChart query 2"
              type="GuageChart"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-6">
        <query-builder :cubejs-api="cubejsApi" :query="TabBinItemCodeWise">
          <template v-slot="{loading, resultSet }">
            <Chart
              title="Tab Bin Item Code Wise query 15"
              type="TabBinItemCodeWise"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
      <div class="col-sm-6">
        <query-builder :cubejs-api="cubejsApi" :query="TabBinHandWareHouseWise">
          <template v-slot="{loading, resultSet }">
            <Chart
              title="Tab Bin hand ware Wise query 16"
              type="TabBinHandWareHouseWise"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
    </div> 
    <div class="row">
      <div class="col-sm-12">
        <query-builder :cubejs-api="cubejsApi" :query="TabLeadByCityLocation">
          <template v-slot="{loading, resultSet }">
            <Chart
              title="TabLeadByCityLocation query 18"
              type="TabLeadByCityLocation"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
    </div> -->
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