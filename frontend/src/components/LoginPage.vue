<script>
import axios from 'axios'
import loginImage from "../assets/loginRegister.jpg"

export default {
    data() {
        return {
            formData: {
                username: "",
                password: ""
            },
            token: "",
            error: "",
            loginImage: loginImage
        }
    },
    methods: {
        async loginUser() {
            try {
                const res = await axios.post(
                    "http://127.0.0.1:5000/api/login",
                    this.formData,
                    { headers: { "Content-Type": "application/json" } }
                )
                this.token = res.data.access_token
                localStorage.setItem("token", res.data.access_token)
                const userId = res.data.id
                if (res.data.role === "admin") this.$router.push("/admin/dashboard")
                else if (res.data.role === "doctor") this.$router.push(`/doctor/${userId}/dashboard`)
                else if (res.data.role === "patient") this.$router.push(`/patient/${userId}/dashboard`)
            } catch (err) {
                this.error = err.response?.data?.message || "Login failed"
            }
        }
    }
}
</script>

<template>
    <div class="login-container">
        <div class="login-image-section">
            <img :src="loginImage" alt="Medical Team Illustration">
        </div>

        <div class="login-form-section">
            <div class="login-card text-center">
                <h1 class="fw-bold mb-4">MedixHub<sup>+</sup></h1>
                <p class="text-muted mb-4">
                    <span class="text-dark fw-bold">Welcome Back!</span> Please enter your details to continue.
                </p>

                <div v-if="error" class="alert alert-danger">{{ error }}</div>

                <form @submit.prevent="loginUser">
                    <div class="form-floating mb-3">
                        <input type="email" class="form-control" id="email" placeholder="Enter email"
                            v-model="formData.username" required>
                        <label for="email"><i class="bi bi-envelope-fill me-2"></i>Username</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input type="password" class="form-control" id="password" placeholder="Enter password"
                            v-model="formData.password" required>
                        <label for="password"><i class="bi bi-lock-fill me-2"></i>Password</label>
                    </div>

                    <button type="submit" class="btn btn-signin w-100 mb-3">
                        <i class="bi bi-box-arrow-in-right me-1"></i> Sign in
                    </button>

                    <div class="text-center text-muted my-2">or</div>

                    <div class="text-center mt-3">
                        Don’t have an account?
                        <router-link to="/register" class="text-dark fw-semibold text-decoration-none">
                            Register for free!
                        </router-link>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped>
.login-container {
    display: flex;
    min-height: 100vh;
    font-family: 'Poppins', sans-serif;
}

.login-image-section {
    width: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
}

.login-image-section img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.login-form-section {
    width: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px;
    background: #fff;
}

.login-card {
    width: 100%;
    max-width: 400px;
}

h1.fw-bold {
    color: #4084F6;
}

.btn-signin {
    background: linear-gradient(90deg, #4084F6, #5268F8);
    color: #fff;
    font-weight: 600;
    border: none;
}

@media (max-width: 991.98px) {
    .login-container {
        flex-direction: column;
    }
}

@media (max-width: 767.98px) {
    .login-image-section {
        display: none;
    }

    .login-form-section {
        width: 100%;
        padding: 20px;
    }
}
</style>