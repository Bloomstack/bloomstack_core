<template>
  <div class="container-fluid">
    This is working now with the watch! hiii ofline
    <div class="row">
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
  </div>
</template>

<script>
import cubejs from "@cubejs-client/core/dist/cubejs-client-core.esm";
import { QueryBuilder } from "@cubejs-client/vue";
import QUERY from "./components/Query.js";
import Chart from "./components/Chart.vue";
import pieChartTerritory from "./components/Chart.vue";
const API_URL = "http://localhost:4000"; // change to your actual endpoint
// const API_URL ="https://ecom.cubecloudapp.dev";

const cubejsApi = cubejs(
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2MDAxNjkxOTMsImV4cCI6MTYwMjc2MTE5M30.M09WQCwOHkt-ZHhtdNk0Nk7IGi2krlEH-53y90RO-G4",
  { apiUrl: API_URL + "/cubejs-api/v1" }
);

export default {
  name: "Home",
  components: {
    QUERY,
    Chart,
    pieChartTerritory,
    QueryBuilder,
  },
  data() {
    const dataObj = {
      cubejsApi,
      TabSalesInvoiceItemUniqueItemCode:
        QUERY.TabSalesInvoiceItemUniqueItemCode,
      TabCustomerCount: QUERY.TabCustomerCount,
      TabSalesAverageInvoiceAmount: QUERY.TabSalesAverageInvoiceAmount,
      tabBinPieTerritoryQuery: QUERY.tabBinPieTerritoryQuery,
      PieChartTerritory: QUERY.PieChartTerritory,
      TabSalesInvoiceItemHorizontalBarChartByItemName:QUERY.TabSalesInvoiceItemHorizontalBarChartByItemName,
      tabBinPieQuery:QUERY.tabBinPieQuery
    };
    return { ...dataObj };
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
