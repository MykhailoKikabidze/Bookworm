<template>
  <div>
    <!-- Toast Notification -->
    <div 
      class="toast" 
      :class="[notificationClass, { show: visible }]"
      v-if="visible"
    >
      {{ message }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'Toast',
  data() {
    return {
      visible: false,
      message: '',
      notificationClass: '', 
      toastType: 'success', // 'success' or 'error'
    };
  },
  methods: {
    hz() {
      this.message = 'Error changing username.';
      this.notificationClass = 'error-toast'; // Assign the error style
      this.showNotificationMessage();
    },
    showNotificationMessage() {
      this.visible = true; // Show the toast
      setTimeout(() => {
        this.visible = false; // Hide the toast after 3 seconds
        this.message = ''; // Clear the message
      }, 10000); // Duration (in milliseconds)
    },
  },
};
</script>

<style scoped>
.toast {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #333;
  color: white;
  padding: 15px 30px;
  border-radius: 8px;
  font-size: 16px;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.5s ease, visibility 0s 0.5s;
  z-index: 9999;
}
.toast.show {
  opacity: 1;
  visibility: visible;
  transition: opacity 0.5s ease, visibility 0s 0s;
}
.success-toast {
  background-color: #4caf50;
}
.error-toast {
  background-color: #f44336;
}
</style>
