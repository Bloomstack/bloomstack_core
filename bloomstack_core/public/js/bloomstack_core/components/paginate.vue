<template>
    <div class="paginate">
        <ul>
            <li v-if="pageNum!=1" @click="changePage(pageNum-1)" class="prev">Prev</li>
            <li @click="changePage(page)" v-for="page in pages" :key="page">{{ page }}</li>
            <li @click="changePage(pageNum+1)" class="next">Next</li>
        </ul>
    </div>
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
                console.log(page)
                this.$emit("changePage", page);
            }
        }
    }
</script>

<style>

</style>