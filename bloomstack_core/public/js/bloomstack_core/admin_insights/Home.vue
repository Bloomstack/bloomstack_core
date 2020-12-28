<template>
  <div class="average-cards">
    <div v-for="card in cardRenderer" :key="card.id">
      <div class="col-sm-4">
        <query-builder
          :cubejs-api="cubejsApi"
          :query=card.query>
          <template v-slot="{ loading, resultSet}">
            <Chart
              title="test data change"
              :type=card.type
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
    </div>
    <div class="average-cards">
      <div class="row"><div class="sub-title-text">Average Cards</div></div>
      <div class="col-sm-4">
        <query-builder
          :cubejs-api="cubejsApi"
          :query="TabPaymentEntryMonthlyRevnue"
        >
          <template v-slot="{ loading, resultSet }">
            <Chart
              title="test data"
              type="TabPaymentEntryMonthlyRevnue"
              :loading="loading"
              :result-set="resultSet"
            />
          </template>
        </query-builder>
      </div>
      <div class="col-sm-4">
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
    <div class="graphs">
      <div class="sub-title-text">Graphs</div>
      <div class="row">
        <div class="col-sm-4">
          Start Date:<datepicker v-model="startDate"></datepicker>
        </div>
        <div class="col-sm-4">
          End Date:<datepicker v-model="endDate"></datepicker>
        </div>
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
  </div>
</template>

<script>
import cubejs from "@cubejs-client/core/dist/cubejs-client-core.esm";
import { QueryBuilder } from "@cubejs-client/vue";
import QUERY from "./components/Query.js";
import Chart from "./components/Chart.vue";
import { CUBE_JS_HOST, CUBE_JS_SECRET } from "../../../../../config.js";
import Datepicker from "vuejs-datepicker";
import cardGraphData from "./data.json";

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
  methods: {
    dateRange: function () {
      return {
        startDate: this.startDate,
        endDate: this.endDate,
      };
    },
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
  },
  computed: {
    cardRenderer() {
      return cardGraphData.cards.map((item) => {
        console.log("xxxxxxxxxxxxxxx",item);
        return item;
      });
    },
  },
  data() {
    var startDate = new Date(2016, 9, 16);
    var endDate = new Date(2016, 9, 17);
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
      TabPaymentEntryMonthlyRevnue: QUERY.TabPaymentEntryMonthlyRevnue(
        DateRange,
        startDate
      ),
      TabPaymentEntryWeeklyRevnue: QUERY.TabPaymentEntryWeeklyRevnue,
      TabSalesInvoiceItemConversionRatio:
        QUERY.TabSalesInvoiceItemConversionRatio,
      TabPaymentEntryMonthlyAverage: QUERY.TabPaymentEntryMonthlyAverage,
      TabPaymentEntryWeeklyAverage: QUERY.TabPaymentEntryWeeklyAverage,
      TabSalesInvoiceTrueCount: QUERY.TabSalesInvoiceTrueCount,
      TabSalesInvoiceItemTrueQty: QUERY.TabSalesInvoiceItemTrueQty,
      TabItemProductCount: QUERY.TabItemProductCount,
      TabSalesInvoiceRevnue: QUERY.TabSalesInvoiceRevnue,
      TabSalesInvoiceTopCustomerByRevenue:
        QUERY.TabSalesInvoiceTopCustomerByRevenue,
      TabSalesInvoiceTopCustomerGroupByRevenue:
        QUERY.TabSalesInvoiceTopCustomerGroupByRevenue,
      TabSalesInvoiceTopsalesPartnerByRevenue:
        QUERY.TabSalesInvoiceTopsalesPartnerByRevenue,
      TabSalesInvoiceRevenueByTerritory:
        QUERY.TabSalesInvoiceRevenueByTerritory,
    };
    return { ...dataObj, startDate, endDate };
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
