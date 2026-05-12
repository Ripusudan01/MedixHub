<script>
import axios from 'axios';

export default {
    data() {
        return {
            jwt_token: "",
            admin_data: {}
        }
    },
    methods: {
        async adminDashHome() {
            try {
                const res = await axios.get("http://127.0.0.1:5000/api/admin_dash/homePage", {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${this.jwt_token}`
                    }
                })
                this.admin_data = res.data
            } catch (err) {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/login")
            }
        }
    },
    mounted() {
        const jwt = localStorage.getItem("token");
        if (jwt) {
            this.jwt_token = jwt;
            this.adminDashHome();
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
            <div class="content px-4 py-3">
                <!-- <div class="d-flex justify-content-between align-items-center mb-4">
                    <div class="btn btn-light border">
                        <i class="bi bi-calendar-check me-2"></i> Last Update: Oct 2025 - Nov 2025
                    </div>
                    <button class="btn text-white shadow-sm report-button" style="background-color: #4084f6; border-radius: 0.5rem;">
                        <i class="bi bi-file-earmark-text me-1"></i> Generate Report
                    </button>
                </div> -->

                <div class="row g-4 mb-4">
                    <div class="col-md-4">
                        <div class="card card-custom p-3">
                            <h6 class="fw-bold"><i class="bi bi-person-fill me-2"></i>Total Users</h6>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Patients</span>
                                <span>{{ admin_data.total_patients }}</span>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Doctors</span>
                                <span>{{ admin_data.total_doctors }}</span>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Others</span>
                                <span>5</span>
                            </div>
                        </div>
                    </div>

                    <div class="col-md-4">
                        <div class="card card-custom p-3">
                            <h6 class="fw-bold"><i class="bi bi-calendar me-2"></i>Appointments</h6>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Today</span>
                                <span>{{ admin_data.upcoming_appointments_count }}</span>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Completed</span>
                                <span>{{ admin_data.completed_appointments_count }}</span>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Cancelled</span>
                                <span>{{ admin_data.cancelled_appointments_count }}</span>
                            </div>
                        </div>
                    </div>

                    <div class="col-md-4">
                        <div class="card card-custom p-3">
                            <h6 class="fw-bold"><i class="bi bi-currency-rupee me-2"></i>Revenue</h6>
                            <div class="d-flex justify-content-between"><span
                                    class="text-muted">Consultation</span><span>40,000</span>
                            </div>
                            <div class="d-flex justify-content-between"><span
                                    class="text-muted">Medicine</span><span>32,500</span>
                            </div>
                            <div class="d-flex justify-content-between"><span
                                    class="text-muted">Tests</span><span>15,450</span></div>
                        </div>
                    </div>
                </div>

                <div class="card card-custom p-3">
                    <h6 class="mb-3 fw-bold"><i class="bi bi-people-fill me-2"></i>Recent Users</h6>
                    <div class="table-responsive">
                        <table class="table align-middle">
                            <thead>
                                <tr>
                                    <th class="text-muted">#</th>
                                    <th class="text-muted">Fullname</th>
                                    <th class="text-muted">Role</th>
                                    <th class="text-muted">Reg. Date</th>
                                    <th class="text-muted">Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-if="!admin_data.recent_5_user || admin_data.recent_5_user.length === 0">
                                    <td colspan="5" class="text-center text-muted">No recent users found</td>
                                </tr>
                                <tr v-else v-for="(user, index) in admin_data.recent_5_user" :key="user.user_id">
                                    <td>{{ index + 1 }}</td>
                                    <td>{{ user.name }}</td>
                                    <td>{{ user.role.charAt(0).toUpperCase() + user.role.slice(1) }}</td>
                                    <td>{{ user.registered_on }}</td>
                                    <td>
                                        <span class="badge rounded-pill" :class="user.status ? 'bg-success' : 'bg-danger'">
                                            {{ user.status ? 'Active' : 'Blocked' }}
                                        </span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="alert alert-danger text-center" v-else>
        Please login to access Dashboard
    </div>
</template>

<style scoped>
.dashboard-body {
    font-family: 'Poppins', sans-serif;
    background-color: #f8fafc;
}

.content {
    flex: 1;
    /* padding: 20px; */
}

.card-custom {
    border-radius: 16px;
    border: none;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.report-button:hover {
    transform: scale(1.03);
    transition: 0.2s ease-in-out;
}
</style>