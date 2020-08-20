<template>

    <div class="wrapper">
        <FilterForm />
        <LicenseList />
    </div>

</template>

<script>
    import FilterForm from './components/FilterForm.vue';
    import LicenseList from './components/LicenseList.vue';
    import 'nprogress/nprogress.css';
    import NProgress from 'nprogress';

    export default {
        components: {
            FilterForm,
            LicenseList
        }
    }
</script>