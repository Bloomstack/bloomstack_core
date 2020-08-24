import LicenseService from '../../license_search/services/license_service';
import FrappeService from "../../license_search/services/frappe_service";
import NProgress from 'nprogress';
import 'nprogress/nprogress.css'


export default {
   state:{
      filters: {},
      licenseTypes: [],
      licenses: [],
      perPage: 20,
      currentPage: 1,
      totalPages: 0,

      leads: [],
      customers: [],
      suppliers: []
   },


   mutations:{
      SET_FILTER(state, filters) {
         state.filters = filters;
      },
      SET_LICENSES(state, licenses) {
         state.licenses = licenses.license_info;
         state.totalPages = Math.ceil(Number(licenses.total_count)/state.perPage);
         state.licenseTypes = licenses.license_types;
      },
      SET_PAGE(state, page) {
         state.currentPage = page;
      },

      ADD_LEAD(state, lead) {
         state.leads.push(lead);
      },
      ADD_CUSTOMER(state, customer) {
         state.customers.push(customer);
      },
      ADD_SUPPLIER(state, supplier) {
         state.suppliers.push(supplier);
      }
   },
   actions:{
      applyFilter({ commit, dispatch, state }, filters) {
         commit('SET_FILTER', filters);
         dispatch('fetchLicenses', {
            pageNum: state.currentPage
         })
      },
      updatePage({ commit, dispatch }, page) {
         commit('SET_PAGE', page);
         dispatch('fetchLicenses', {
            pageNum: page
         })
      },
      fetchLicenses({ commit, state }, data) {
         NProgress.start();
         data.filters = state.filters;
         data.perPage = state.perPage;
         LicenseService.getLicenses(data).then(function(response) {
            commit('SET_LICENSES', response);
            NProgress.done();
         });
      },
      makeLead({ commit, dispatch, state }, lead) {
         FrappeService.insertDoc({
            doc: lead,
            isFieldExist: "customer_name"
         }).then(function(response) {
            commit('ADD_LEAD', response);
         });
      },
      makeCustomer({ commit, dispatch }, customer) {
         FrappeService.insertDoc({
            doc: customer,
            isFieldExist: "customer_name"
         }).then(function(response) {
            commit('ADD_CUSTOMER', response);
         });
      },
      makeSupplier({ commit, state }, supplier) {
         FrappeService.insertDoc({
            doc: supplier,
            isFieldExist: "customer_name"
         }).then(function(response) {
            commit('ADD_SUPPLIER', response);
         });
      }
   }
}