<template>
  <button
    @click="onClick"
    :class="['flex flex-col items-center gap-2 p-4 rounded-xl text-white hover:scale-105 transition-transform shadow-lg', gradient]"
  >
    <component :is="icon" class="h-6 w-6" />
    <span class="text-xs text-center">{{ label }}</span>
  </button>
</template>

<script>
export default {
  props: {
    icon: {
      type: Object,
      required: true
    },
    label: {
      type: String,
      required: true
    },
    onClick: {
      type: Function,
      required: true
    },
    gradient: {
      type: String,
      required: true
    }
  }
};
</script>

<style scoped>
/* Add any additional styles here */
</style>
