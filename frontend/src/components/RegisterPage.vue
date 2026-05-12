<script>
import axios from "axios";
import registerImage from "../assets/loginRegister.jpg"

export default {
    data() {
        return {
            registerData: {
                username: "",
                password: "",
                fullname: ""
            },
            registerImage,
            error: "",
            success: ""
        }
    },
    methods: {
        async registerUser() {
            this.error = ""
            this.success = ""
            try {
                const res = await axios.post("http://127.0.0.1:5000/api/register",
                    this.registerData,
                    { headers: { "Content-Type": "application/json" } }
                )
                this.success = "Registration successful! Please Login"
                this.$router.push('/login')
                alert(this.success)
            } catch (error) {
                if (error.response) {
                    this.error = error.response.data
                } else {
                    this.error = "Network error"
                }
            }
        }
    }
}
</script>

<template>
    <div class="register-container">
        <div class="register-image-section">
            <img :src="registerImage" alt="Medical Team Illustration">
        </div>

        <div class="register-form-section">
            <div class="register-card text-center">
                <h1 class="fw-bold mb-4" style="color:#4084F6;">MedixHub<sup>+</sup></h1>
                <p class="text-muted mb-4">
                    <span class="text-dark fw-bold">Get Started!</span> Please enter your details to create a new
                    account.
                </p>
                <div v-if="error" class="alert alert-danger">{{ error }}</div>

                <form @submit.prevent="registerUser">
                    <div class="form-floating mb-3">
                        <input v-model="registerData.fullname" type="text" class="form-control" id="fullname"
                            placeholder="Enter fullname" required>
                        <label for="fullname"><i class="bi bi-person-fill me-2"></i>Fullname</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input v-model="registerData.username" type="email" class="form-control" id="email"
                            placeholder="Enter email" required>
                        <label for="email"><i class="bi bi-envelope-fill me-2"></i>Username</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input v-model="registerData.password" type="password" class="form-control" id="pwd"
                            placeholder="Enter password" required>
                        <label for="pwd"><i class="bi bi-lock-fill me-2"></i>Password</label>
                    </div>
                    <button type="submit" class="btn btn-register w-100 mb-3">
                        <i class="bi bi-person-plus-fill me-1"></i> Register
                    </button>

                    <div class="text-center text-muted my-2">or</div>

                    <div class="text-center mt-3">
                        Already have an account?
                        <router-link to="/login" class="text-dark fw-semibold text-decoration-none">
                            Sign in
                        </router-link>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped>
.register-container {
    display: flex;
    min-height: 100vh;
    font-family: 'Poppins', sans-serif;
}

.register-image-section {
    width: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
}

.register-image-section img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.register-form-section {
    width: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px;
    background: #fff;
}

.register-card {
    width: 100%;
    max-width: 400px;
}

.btn-register {
    background: linear-gradient(90deg, #4084F6, #5268F8);
    color: #fff;
    font-weight: 600;
    border: none;
}

@media (max-width: 991.98px) {
    .register-container {
        flex-direction: column;
    }
}

@media (max-width: 767.98px) {
    .register-image-section {
        display: none;
    }

    .register-form-section {
        width: 100%;
        padding: 20px;
    }
}
</style>