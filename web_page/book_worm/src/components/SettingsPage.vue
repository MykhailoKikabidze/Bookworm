<template>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500&display=swap" rel="stylesheet">

    <div class="settings-container">
      <div class="overlay"></div> <!-- Semi-transparent overlay -->
     
      <div class="form-container">
        <h1>Update Settings</h1>
        <form @submit.prevent="updateSettings">
          <div class="form-group">
            <label for="username">New Username</label>
            <input type="text" id="username" v-model="newUsername" required />
            <button type="button" @click="saveUsername" class="save-username-button">Save Username</button>
          </div>
          <div class="form-group">
            <label for="password">Current Password</label>
            <div class="password-wrapper">
              <input
                :type="currentPasswordVisible ? 'text' : 'password'"
                id="password"
                v-model="currentPassword"
                :class="{ 'input-error': !isPasswordValid && currentPassword.length > 0 }"
                required
              />
              <span v-if="!isPasswordValid && currentPassword.length > 0" class="error-message">
                Password must be at least 8 characters.
              </span>
              <span @click="toggleCurrentPasswordVisibility" class="eye-icon">
                <i :class="currentPasswordVisible ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </span>
            </div>
          </div>
          <div class="form-group">
            <label for="password">New Password</label>
            <div class="password-wrapper">
              <input
                :type="newPasswordVisible ? 'text' : 'password'"
                id="password"
                v-model="newPassword"
                :class="{ 'input-error': !isPasswordValid && newPassword.length > 0 }"
                required
              />
              <span v-if="!isPasswordValid && newPassword.length > 0" class="error-message">
                Password must be at least 8 characters.
              </span>
              <span @click="toggleNewPasswordVisibility" class="eye-icon">
                <i :class="newPasswordVisible ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </span>
            </div>
          </div>
          <div class="form-group">
            <label for="confirm-password">Confirm Password</label>
            <div class="password-wrapper">
              <input
                :type="'password'"
                id="confirm-password"
                v-model="confirmPassword"
                :class="{ 'input-error': confirmPassword && confirmPassword !== newPassword }"
                required
              />
              <span v-if="confirmPassword && confirmPassword !== newPassword" class="error-message">
                Passwords do not match.
              </span>
            </div>
          </div>
          <button
            type="button"
            @click="savePassword"
            :disabled="!isPasswordValid || confirmPassword !== newPassword"
          >
            Save Password
          </button>
        </form>
  
        <!-- Toast Notification -->
        <div v-if="notificationMessage" :class="notificationClass" class="toast-notification">
          {{ notificationMessage }}
        </div>
  
        <button type="button" class="delete-account-button" @click="deleteAccount">Delete Account</button>
      </div>
      <Toast ref="toastRef" />

    </div>
  </template>
  
  <script>
  import Toast from './Toast.vue';

  export default {
    data() {
      return {
        newUsername: "",
        currentPassword: "",
        correctPassword: false,
        email:"",
        newPassword: "",
        confirmPassword: "",
        newPasswordVisible: false,  // Independent state for new password visibility
        currentPasswordVisible: false,  // Independent state for confirm password visibility
        notificationMessage: "",  // Holds the notification message
        notificationClass: "",  // Holds the class for the notification style (success/error)
      };
    },
    components: {
    Toast,
  },
    computed: {
      isPasswordValid() {
        return this.newPassword.length >= 8;
      },
    },
    methods: {
      toggleCurrentPasswordVisibility() {
        this.currentPasswordVisible = !this.currentPasswordVisible;
      },
      toggleNewPasswordVisibility() {
        this.newPasswordVisible = !this.newPasswordVisible;
      },
      async authorization() {
      try {
        const response = await fetch(this.$link_backend + "/users/me", {
          method: 'GET',
          headers: {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + localStorage.getItem('authToken'),
            "ngrok-skip-browser-warning": "anyValue"
          },
        });

        if (!response.ok) {
          const data = await response.json();
          this.responseData = data.detail;

        } else {
          const data = await response.json();
          this.email=data.login;
        }
      } catch (error) {
        console.error("Error during authorization:", error);

      }

    },
      async saveUsername() {
        const params = new URLSearchParams();
        params.append("new_username", this.newUsername);
  
        try {
          const response = await fetch(`${this.$link_backend}/users/name?${params.toString()}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
              "Authorization": `Bearer ${localStorage.getItem('authToken')}`,
            },
          });
  
          if (response.ok) {
            this.showNotification('Username successfully updated!', 'success-toast');
          } else {
            const data = await response.json();
            this.showNotification(data.detail || 'Error updating username.', 'error-toast');
          }
        } catch (error) {
          this.showNotification('Error updating username.', 'error-toast');
        }
      },
      async getToken() {
      const toastRef = this.$refs.toastRef;

      const params = new URLSearchParams();
      params.append("username", this.email);
      params.append("password", this.currentPassword);
      const response = await fetch(this.$link_backend + "/token", {
       method: 'POST',
       headers: {
       'Content-Type': 'application/x-www-form-urlencoded',
         "ngrok-skip-browser-warning": "anyValue"
       },
       body: params
      });
        if (!response.ok) {
          const data = await response.json();
          this.correctPassword=true;
          toastRef.message =data.detail + ' current password writing by user is incorrect';
          toastRef.notificationClass = 'error-toast';
        }
        else{
          this.correctPassword=false;
        }
     this.$refs.toastRef.showNotificationMessage();

    },
      async savePassword() {
        if (!this.isPasswordValid) {
          this.showNotification('Password must be at least 8 characters long.', 'error-toast');
          return;
        }
        if (this.newPassword !== this.confirmPassword) {
          this.showNotification('Passwords do not match.', 'error-toast');
          return;
        }
        
        await this.authorization();
        await this.getToken();

        if(this.correctPassword)
        {
          return;
        }

        //to do
        //from  GET "users/me" take the our mail
        //then PUT "/token" with this.currentPassword if ok continue (PUT "users/password")
        //if doesn't -> current password writing by user is incorrect (show toast) 
  
        const params = new URLSearchParams();
        params.append("new_password", this.newPassword);
  
        try {
          const response = await fetch(`${this.$link_backend}/users/password?${params.toString()}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
              "Authorization": `Bearer ${localStorage.getItem('authToken')}`,
            },
          });
  
          if (response.ok) {
            this.showNotification('Password successfully updated!', 'success-toast');
          } else {
            const data = await response.json();
            this.showNotification(data.detail || 'Error updating password.', 'error-toast');
          }
        } catch (error) {
          this.showNotification('Error updating password.', 'error-toast');
        }
      },
  
      async deleteAccount() {
        const confirmation = confirm("Are you sure you want to delete your account? This action is irreversible.");
        if (!confirmation) return;
  
        try {
          const response = await fetch(`${this.$link_backend}/users`, {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
              "Authorization": `Bearer ${localStorage.getItem('authToken')}`,
            },
          });
  
          if (response.ok) {
            localStorage.removeItem("authToken");
            window.location.reload();
            this.showNotification('Account deleted successfully.', 'success-toast');
          } else {
            const data = await response.json();
            this.showNotification(data.detail || 'Error deleting account.', 'error-toast');
          }
        } catch (error) {
          this.showNotification('Error deleting account.', 'error-toast');
        }
      },
  
      showNotification(message, type) {
        this.notificationMessage = message;
        this.notificationClass = type;
        setTimeout(() => {
          this.notificationMessage = '';
        }, 3000); // Notification will disappear after 3 seconds
      },
    },
  };
  </script>
  
  <style scoped>
  .settings-container {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-image: url('./pictures/book.jpeg');
    background-size: cover;
    background-position: center;
    overflow: hidden;
  }
  
  .overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(250, 250, 250, 0.15);
    z-index: 1;
  }
  
  .form-container {
    position: relative;
    z-index: 2;
    background-color: rgba(255, 255, 255, 0.9);
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    width: 350px;
    text-align: center;
    font-family: 'Georgia', serif;
    color: #002f5b;
  }
  
  h1 {
    font-size: 28px;
    color: #002f5b;
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 20px;
    text-align: left;
    position: relative;
  }
  
  label {
    font-size: 17px;
    color: #002f5b;
    margin-bottom: 5px;
    display: block;
  }
  
  input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 16px;
    font-family: 'Georgia', serif;
    background-color: #f5f5f5;
    color: #2f2f2f;
  }
  
  button {
    width: 100%;
    padding: 10px;
    border: none;
    border-radius: 5px;
    background-color: #002f5b;
    color: white;
    font-size: 18px;
    font-family: 'Georgia', serif;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  button:hover {
    background-color: #004080;
  }
  
  .eye-icon {
    position: absolute;
    right: 14px;
    top: 10px;
    cursor: pointer;
    font-size: 18px;
    color: #002f5b;
  }
  
  .eye-icon i {
    font-size: 20px;
  }
  
  .error-message {
    color: red;
    font-size: 12px;
    margin-top: 5px;
    position: absolute;
    left: 0;
    top: 100%;
    width: 100%;
  }
  
  .toast-notification {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    padding: 10px 20px;
    border-radius: 5px;
    font-size: 16px;
    font-weight: bold;
    z-index: 9999;
    opacity: 0;
    animation: fadeIn 0.5s forwards;
  }
  
  .success-toast {
    background-color: green;
    color: white;
  }
  
  .error-toast {
    background-color: red;
    color: white;
  }
  
  @keyframes fadeIn {
    0% {
      opacity: 0;
      transform: translateX(-50%) translateY(-20px);
    }
    100% {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }
  }
  
  .toast-notification.hide {
    animation: fadeOut 0.5s forwards;
  }
  
  @keyframes fadeOut {
    0% {
      opacity: 1;
    }
    100% {
      opacity: 0;
      transform: translateX(-50%) translateY(-20px);
    }
  }
  
  .delete-account-button {
    background-color: red;
    color: white;
    margin-top: 20px;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .delete-account-button:hover {
    background-color: darkred;
  }

  .save-username-button {
  margin-top: 20px; /* Możesz dostosować tę wartość */
}


  </style>
  