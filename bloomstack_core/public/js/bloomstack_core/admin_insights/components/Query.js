const tabsalesQuery = (selected) => {
    return ({
        order: {},
        measures: [
            "TabSalesInvoice.netTotal",
            // "TabSalesInvoice.totalSalesMonthly",
            "TabSalesInvoice.outstandingAmount",
            "TabSalesInvoice.totalQty",
            "TabSalesInvoice.discountAmount",
        ],
        timeDimensions: [
            {
                dimension: "TabSalesInvoice.creation",
                granularity: selected.text,
                dateRange: "This year",
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
    });
};

const GuageChart = {
    measures: ["TabSalesInvoice.trueNetTotal"],
    timeDimensions: [
        {
            dimension: "TabSalesInvoice.creation",
        },
    ],
    order: {},
    filters: [],

};

const tabBinQuery = {
    "measures": [
        "TabBin.actualQty"
    ],
    "timeDimensions": [],
    "order": {
        "TabBin.actualQty": "asc"
    },
    "dimensions": [
        "TabBin.itemCode"
    ],
    "filters": []
};

const tabBinPieQuery = {
    measures: ["TabBin.actualQty"],
    timeDimensions: [
        {
            dimension: "TabBin.creation",
        },
    ],
    order: {
        "TabBin.warehouse": "desc",
    },
    dimensions: ["TabBin.warehouse"],
    filters: [],
};

const tabBinPieTerritoryQuery = {
    measures: ["TabSalesInvoice.netTotal"],
    timeDimensions: [
        {
            dimension: "TabSalesInvoice.creation",
        },
    ],
    order: {
        "TabSalesInvoice.netTotal": "asc",
        "TabSalesInvoice.territory": "asc",
    },
    dimensions: ["TabSalesInvoice.territory"],
    filters: [],
};

const TabSalesInvoiceCustomerGroup = {
    measures: ["TabSalesInvoice.netTotal"],
    timeDimensions: [
        {
            dimension: "TabSalesInvoice.creation",
        },
    ],
    order: {
        "TabSalesInvoice.total": "desc",
    },
    dimensions: ["TabSalesInvoice.customerGroup"],
    filters: [],
};

const PieSalesInvoiceByStatus = {
    measures: ["TabSalesInvoice.netTotal"],
    timeDimensions: [
        {
            dimension: "TabSalesInvoice.creation",
        },
    ],
    order: {
        "TabSalesInvoice.netTotal": "desc",
    },
    dimensions: ["TabSalesInvoice.status"],
    filters: [],
};

const TabSalesAverageInvoiceAmount = {
    measures: ["TabSalesInvoice.AverageInvoiceAmount"],
    timeDimensions: [
        {
            dimension: "TabSalesInvoice.creation",
        },
    ],
    order: {},
    filters: [],
};

const TabSalesTotalInvoiceCount = {
    "measures": [
        "TabSalesInvoice.count"
    ],
    "timeDimensions": [
        {
            "dimension": "TabSalesInvoice.creation"
        }
    ],
    "order": {},
    "filters": []
};

const TabCustomerCount = {
    measures: ["TabCustomer.countName"],
    timeDimensions: [
        {
            dimension: "TabCustomer.creation",
        },
    ],
    order: {},
    filters: [],
};

const TabSalesInvoiceNetTotal = {
    measures: ["TabSalesInvoice.trueNetTotal"],
    timeDimensions: [
        {
            dimension: "TabSalesInvoice.creation",
        },
    ],
    order: {},
    filters: [],
};

const TabSalesInvoiceItemUniqueItemCode = {
    "measures": [
        "TabSalesInvoiceItem.itemCodeCount"
    ],
    "timeDimensions": [
        {
            "dimension": "TabSalesInvoiceItem.creation"
        }
    ],
    "order": {},
    "filters": []
};

const TabSalesInvoiceItemHorizontalBarChartByItemName = {
    measures: ["TabSalesInvoiceItem.amount"],
    timeDimensions: [
        {
            dimension: "TabSalesInvoiceItem.creation",
        },
    ],
    order: {
        "TabSalesInvoiceItem.amount": "desc",
    },
    dimensions: ["TabSalesInvoiceItem.itemName"],
    filters: [],
    limit: 10,
};

const TabSalesInvoiceItemHorizontalBarChartByItemGroup = {
    measures: ["TabSalesInvoiceItem.amount"],
    timeDimensions: [
        {
            dimension: "TabSalesInvoiceItem.creation",
        },
    ],
    order: {
        "TabSalesInvoiceItem.amount": "desc",
    },
    dimensions: ["TabSalesInvoiceItem.itemGroup"],
    filters: [],
};

const TabPurchaseInvoiceHorizontalBarChartBySupplier = {
    measures: ["TabPurchaseInvoice.netTotal"],
    timeDimensions: [
        {
            dimension: "TabPurchaseInvoice.creation",
        },
    ],
    order: {
        "TabPurchaseInvoice.netTotal": "desc",
    },
    dimensions: ["TabPurchaseInvoice.supplier"],
    filters: [],
    limit: 10,
};

const TabCustomerBarChartByNewCustomer = {
    measures: ["TabCustomer.count"],
    timeDimensions: [
        {
            dimension: "TabCustomer.creation",
            granularity: "month",
        },
    ],
    order: {},
    filters: [],
};

const TabSalesInvoiceBarChartBySalesPartner = {
    measures: ["TabSalesInvoice.netTotal"],
    timeDimensions: [
        {
            dimension: "TabSalesInvoice.creation",
        },
    ],
    order: {
        "TabSalesInvoice.netTotal": "desc",
    },
    dimensions: ["TabSalesInvoice.salesPartner"],
    filters: [],
};

const TabBinItemCodeWise = {
    measures: ["TabBin.actualQty"],
    timeDimensions: [
        {
            dimension: "TabBin.creation",
        },
    ],
    order: {
        "TabBin.itemCode": "asc",
    },
    dimensions: ["TabBin.itemCode"],
    filters: [],
};

const TabBinHandWareHouseWise = {
    "measures": [
        "TabBin.actualQty"
    ],
    "timeDimensions": [
        {
            "dimension": "TabBin.creation"
        }
    ],
    "order": {
        "TabBin.warehouse": "asc"
    },
    "dimensions": [
        "TabBin.warehouse"
    ],
    "filters": []
};

const TabLeadByCityLocation = {
    "measures": [
        "TabLead.count"
    ],
    "timeDimensions": [
        {
            "dimension": "TabLead.creation"
        }
    ],
    "order": {
        "TabLead.city": "asc"
    },
    "dimensions": [
        "TabLead.city"
    ],
    "filters": []
};

//insight engine Query

const tabPaymentEntryMonthlyRevnue = {
    "measures": [
        "TabPaymentEntry.truePaidAmount"
    ],
    "timeDimensions": [
        {
            "dimension": "TabPaymentEntry.postingDate",
            "dateRange": "Last month"
        }
    ],
    "order": {},
    "filters": []
};

const tabPaymentEntryWeeklyRevnue = {
    "measures": [
        "TabPaymentEntry.truePaidAmount"
    ],
    "timeDimensions": [
        {
            "dimension": "TabPaymentEntry.postingDate",
            "dateRange": "Last week"
        }
    ],
    "order": {},
    "filters": []
};

const tabSalesInvoiceItemConversionRatio = {
    "measures": [
        "TabSalesInvoiceItem.salesInvoiceToSalesOrderRatio"
    ],
    "timeDimensions": [
        {
            "dimension": "TabSalesInvoiceItem.creation"
        }
    ],
    "order": {},
    "filters": []
};

const tabPaymentEntryMonthlyAverage = {
    "measures": [
        "TabPaymentEntry.monthlyAverageTruePaidAmount"
    ],
    "timeDimensions": [
        {
            "dimension": "TabPaymentEntry.creation",
            "dateRange": "Last month"
        }
    ],
    "order": {},
    "filters": []
};

const tabPaymentEntryWeeklyAverage = {
    "measures": [
        "TabPaymentEntry.weeklyAverageTruePaidAmount"
    ],
    "timeDimensions": [
        {
            "dimension": "TabPaymentEntry.creation",
            "dateRange": "Last week"
        }
    ],
    "order": {},
    "filters": []
};

const tabSalesInvoiceTrueCount = {
    "measures": [
        "TabSalesInvoice.trueCount"
    ],
    "timeDimensions": [
        {
            "dimension": "TabSalesInvoice.creation"
        }
    ],
    "order": {},
    "filters": []
};

const tabSalesInvoiceItemTrueQty = {
    "measures": [
        "TabSalesInvoiceItem.trueQty"
    ],
    "timeDimensions": [
        {
            "dimension": "TabSalesInvoiceItem.creation"
        }
    ],
    "order": {},
    "filters": []
};

const tabItemProductCount = {
    "measures": [
        "TabItem.productCount"
    ],
    "timeDimensions": [
        {
            "dimension": "TabItem.creation"
        }
    ],
    "order": {},
    "filters": []
};

const tabSalesInvoiceRevnue = (startDate, endDate ,range) => {
    return ({
        "measures": [
            "TabSalesInvoice.trueGrandTotal"
        ],
        "timeDimensions": [
            {
                "dimension": "TabSalesInvoice.postingDate",
                "granularity": "month",
                "dateRange": range?range:[startDate, endDate]
            }
        ],
        "order": {},
        "filters": []
    });
};

const tabSalesInvoiceTopCustomerByRevenue = (startDate, endDate,range) => {
    return ({
        "measures": [
            "TabSalesInvoice.trueGrandTotal"
        ],
        "timeDimensions": [
            {
                "dimension": "TabSalesInvoice.postingDate",
                "dateRange":range?range:[startDate, endDate]
            }
        ],
        "order": {
            "TabSalesInvoice.trueGrandTotal": "desc"
        },
        "filters": [],
        "dimensions": [
            "TabSalesInvoice.customerName"
        ],
        limit: 10
    });
};

const tabSalesInvoiceTopCustomerGroupByRevenue = (startDate, endDate,range) => {
    return ({
        "measures": [
            "TabSalesInvoice.trueGrandTotal"
        ],
        "timeDimensions": [
            {
                "dimension": "TabSalesInvoice.postingDate",
                "dateRange":range?range:[startDate, endDate]
            }
        ],
        "order": {
            "TabSalesInvoice.trueGrandTotal": "desc"
        },
        "filters": [],
        "dimensions": [
            "TabSalesInvoice.customerGroup"
        ],
        limit: 10
    });
};

const tabSalesInvoiceTopsalesPartnerByRevenue = (startDate,endDate,range) => {
    return ({
        "measures": [
            "TabSalesInvoice.trueGrandTotal"
        ],
        "timeDimensions": [
            {
                "dimension": "TabSalesInvoice.postingDate",
                "dateRange": range?range:[startDate,endDate]
            }
        ],
        "order": {
            "TabSalesInvoice.trueGrandTotal": "desc"
        },
        "filters": [],
        "dimensions": [
            "TabSalesInvoice.salesPartner"
        ],
        limit: 5
    });
};

const tabSalesInvoiceRevenueByTerritory = (startDate,endDate,range) => {
    return ({
        "measures": [
            "TabSalesInvoice.trueGrandTotal"
        ],
        "timeDimensions": [
            {
                "dimension": "TabSalesInvoice.postingDate",
                "dateRange": range?range:[startDate,endDate]
            }
        ],
        "order": {
            "TabSalesInvoice.trueGrandTotal": "desc"
        },
        "dimensions": [
            "TabSalesInvoice.territory"
        ],
        "filters": [
            {
                "dimension": "TabSalesInvoice.territory",
                "operator": "notEquals",
                "values": [
                    "All Territories"
                ]
            },
            {
                "dimension": "TabTerritory.is_group",
                "operator": "equals",
                "values": [
                    "1"
                ]
            }
        ]
    });
};

const tabSalesInvoiceWeeklySales = (startDate,endDate,range) => {
    return ({
        "measures": [
            "TabSalesInvoice.trueGrandTotal"
        ],
        "timeDimensions": [
            {
                "dimension": "TabSalesInvoice.postingDate",
                "dateRange": range?range:[startDate,endDate],
                "granularity": "week"
            }
        ],
        "order": {},
        "filters": []
    });
};

const Query = {
    tabsalesQuery: (selected) => tabsalesQuery(selected),
    tabBinQuery,
    GuageChart,
    tabBinPieQuery,
    tabBinPieTerritoryQuery,
    TabSalesInvoiceCustomerGroup,
    PieSalesInvoiceByStatus,
    TabSalesAverageInvoiceAmount,
    TabCustomerCount,
    TabSalesInvoiceNetTotal,
    TabSalesInvoiceItemUniqueItemCode,
    TabSalesInvoiceItemHorizontalBarChartByItemName,
    TabSalesInvoiceItemHorizontalBarChartByItemGroup,
    TabPurchaseInvoiceHorizontalBarChartBySupplier,
    TabCustomerBarChartByNewCustomer,
    TabSalesInvoiceBarChartBySalesPartner,
    TabBinItemCodeWise,
    TabBinHandWareHouseWise,
    TabLeadByCityLocation,
    TabSalesTotalInvoiceCount,
    //Insight engine Query
    tabPaymentEntryMonthlyRevnue,
    tabPaymentEntryWeeklyRevnue,
    tabSalesInvoiceItemConversionRatio,
    tabPaymentEntryMonthlyAverage,
    tabPaymentEntryWeeklyAverage,
    tabSalesInvoiceTrueCount,
    tabSalesInvoiceItemTrueQty,
    tabItemProductCount,
    tabSalesInvoiceRevnue,
    tabSalesInvoiceTopCustomerByRevenue,
    tabSalesInvoiceTopCustomerGroupByRevenue,
    tabSalesInvoiceTopsalesPartnerByRevenue,
    tabSalesInvoiceRevenueByTerritory,
    tabSalesInvoiceWeeklySales

};

export default Query;
