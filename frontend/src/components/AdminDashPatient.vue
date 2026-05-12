<script>
import axios from 'axios';

export default {
    data() {
        return {
            jwt_token: "",
            admin_patient_data: [],
            searchText: ""
        }
    },
    methods: {
        async adminDashPatient() {
            try {
                const res = await axios.get("http://127.0.0.1:5000/api/admin_dash/patientPage", {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${this.jwt_token}`
                    }
                })
                this.admin_patient_data = res.data.patients
            } catch (err) {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/login")
            }
        },
        async adminUpdatePatientStatus(patient) {
            if (!confirm(`Are you sure you want to ${patient.status ? 'block' : 'unblock'} ${patient.fullname}`)) {
                return;
            }
            try {
                await axios.patch(`http://127.0.0.1:5000/api/admin_dash/patientPage/${patient.id}/status`, {}, {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${this.jwt_token}`
                    }
                })
                this.adminDashPatient()
            } catch (err) {
                alert("Failed to update status " + (err.response?.data?.msg || ""))
            }
        },
        async adminDeletePatient(patient) {
            if (!confirm(`Are you sure you want to delete patient ${patient.fullname}`)) {
                return;
            }
            try {
                await axios.delete(`http://127.0.0.1:5000/api/admin_dash/patientPage/${patient.id}/delete`, {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${this.jwt_token}`
                    }
                })
                this.adminDashPatient()
            } catch (err) {
                alert("Failed to delete patient " + (err.response?.data?.msg || ""))
            }
        }
    },
    mounted() {
        const jwt = localStorage.getItem("token");
        if (jwt) {
            this.jwt_token = jwt;
            this.adminDashPatient();
        } else {
            this.$router.push("/login");
            alert("Please login to access Dashboard.");
        }
    },
    computed: {
        patientFilter() {
            if (!this.searchText) {
                return this.admin_patient_data;
            }
            const q = this.searchText.toLowerCase();
            return this.admin_patient_data.filter(d =>
                d.fullname.toLowerCase().includes(q) ||
                (d.username && d.username.toLowerCase().includes(q)) ||
                (d.contact && d.contact.toLowerCase().includes(q))
            )
        }
    }
}
</script>

<template>
    <div v-if="jwt_token">
        <div class="d-flex dashboard-body">
            <div class="content px-4 py-3">
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
                                    <th class="text-muted">Email</th>
                                    <th class="text-muted">Age</th>
                                    <th class="text-muted">Gender</th>
                                    <th class="text-muted">Phone</th>
                                    <th class="text-muted">Visits</th>
                                    <th class="text-muted">Status</th>
                                    <th class="text-muted">Reg. Date</th>
                                    <th class="text-muted">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-if="!patientFilter || patientFilter.length === 0">
                                    <td colspan="9" class="text-center text-muted">No patient found</td>
                                </tr>
                                <tr v-for="patient in patientFilter" :key="patient.id">
                                    <td>{{ patient.fullname }}</td>
                                    <td>{{ patient.username }}</td>
                                    <td>{{ patient.age }}</td>
                                    <td>{{ patient.gender }}</td>
                                    <td>{{ patient.contact }}</td>
                                    <td>{{ patient.appointments }}</td>
                                    <td>
                                        <span class="badge rounded-pill" :class="patient.status ? 'bg-success' : 'bg-danger'">
                                            {{ patient.status ? 'Active' : 'Blocked' }}
                                        </span>
                                    </td>
                                    <td>{{ patient.registered_on }}</td>
                                    <td>
                                        <i class="bi"
                                            :class="patient.status ? 'bi-slash-circle text-danger me-2 fs-5' : 'bi-check-circle text-success me-2 fs-5'"
                                            style="cursor:pointer" @click="adminUpdatePatientStatus(patient)"></i>
                                            
                                        <i class="bi bi-trash3-fill text-danger fs-5" style="cursor:pointer" @click="adminDeletePatient(patient)"></i>
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