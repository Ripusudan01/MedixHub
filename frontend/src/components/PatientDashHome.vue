<script>
import axios from 'axios';

export default {
    data() {
        return {
            jwt_token: "",
            patient_data: {},
            isCsvCompleted: false
        }
    },
    methods: {
        async patientDashHome() {
            try {
                const res = await axios.get("http://127.0.0.1:5000/api/patient_dash/homePage", {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${this.jwt_token}`
                    }
                })
                this.patient_data = res.data
                // console.log(res.data)
            } catch (err) {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/login")
            }
        },
        async exportCsvReport() {
            try {
                this.isCsvCompleted = true;
                const userId = this.$route.params.id

                const res = await axios.get(`http://127.0.0.1:5000/api/patient_export_csv/${userId}`);
                const taskId = res.data.task_id;

                setTimeout(() => {
                    window.location.href = `http://127.0.0.1:5000/api/csv_result/${taskId}`;
                    this.isCsvCompleted = false;
                }, 3000);
            } catch (err) {
                // console.log(err)
                this.isCsvCompleted = false;
                alert("Failed to generate report.");
            }
        }
    },
    mounted() {
        const jwt = localStorage.getItem("token");
        if (jwt) {
            this.jwt_token = jwt;
            this.patientDashHome();
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
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <div class="btn btn-light border">
                        <i class="bi bi-calendar-check me-2"></i> Last Update: Oct 2025 - Nov 2025
                    </div>
                    <button class="btn text-white shadow-sm report-button" :disabled="isCsvCompleted"
                        @click="exportCsvReport" style="background-color: #4084f6; border-radius: 0.5rem;">
                        <i class="bi bi-file-earmark-text me-1"></i> Generate Report
                    </button>
                </div>
                <div class="row g-4 mb-4">
                    <div class="col-md-4">
                        <div class="card card-custom p-3">
                            <h6 class="fw-bold"><i class="bi bi-file-earmark-text me-2"></i>Recent Treatment</h6>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Medicine</span>
                                <span>{{ patient_data.recent_treatment?.medicine || 'NA' }}</span>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Diagnosis</span>
                                <span>{{ patient_data.recent_treatment?.diagnosis || 'NA' }}</span>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Date</span>
                                <span>{{ patient_data.recent_treatment?.date || 'NA' }}</span>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Doctor</span>
                                <span>{{ patient_data.recent_treatment?.doctor || 'NA' }}</span>
                            </div>
                        </div>
                    </div>

                    <div class="col-md-4">
                        <div class="card card-custom p-3">
                            <h6 class="fw-bold"><i class="bi bi-calendar-check me-2"></i>Next Appointment</h6>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Date</span>
                                <span>{{ patient_data.next_appointment?.date || 'NA' }}</span>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Doctor</span>
                                <span>{{ patient_data.next_appointment?.doctor || 'NA' }}</span>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Department</span>
                                <span>{{ patient_data.next_appointment?.department || 'NA' }}</span>
                            </div>
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="text-muted">Status</span>
                                <span
                                    class="badge rounded-pill bg-primary d-flex align-items-center justify-content-center">
                                    {{ patient_data.next_appointment?.status || 'NA' }}
                                </span>
                            </div>
                        </div>
                    </div>

                    <div class="col-md-4">
                        <div class="card card-custom p-3">
                            <h6 class="fw-bold"><i class="bi bi-bar-chart-fill me-2"></i>Health Stats</h6>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Blood Pressure</span>
                                <span>120/80</span>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Height</span>
                                <span>6 feet</span>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Weight</span>
                                <span>80 kg</span>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Heart Rate</span>
                                <span>60 bpm</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card card-custom p-3">
                    <h6 class="mb-3 fw-bold"><i class="bi bi-calendar-plus me-2"></i>Recent Appointments</h6>
                    <div class="table-responsive">
                        <table class="table align-middle">
                            <thead>
                                <tr>
                                    <th class="text-muted">#</th>
                                    <th class="text-muted">Date</th>
                                    <th class="text-muted">Doctor</th>
                                    <th class="text-muted">Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr
                                    v-if="!patient_data.recent_appointments || patient_data.recent_appointments.length === 0">
                                    <td colspan="4" class="text-center text-muted">No recent appointments found</td>
                                </tr>
                                <tr v-else v-for="(appt, index) in patient_data.recent_appointments"
                                    :key="appt.appointment_id">
                                    <td>{{ index + 1 }}</td>
                                    <td>{{ appt.date }}</td>
                                    <td>{{ appt.doctor }}</td>
                                    <td>
                                        <span class="badge rounded-pill" :class="{
                                            'bg-primary': appt.status === 'Booked',
                                            'bg-success': appt.status === 'Completed',
                                            'bg-danger': appt.status === 'Cancelled'
                                        }">
                                            {{ appt.status }}
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