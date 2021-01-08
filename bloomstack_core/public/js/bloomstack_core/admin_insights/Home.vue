<template>
  <div>
    <div class="average-cards">
      <div class="row"><div class="sub-title-text">Average Cards</div></div>
      <div class="col-sm-4" v-for="card in cardRenderer" :key="card.data.type">
        <query-builder :cubejs-api="cubejsApi" :query="card.data">
          <template v-slot="{ loading, resultSet }">
            <Chart
              title
              :type="card.data.type"
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
      <div
        class="col-sm-6"
        v-for="graph in graphRenderer"
        :key="graph.data.type"
      >
        <query-builder :cubejs-api="cubejsApi" :query="graph.data">
          <template v-slot="{ loading, resultSet }">
            <Chart
              :type="graph.type"
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
import Datepicker from "vuejs-datepicker";

const cubejsApiFn = (host, secret) =>
  cubejs(secret, {
    apiUrl: host + "/cubejs-api/v1",
  });

function transformData(cards, type) {
  cards = cards.filter((el) => el.type === type);
  let newCards = [];
  cards.map((el) => {
    let data = JSON.parse(el.data);
    let type = el.type;
    newCards.push({ data, type });
  });
  return newCards.map((item) => {
    return item;
  });
}

export default {
  name: "Home",
  components: {
    QUERY,
    Chart,
    QueryBuilder,
    Datepicker,
  },
  props: {
    cardsData: {
      type: Array,
    },
    config: {
      CubeJsHost: String,
      CubeJsSecret: String,
    },
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
    cubejsApi() {
      let config = this.config;
      console.log("this is..config....", config);
      return cubejsApiFn(config.CubeJsHost, config.CubeJsSecret);
    },
    cardRenderer() {
      return transformData(this.cardsData, "Cards");
    },
    graphRenderer() {
      return transformData(this.cardsData, "Graphs");
    },
  },
  data() {
    var startDate = new Date(2016, 9, 16);
    var endDate = new Date(2016, 9, 17);
    let DateRange = "This Week";
    const dataObj = {
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
