<template>
  <div class="container-fluid">
    <!-- <div>
      From
      <input type="date" v-model="state.startDate" format="yyyy-MM-dd" />
      To
      <input type="date" v-model="state.endDate" format="yyyy-MM-dd" />
    </div> -->
    <div>
      <datepicker v-model="startDate" format="yyyy-MM-dd"></datepicker
      >{{ startDate }}
      <datepicker v-model="endDate" format="yyyy-MM-dd"></datepicker
      >{{ endDate }}
    </div>
    <div class="row">
      <div class="col-sm-6">
        <query-builder :cubejs-api="cubejsApi" :query="TabSalesInvoiceRevnue">
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
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
    <!-- <div class="row">
      <div class="col-sm-4">
        <query-builder :cubejs-api="cubejsApi" :query="TabSalesInvoiceItemUniqueItemCode">
          <template v-slot="{loading, resultSet }">
            <Chart
              title="Tab Sales Invoice Item Unique Item Code Query 11"
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
              title="Tab Customer Count Query 10"
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
              title="Tab Sales Average Invoice Amount Query 5"
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
              title="Tab Bin pie Territory Query 4"
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
              title="Tab Bin pie Query"
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
              title="Tab Sales Customer Group Query 17  "
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
              title="Pie Sales Invoice By Status Query 20"
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
              title="Tab Sales Invoice Item Horizontal Bar Chart By Item Name Query 7"
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
              title="Tab Purchase Invoice Horizontal Bar Chart By Supplier Query 19"
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
              title="Tab Sales Invoice Item Horizontal Bar Chart By Item Group Query 8"
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
              title="Tab Customer Bar Chart By New Customer Query 13"
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
              title="Tab Sales Invoice Bar Chart By Sales Partner Query 14"
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
              title="Tab Bin Query"
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
              title="GuageChart Query 2"
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
              title="Tab Bin Item Code Wise Query 15"
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
              title="Tab Bin hand ware Wise Query 16"
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
              title="TabLeadByCityLocation Query 18"
              type="TabLeadByCityLocation"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
    </div> -->
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
  </div>
</template>

<script>
import cubejs from "@cubejs-client/core/dist/cubejs-client-core.esm";
import { QueryBuilder } from "@cubejs-client/vue";
import QUERY from "./components/Query.js";
import Chart from "./components/Chart.vue";
import { CUBE_JS_HOST, CUBE_JS_SECRET } from "../../../../../config.js";
import Datepicker from "vuejs-datepicker";
import Vue from "vue/dist/vue.js";

const cubejsApi = cubejs(CUBE_JS_SECRET, {
  apiUrl: CUBE_JS_HOST + "/cubejs-api/v1",
});

