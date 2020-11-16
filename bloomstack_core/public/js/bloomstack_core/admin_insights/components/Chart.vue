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
        <tab-bin-item-code-wise v-if="!loading && type === 'TabBinItemCodeWise'" :values="values" :metrics="metrics" />
        <tab-bin-hand-ware-house-wise v-if="!loading && type === 'TabBinHandWareHouseWise'" :values="values" :metrics="metrics" />
        <guage-chart v-if="!loading && type === 'GuageChart'" :values="values" :metrics="metrics" />
        <tab-lead-by-city-location v-if="!loading && type === 'TabLeadByCityLocation'" :values="values" :metrics="metrics" />


        <kpi-currency v-if="!loading && type === 'TabPaymentEntryMonthlyRevnue'" :values="values" :metrics="metrics" title="MONTHLY REVENUE" description="Payments received in the last 30 days"/>
        <kpi-currency v-if="!loading && type === 'TabPaymentEntryWeeklyRevnue'" :values="values" :metrics="metrics" title="WEEKLY REVENUE" description="Payments received in the last 7 days"/>
        <kpi-currency v-if="!loading && type === 'TabPaymentEntryMonthlyAverage'" :values="values" :metrics="metrics" title="AVERAGE DAILY REVENUE (LAST MONTH)" description="Average of payments received in the last 30 days"/>
        <kpi-currency v-if="!loading && type === 'TabPaymentEntryWeeklyAverage'" :values="values" :metrics="metrics" title="AVERAGE DAILY REVENUE (LAST WEEk)" description="Average of payments received in the last 7 days"/>
        <kpi v-if="!loading && type === 'TabSalesInvoiceItemConversionRatio'" :values="values" :metrics="metrics" title="BOOK-TO-BILL RATIO" description="% conversion rate for lifetime orders"/>
        <kpi v-if="!loading && type === 'TabSalesInvoiceTrueCount'" :values="values" :metrics="metrics" title="TOTAL INVOICES" description="Raised from the start of business"/>
        <kpi v-if="!loading && type === 'TabSalesInvoiceItemTrueQty'" :values="values" :metrics="metrics" title="PRODUCTS SOLD" description="Sold from the start of business"/>
        <kpi v-if="!loading && type === 'TabItemProductCount'" :values="values" :metrics="metrics" title="TOTAL PRODUCTS" description="Number of products being sold"/>
        <line-gchart v-if="!loading && type === 'TabSalesInvoiceRevnue'" :values="values" :metrics="metrics" title="TOTAL REVENUE" description="month-to-date" xname="Posting Date" yname="Revenue"/>
        <line-gchart v-if="!loading && type === 'TabSalesInvoiceWeeklySales'" :values="values" :metrics="metrics" title="TOP SALES" description="by week" xname="Posting Date" yname="Sales"/>
        <line-cummulative-gchart v-if="!loading && type === 'TabSalesInvoiceCummulativeRevnue'" :values="values" :metrics="metrics" title="TOTAL REVENUE" description="MONTHLY" xname="Posting Date" yname="Revenue"/>
        <coloumn-gchart v-if="!loading && type === 'TabSalesInvoiceTopCustomerByRevenue'" :values="values" :metrics="metrics" title="TOP CUSTOMER" description="MONTHLY" xname="Customer Name" yname="Revenue"/>
        <coloumn-gchart v-if="!loading && type === 'TabSalesInvoiceTopCustomerGroupByRevenue'" :values="values" :metrics="metrics" title="TOTAL CUSTOMER GROUP" description="MONTHLY" xname="Customer Group" yname="Revenue"/>
        <bar-gchart v-if="!loading && type === 'TabSalesInvoiceTopsalesPartnerByRevenue'" :values="values" :metrics="metrics" title="TOP SALES PARTNERS" description="MONTHLY" xname="Customer Group" yname="Revenue"/>
        <donut-gchart v-if="!loading && type === 'TabSalesInvoiceRevenueByTerritory'" :values="values" :metrics="metrics" title="TOTAL REVENUE" description="Territory" xname="Customer Group" yname="Revenue"/>
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
import GuageChart from "./GuageChart.vue";
import TabBinItemCodeWise from "./TabBinItemCodeWise.vue";
import TabBinHandWareHouseWise from "./TabBinHandWareHouseWise.vue";
import TabLeadByCityLocation from "./TabLeadByCityLocation.vue";
//Insight engine Chart
import KpiCurrency from "./KpiCurrency.vue";
import kpi from "./Kpi.vue";
import LineGchart from "./LineGchart.vue";
import LineCummulativeGchart from "./LineCummulativeGchart.vue";
import ColoumnGchart from "./ColoumnGchart.vue";
import BarGchart from "./BarGchart.vue";
import DonutGchart from "./DonutGchart.vue";
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
    GuageChart,
    TabBinItemCodeWise,
    TabBinHandWareHouseWise,
    TabLeadByCityLocation,
    //Insight engine Component
    KpiCurrency,
    kpi,
    LineGchart,
    LineCummulativeGchart,
    ColoumnGchart,
    BarGchart,
    DonutGchart

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
      // console.log("qqqqq77777q....", this.loading, this.title, this.resultSet);
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
