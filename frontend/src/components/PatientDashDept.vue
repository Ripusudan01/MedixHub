<script>
import axios from 'axios';

export default {
    data() {
        return {
            jwt_token: "",
            patient_dept_data: []
        }
    },
    methods: {
        async patientDashDept() {
            try {
                const res = await axios.get("http://127.0.0.1:5000/api/patient_dash/deptPage", {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${this.jwt_token}`
                    }
                })
                this.patient_dept_data = res.data.department
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
            this.patientDashDept();
        } else {
            this.$router.push("/login");
            alert("Please login to access Dashboard.");
        }
    }
}
</script>

<template>
    <div v-if="jwt_token">
        <div class="d-flex dashboard-body px-4 py-3">
            <div class="content">
                <!-- <div class="d-flex justify-content-end mb-3">
                    <button class="btn btn-outline-secondary">
                        <i class="bi bi-upload me-1"></i> Export to CSV
                    </button>
                </div> -->

                <div class="card card-custom p-3">
                    <h6 class="mb-3 fw-bold"><i class="bi bi-diagram-3 me-2"></i>Department List</h6>
                    <div class="table-responsive">
                        <table class="table align-middle">
                            <thead>
                                <tr>
                                    <th class="text-muted">Name</th>
                                    <th class="text-muted">Total Doctors</th>
                                    <th class="text-muted">Description</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-if="!patient_dept_data || patient_dept_data.length === 0">
                                    <td colspan="3" class="text-center text-muted">No department found</td>
                                </tr>
                                <tr v-for="dept in patient_dept_data" :key="dept.id">
                                    <td>{{ dept.name }}</td>
                                    <td>{{ dept.doctorCount }}</td>
                                    <td>{{ dept.description }}</td>
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
</style>