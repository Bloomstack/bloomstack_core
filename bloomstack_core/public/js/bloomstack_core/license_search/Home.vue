<template>

    <div class="wrapper">
        <FilterForm />
        <LicenseList />
    </div>

</template>

<script>
    import FilterForm from './components/FilterForm.vue';
    import LicenseList from './components/LicenseList.vue';

    export default {
        components: {
            FilterForm,
            LicenseList
        }
    }
</script>