export default {
  name: "Home",
  components: {
    QUERY,
    Chart,
    QueryBuilder,
    Datepicker,
  },
  handleStartDate() {},
  data() {
    // var state = new Vue({
    //   data: {
    //     startDate: "2019-01-01",
    //     endDate: "2020-12-31",
    //   },
    // });
    var startDate = new Date("2019-01-01");
    var endDate = new Date("2020-12-31");
    let DateRange = "This Week";
    const dataObj = {
      cubejsApi,
      TabSalesInvoiceItemUniqueItemCode:
        QUERY.TabSalesInvoiceItemUniqueItemCode,
      TabCustomerCount: QUERY.TabCustomerCount,
      TabSalesAverageInvoiceAmount: QUERY.TabSalesAverageInvoiceAmount,
      tabBinPieTerritoryQuery: QUERY.tabBinPieTerritoryQuery,
      PieChartTerritory: QUERY.PieChartTerritory,
      TabSalesInvoiceItemHorizontalBarChartByItemName:
        QUERY.TabSalesInvoiceItemHorizontalBarChartByItemName,
      tabBinPieQuery: QUERY.tabBinPieQuery,
      TabCustomerBarChartByNewCustomer: QUERY.TabCustomerBarChartByNewCustomer,
      TabSalesInvoiceBarChartBySalesPartner:
        QUERY.TabSalesInvoiceBarChartBySalesPartner,
      TabSalesInvoiceCustomerGroup: QUERY.TabSalesInvoiceCustomerGroup,
      PieSalesInvoiceByStatus: QUERY.PieSalesInvoiceByStatus,
      TabSalesInvoiceItemHorizontalBarChartByItemGroup:
        QUERY.TabSalesInvoiceItemHorizontalBarChartByItemGroup,
      TabPurchaseInvoiceHorizontalBarChartBySupplier:
        QUERY.TabPurchaseInvoiceHorizontalBarChartBySupplier,
      tabBinQuery: QUERY.tabBinQuery,
      TabSalesInvoiceNetTotal: QUERY.TabSalesInvoiceNetTotal,
      TabBinItemCodeWise: QUERY.TabBinItemCodeWise,
      TabBinHandWareHouseWise: QUERY.TabBinHandWareHouseWise,
      TabLeadByCityLocation: QUERY.TabLeadByCityLocation,
      //Insight Engine Query
      TabPaymentEntryMonthlyRevnue: QUERY.TabPaymentEntryMonthlyRevnue,
      TabPaymentEntryWeeklyRevnue: QUERY.TabPaymentEntryWeeklyRevnue,
      TabSalesInvoiceItemConversionRatio:
        QUERY.TabSalesInvoiceItemConversionRatio,
      TabPaymentEntryMonthlyAverage: QUERY.TabPaymentEntryMonthlyAverage,
      TabPaymentEntryWeeklyAverage: QUERY.TabPaymentEntryWeeklyAverage,
      TabSalesInvoiceTrueCount: QUERY.TabSalesInvoiceTrueCount,
      TabSalesInvoiceItemTrueQty: QUERY.TabSalesInvoiceItemTrueQty,
      TabItemProductCount: QUERY.TabItemProductCount,
      // TabSalesInvoiceRevnue: QUERY.TabSalesInvoiceRevnue(state.startDate,state.endDate),
      // TabSalesInvoiceTopCustomerByRevenue:
      //   QUERY.TabSalesInvoiceTopCustomerByRevenue,
      // TabSalesInvoiceTopCustomerGroupByRevenue:
      //   QUERY.TabSalesInvoiceTopCustomerGroupByRevenue,
      // TabSalesInvoiceTopsalesPartnerByRevenue:
      //   QUERY.TabSalesInvoiceTopsalesPartnerByRevenue,
      // TabSalesInvoiceRevenueByTerritory:
      //   QUERY.TabSalesInvoiceRevenueByTerritory,
      // TabSalesInvoiceWeeklySales: QUERY.TabSalesInvoiceWeeklySales,
    };
    return { ...dataObj, startDate, endDate };
  },
  watch: {
    startDate: function () {
      console.log("change captured ......", this.startDate, this.endDate);
      this.dateRange();
    },
    endDate: function () {
      console.log(
        "change captured .end date.........",
        this.startDate,
        this.endDate
      );
      this.dateRange();
    },
    methods: {
      dateRange: function () {
        return {
          startDate: this.startDate,
          endDate: this.endDate,
        };
      },
    },
  },
  computed: {
    TabSalesInvoiceRevnue() {
      return QUERY.TabSalesInvoiceRevnue(this.startDate, this.endDate);
    },

    TabSalesInvoiceTopCustomerByRevenue() {
      return QUERY.TabSalesInvoiceTopCustomerByRevenue(
        this.startDate,
        this.endDate
      );
    },

    TabSalesInvoiceTopCustomerGroupByRevenue() {
      return QUERY.TabSalesInvoiceTopCustomerGroupByRevenue(
        this.startDate,
        this.endDate
      )
    },

    TabSalesInvoiceTopsalesPartnerByRevenue() {
      return QUERY.TabSalesInvoiceTopsalesPartnerByRevenue(
        this.startDate,
        this.endDate
      );
    },

    TabSalesInvoiceRevenueByTerritory() {
      return QUERY.TabSalesInvoiceRevenueByTerritory(
        this.startDate,
        this.endDate
      );
    },

    TabSalesInvoiceWeeklySales(){
      return QUERY.TabSalesInvoiceWeeklySales(
        this.startDate,
        this.endDate
      );
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
