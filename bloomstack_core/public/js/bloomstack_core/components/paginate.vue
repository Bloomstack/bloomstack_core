<template>
    <paginate
    :page-count="totalPages"
    :click-handler="changePage"
    :prev-text="'Prev'"
    :next-text="'Next'"
    :container-class="'paginate'"
    :page-class="'page-item'">
    </paginate>
</template>

<script>
    export default {
        props: {
            pageNum: Number,
            totalPages: Number
        },
        computed: {
            pages() {
                let result = [];
                for(let i=1; i<this.totalPages; i++) {
                    result.push(i);
                }
                return result;
            }
        },
        methods: {
            changePage(page) {
                this.$emit("changePage", page);
            }
        }
    }
</script>

<style>

</style>