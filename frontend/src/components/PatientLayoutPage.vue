<script>
import axios from 'axios'

export default {
    data() {
        return {
            jwt_token: "",
            layout_data: {},
            userId: this.$route.params.id,
            editProfile: { fullname: "", age: "", ph_number: "", gender: "" }
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
                this.editProfile.fullname = res.data.fullname || "";
                this.editProfile.age = res.data.age || "";
                this.editProfile.ph_number = res.data.ph_number || "";
            } catch (err) {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/login")
            }
        },
        async updateProfile() {
            try {
                await axios.put(
                    "http://127.0.0.1:5000/api/patient_dash/editProfile",
                    this.editProfile,
                    {
                        headers: {
                            "Content-Type": "application/json",
                            "Authorization": `Bearer ${this.jwt_token}`
                        }
                    }
                );
                // alert("Profile updated successfully!");
                this.fetchLayoutData();
                const modal = bootstrap.Modal.getInstance(document.getElementById("editProfileModal"));
                modal.hide();
            } catch (err) {
                alert("Failed to update profile " + (err.response?.data?.msg || ""));
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
                    <router-link :to="`/patient/${userId}/dashboard`" class="nav-link" exact-active-class="active-link">
                        <i class="bi bi-grid me-2"></i> Dashboard
                    </router-link>
                    <router-link :to="`/patient/${userId}/dashboard/doctor`" class="nav-link"
                        active-class="active-link">
                        <i class="bi bi-person-badge me-2"></i> Doctor
                    </router-link>
                    <router-link :to="`/patient/${userId}/dashboard/appointment`" class="nav-link"
                        active-class="active-link">
                        <i class="bi bi-calendar-check me-2"></i> Appointment
                    </router-link>
                    <router-link :to="`/patient/${userId}/dashboard/department`" class="nav-link"
                        active-class="active-link">
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
                                <li><a class="dropdown-item" data-bs-toggle="modal"
                                        data-bs-target="#editProfileModal">Edit Profile</a></li>
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
        <!-- Edit Profile Modal -->
        <div class="modal fade" id="editProfileModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title w-100 text-center">Edit Profile</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="updateProfile">
                            <div class="mb-3">
                                <label class="form-label">Full Name</label>
                                <input type="text" v-model="editProfile.fullname" class="form-control" />
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Age</label>
                                <input type="number" v-model="editProfile.age" class="form-control" />
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Phone Number</label>
                                <input type="text" v-model="editProfile.ph_number" class="form-control" />
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Gender</label>
                                <select v-model="editProfile.gender" class="form-select">
                                    <option value="" disabled>Select Gender</option>
                                    <option value="Male">Male</option>
                                    <option value="Female">Female</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
                            <button type="submit" class="btn btn-primary w-100">
                                <i class="bi bi-check-circle me-1"></i> Save
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div v-else class="alert alert-danger text-center">
        Please login to access Dashboard
    </div>
</template>

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