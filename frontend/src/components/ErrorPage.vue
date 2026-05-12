<script>
import errorImg from '../assets/error2.jpg'
export default {
  data() {
    return {
      errorImg
    }
  }
}
</script>

<template>
  <div class="error-container">
    <img :src="errorImg" alt="404 Error" class="error-image" />
  </div>
</template>

<style scoped>
.error-container {
  height: 100vh;
}

.error-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>

