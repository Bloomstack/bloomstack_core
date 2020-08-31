<template>
    <div>
        <label v-if="label" :for="label">{{ label }}</label>
        <select :id="label" @change="updateValue">
            <option
                    v-for="option in options"
                    :selected="option === value"
            >{{ option }}</option>
        </select>
    </div>
</template>

<script>
    import FormField from './../mixins/form_field';

    export default {
        mixins: [FormField],
        props: {
            options: Array,
        }
    }
</script>