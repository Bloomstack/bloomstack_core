<template>
    <div>
        <label v-if="label" :for="label">{{ label }}</label>
        <input
                :id="label"
                :value="value"
                v-bind="$attrs"
                @input="updateValue"
        />
    </div>
</template>

<script>
    import FormField from './../mixins/form_field';

    export default {
        mixins: [FormField]

    }
</script>