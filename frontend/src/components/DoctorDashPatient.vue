<script>
import axios from 'axios';

export default {
    data() {
        return {
            jwt_token: "",
            doctor_patient_data: [],
            searchText: ""
        }
    },
    methods: {
        async doctorDashPatient() {
            try {
                const res = await axios.get("http://127.0.0.1:5000/api/doctor_dash/patientPage", {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${this.jwt_token}`
                    }
                })
                this.doctor_patient_data = res.data.patients
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
            this.doctorDashPatient();
        } else {
            this.$router.push("/login");
            alert("Please login to access Dashboard.");
        }
    },
    computed: {
        patientSearch() {
            if (!this.searchText) {
                return this.doctor_patient_data
            }
            const q = this.searchText.toLowerCase()
            return this.doctor_patient_data.filter(d => d.fullname && d.fullname.toLowerCase().includes(q))
        }
    }
}
</script>

<template>
    <div v-if="jwt_token">
        <div class="d-flex dashboard-body px-4 py-1">
            <div class="content">
                <!-- <div class="d-flex justify-content-end mb-3">
                    <button class="btn btn-outline-secondary">
                        <i class="bi bi-upload me-1"></i> Export to CSV
                    </button>
                </div> -->
                <div class="card card-custom p-3">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h6 class="fw-bold">
                            <i class="bi bi-people-fill me-2"></i>Patient List
                        </h6>
                        <div>
                            <label class="me-2 text-muted">Search:</label>
                            <input type="text" v-model="searchText" class="form-control form-control-sm d-inline-block"
                                style="width: 200px;">
                        </div>
                    </div>
                    <div class="table-responsive">
                        <table class="table align-middle">
                            <thead>
                                <tr>
                                    <th class="text-muted">Name</th>
                                    <th class="text-muted">Age</th>
                                    <th class="text-muted">Gender</th>
                                    <th class="text-muted">Phone</th>
                                    <th class="text-muted">Last Visits</th>
                                    <th class="text-muted">Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-if="!patientSearch || patientSearch.length === 0">
                                    <td colspan="5" class="text-center text-muted">No patient found</td>
                                </tr>
                                <tr v-for="patient in patientSearch" :key="patient.patient_id">
                                    <td>{{ patient.fullname }}</td>
                                    <td>{{ patient.age }}</td>
                                    <td>{{ patient.gender }}</td>
                                    <td>{{ patient.phone }}</td>
                                    <td>{{ patient.latest_appointment }}</td>
                                    <td>
                                        <span class="badge rounded-pill bg-success">{{ patient.status }}</span>
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

.btn:hover {
    transform: scale(1.03);
    transition: 0.2s ease-in-out;
}
</style>