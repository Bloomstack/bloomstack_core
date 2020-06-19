import LicenseService from '../../license_search/services/license_service';

export default {
   state:{
      filters: {},
      licenseTypes: [],
      licenses: [],
      perPage: 20,
      currentPage: 1,
      totalPages: null
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
         data.filters = state.filters;
         data.perPage = state.perPage;
         LicenseService.getLicenses(data).then(function(response) {
            commit('SET_LICENSES', response);
         });
      }
   }
}