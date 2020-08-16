<template>
    <div class="license-list">
        <License v-for="item in license.licenses" :key="item.license_number" :license="item" />
        <paginate
            :page-count="license.totalPages"
            :click-handler="refreshView"
            :prev-text="'Prev'"
            :next-text="'Next'"
            :container-class="'paginate'"
            :page-class="'page-item'"
            :pageNum="license.currentPage">
        </paginate>
    </div>
</template>

<script>
    import License from "./License.vue";
    import Vuex from './../../../../node_modules/vuex/dist/vuex';
    import Paginate from 'vuejs-paginate';

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