<template>
    <div class="license-filter">
        <form @submit.prevent="applyFilters">
            <Input type="text" placeholder="Search" v-model="filters.search" />
            <Input type="text" placeholder="Zipcode" v-model="filters.zip" />
            <Select label="License Type" :options="license.licenseTypes" v-model="filters.licenseType" />

            <input type="submit" value="Submit" />
        </form>
    </div>
</template>

<script>
    import Input from './../../components/input.vue';
    import Select from './../../components/select.vue';
    import Vuex from './../../../../node_modules/vuex/dist/vuex';

    export default {
        components: {
            Input,
            Select
        },
        data() {
            return {
                filters: {
                    search: "",
                    zip: "",
                    licenseType: ""
                }
            }
        },
        computed: {
            ...Vuex.mapState(['license'])
        },
        methods: {
            applyFilters() {
                this.$store.dispatch("applyFilter", this.filters);
            }
        }
    }
</script>