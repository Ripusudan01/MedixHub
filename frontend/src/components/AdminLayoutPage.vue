<script>
import axios from 'axios'

export default {
    data() {
        return {
            jwt_token: "",
            layout_data: {}
        }
    },
    methods: {
        async fetchLayoutData() {
            try {
                const res = await axios.get("http://127.0.0.1:5000/api/dash_layout_data", {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${this.jwt_token}`
                    }
                })
                this.layout_data = res.data
            } catch (err) {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/login")
            }
        },
        logoutUser() {
            localStorage.removeItem("token")
            this.jwt_token = ""
            this.$router.push("/login")
        }
    },
    mounted() {
        const jwt = localStorage.getItem("token");
        if (jwt) {
            this.jwt_token = jwt;
            this.fetchLayoutData();
        } else {
            this.$router.push("/login");
            alert("Please login to access Dashboard.");
        }
    }
}
</script>

<template>
    <div v-if="jwt_token">
        <div class="d-flex dashboard-body">
            <div class="sidebar" style="position: fixed; z-index: 2;">
                <h4>MedixHub<sup>+</sup></h4>
                <hr />
                <nav class="nav flex-column">
                    <router-link to="/admin/dashboard" class="nav-link" exact-active-class="active-link">
                        <i class="bi bi-grid me-2"></i> Dashboard
                    </router-link>
                    <router-link to="/admin/dashboard/doctor" class="nav-link" active-class="active-link">
                        <i class="bi bi-person-badge me-2"></i> Doctor
                    </router-link>
                    <router-link to="/admin/dashboard/patient" class="nav-link" active-class="active-link">
                        <i class="bi bi-people-fill me-2"></i> Patient
                    </router-link>
                    <router-link to="/admin/dashboard/appointment" class="nav-link" active-class="active-link">
                        <i class="bi bi-calendar-check me-2"></i> Appointment
                    </router-link>
                    <router-link to="/admin/dashboard/department" class="nav-link" active-class="active-link">
                        <i class="bi bi-building me-2"></i> Department
                    </router-link>
                    <hr />
                    <a class="nav-link" href="#"><i class="bi bi-gear-fill me-2"></i> Settings</a>
                    <a class="nav-link" href="https://wa.me/919507444356" target="_blank"><i
                            class="bi bi-headset me-2"></i> Help Center</a>
                    <a class="nav-link logout-link" href="" @click.prevent="logoutUser">
                        <i class="bi bi-box-arrow-right me-2"></i> Logout
                    </a>
                </nav>
            </div>

            <div class="content" style="margin-left: 250px;">
                <nav
                    class="navbar navbar-light navbar-custom px-3 mb-2 d-flex justify-content-between align-items-center">
                    <span style="font-family: 'Poppins', sans-serif; font-weight: 500; font-size: 1.1rem; color: #333;">
                        Welcome, {{ layout_data.fullname }}
                    </span>

                    <div class="d-flex align-items-center gap-2">
                        <button class="btn btn-light rounded-4 p-2">
                            <i class="bi bi-envelope fs-5"></i>
                        </button>

                        <button class="btn btn-light rounded-4 p-2">
                            <i class="bi bi-bell fs-5"></i>
                        </button>

                        <div class="dropdown">
                            <button class="btn btn-light rounded-4 d-flex align-items-center px-2 py-1"
                                data-bs-toggle="dropdown">
                                <img :src="`https://ui-avatars.com/api/?name=${layout_data.fullname}&background=4084f6&color=ffffff&bold=true&size=128&rounded=true`"
                                    class="rounded-circle me-2" width="35" height="35" alt="avatar" />
                                <i class="bi bi-chevron-down" style="-webkit-text-stroke: 0.7px;"></i>
                            </button>
                            <ul class="dropdown-menu dropdown-menu-end">
                                <li>
                                    <h6 class="dropdown-header">{{ layout_data.fullname }}</h6>
                                </li>
                                <li><a class="dropdown-item" href="#">Edit Profile</a></li>
                                <li><a class="dropdown-item" href="#">Settings</a></li>
                                <li>
                                    <hr class="dropdown-divider">
                                </li>
                                <li><a class="dropdown-item text-danger" href="" @click.prevent="logoutUser">Logout</a>
                                </li>
                            </ul>
                        </div>

                        <button class="btn btn-light rounded-4 p-2">
                            <i class="bi bi-three-dots"></i>
                        </button>
                    </div>
                </nav>
                <router-view />
            </div>
        </div>
    </div>
    <div v-else class="alert alert-danger text-center">
        Please login to access Dashboard
    </div>
</template>

<!-- <style scoped>
.dashboard-body {
    font-family: 'Poppins', sans-serif;
    background-color: #f8fafc;
}

.sidebar {
    width: 250px;
    min-height: 100vh;
    background: #ffffff;
    border-right: 1px solid #e5e7eb;
    padding: 20px;
}

.sidebar h4 {
    font-weight: 700;
    color: #4084f6;
}

.sidebar .nav-link {
    color: #333;
    font-weight: 500;
    margin: 8px 0;
    border-radius: 10px;
    padding: 8px 10px;
    display: flex;
    align-items: center;
}

.sidebar .nav-link:hover,
.sidebar .nav-link.active-link {
    background: #eaf1ff;
    color: #4084f6;
    font-weight: 600;
}

.sidebar .logout-link {
    color: #dc3545;
    font-weight: 500;
}

.sidebar .logout-link:hover {
    background: #ffe5e9;
    color: #b02a37;
}

.content {
    flex: 1;
}

.navbar-custom {
    background: #fff;
    border-bottom: 1px solid #e5e7eb;
}
</style> -->

<style scoped>
.dashboard-body {
    font-family: 'Poppins', sans-serif;
    background-color: #f8fafc;
}

.sidebar {
    width: 250px;
    min-height: 100vh;
    background: #4084f6;
    padding: 20px;
    color: #fff;
}

.sidebar h4 {
    font-weight: 700;
    color: #ffffff;
}

.sidebar .nav-link {
    color: #ffffff;
    font-weight: 500;
    margin: 8px 0;
    border-radius: 10px;
    padding: 8px 10px;
    display: flex;
    align-items: center;
    transition: background 0.2s ease, transform 0.1s ease;
}

.sidebar .nav-link:hover,
.sidebar .nav-link.active-link {
    background: #ffffff;
    color: #4084f6;
    font-weight: 600;
    transform: scale(1.02);
}

.sidebar .logout-link {
    font-weight: 500;
}

.sidebar .logout-link:hover {
    background: #ffffff;
    color: red;
}

.content {
    flex: 1;
}

.navbar-custom {
    background: #fff;
    border-bottom: 1px solid #e5e7eb;
}
</style>
