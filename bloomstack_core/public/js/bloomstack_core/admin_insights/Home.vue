<template>
  <div id="app">
    <h1> Hello, {{ formatName(user) }}! </h1>
  </div>
</template>

<script>
export default {
  name: 'app',
  data() {
    return {
      user: {
        firstName: 'Harry',
        lastName: 'Manchanda'
      }
    };
  },
  methods: {
    formatName(user) {
      return `${user.firstName} ${user.lastName}`;
    }
  }
}
</script>

<style lang="scss">
</style>


<!-- 
<template>
  <div id="app-2">
    <span v-bind:title="message">
      Hover your mouse over me for a few seconds
      to see my dynamically bound title!
    </span>
  </div>
</template>


<script>
import cubejs from "@cubejs-client/core";
import { QueryBuilder } from "@cubejs-client/vue";
import Chart from "./Chart.vue";
const API_URL = "http://localhost:4000"; // change to your actual endpoint
const cubejsApi = cubejs(
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1OTc4Mzk2MDYsImV4cCI6MTU5NzkyNjAwNn0.eyS33ppbBdPZsb9K7ymkhKrHS-l2x_hf25lXFVk5m30",
  { apiUrl: API_URL + "/cubejs-api/v1" }
);
export default {
  name: "Home",
  components: {
    Chart,
    QueryBuilder,
  },
  data() {
    return {
      cubejsApi,
      selected: { value: 2, text: "day" },
      granularity: [
        { value: 1, text: "hour" },
        { value: 2, text: "day" },
        { value: 3, text: "week" },
        { value: 4, text: "month" },
        { value: 5, text: "year" },
      ],
    };
  },
  computed: {
    tabsalesQuery() {
      return {
        order: {},
        measures: [
          "TabSalesInvoice.total",
          // "TabSalesInvoice.totalSalesMonthly",
          "TabSalesInvoice.outstandingAmount",
          "TabSalesInvoice.totalQty",
          "TabSalesInvoice.discountAmount",
        ],
        timeDimensions: [
          {
            dimension: "TabSalesInvoice.creation",
            granularity: this.selected.text,
            // dateRange: dateRange ? dateRange : [startDate, endDate],
          },
        ],
        filters: [
          {
            dimension: "TabTerritory.name",
            operator: "equals",
            values: ["Northern California"],
          },
        ],
      };
    },
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
 -->