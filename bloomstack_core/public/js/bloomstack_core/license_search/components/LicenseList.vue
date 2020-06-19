<template>
    <div class="license-list">
        <License v-for="item in license.licenses" :key="item.license_number" :license="item" />
        <Paginate v-on:changePage="refreshView" :pageNum="license.currentPage" :totalPages="license.totalPages" />
    </div>
</template>

<script>
    import License from "./License.vue";
    import Paginate from "./../../components/paginate.vue";
    import Vuex from 'vuex/dist/vuex';

    export default {
        components: {
            License,
            Paginate
        },
        created() {
            this.refreshView();
        },
        computed: {
            ...Vuex.mapState(['license'])
        },
        methods: {
            refreshView(page=1) {
                this.$store.dispatch('updatePage', page);
            }
        }
    }
</script>

<style>

</style>