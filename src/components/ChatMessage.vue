<template>
  <div :class="['flex gap-3', isBot ? 'justify-start' : 'justify-end']">
    <div v-if="isBot" class="h-8 w-8 bg-gradient-to-br from-orange-500 to-orange-600 rounded-full flex items-center justify-center">
      <span class="text-white">🤖</span>
    </div>
    <div :class="['flex flex-col max-w-[80%]', isBot ? 'items-start' : 'items-end']">
      <div class="p-2 rounded-lg" :class="isBot ? 'bg-gray-200 text-black' : 'bg-blue-500 text-white'">
        {{ message }}
      </div>
      <span class="text-xs text-gray-500 mt-1">{{ timestamp }}</span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    message: {
      type: String,
      required: true
    },
    isBot: {
      type: Boolean,
      required: true
    },
    timestamp: {
      type: String,
      required: true
    }
  }
};
</script>

<style scoped>
/* Add any additional styles here */
</style>
