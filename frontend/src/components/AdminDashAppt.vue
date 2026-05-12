<script>
import axios from 'axios';

export default {
    data() {
        return {
            jwt_token: "",
            admin_appt_data: [],
            searchText: "",
            selectedAppt: null
        }
    },
    methods: {
        async adminDashAppt() {
            try {
                const res = await axios.get("http://127.0.0.1:5000/api/admin_dash/appointmentPage", {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${this.jwt_token}`
                    }
                })
                this.admin_appt_data = res.data.appointments
            } catch (err) {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/login")
            }
        },
        viewTreatmentModal(appt) {
            this.selectedAppt = appt
            const modal = new bootstrap.Modal(document.getElementById("viewTreatmentModal"));
            modal.show();
        }
    },
    mounted() {
        const jwt = localStorage.getItem("token");
        if (jwt) {
            this.jwt_token = jwt;
            this.adminDashAppt();
        } else {
            this.$router.push("/login");
            alert("Please login to access Dashboard.");
        }
    },
    computed: {
        apptFilter() {
            if (!this.searchText) return this.admin_appt_data;
            const q = this.searchText.toLowerCase();
            return this.admin_appt_data.filter(appt =>
                (appt.patient?.name && appt.patient.name.toLowerCase().includes(q)) ||
                (appt.doctor?.name && appt.doctor.name.toLowerCase().includes(q)) ||
                (appt.doctor?.department && appt.doctor.department.toLowerCase().includes(q)) ||
                (appt.status && appt.status.toLowerCase().includes(q))
            );
        }
    }
}
</script>

<template>
    <div v-if="jwt_token">
        <div class="d-flex dashboard-body">
            <div class="content px-4 py-3">
                <!-- <div class="d-flex justify-content-between align-items-center mb-4">
                    <button class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#addDeptModal">
                        <i class="bi bi-building-add me-1"></i>Department
                    </button>
                    <button class="btn btn-outline-secondary">
                        <i class="bi bi-upload me-1"></i> Export to CSV
                    </button>
                </div> -->

                <div class="card card-custom p-3">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h6 class="fw-bold">
                            <i class="bi bi-calendar me-2"></i>Appointment List
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
                                    <th class="text-muted">Date</th>
                                    <th class="text-muted">Time</th>
                                    <th class="text-muted">Patient Name</th>
                                    <th class="text-muted">Doctor Name</th>
                                    <th class="text-muted">Department</th>
                                    <th class="text-muted">Status</th>
                                    <th class="text-muted">Details</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-if="!apptFilter || apptFilter.length === 0">
                                    <td colspan="7" class="text-center text-muted">No appointment found</td>
                                </tr>
                                <tr v-for="appt in apptFilter" :key="appt.appointment_id">
                                    <td>{{ appt.date }}</td>
                                    <td>{{ appt.time }}</td>
                                    <td>{{ appt.patient.name }}</td>
                                    <td>{{ appt.doctor.name }}</td>
                                    <td>{{ appt.doctor.department }}</td>
                                    <td>
                                        <span :class="{
                                            'badge rounded-pill bg-success': appt.status === 'Completed',
                                            'badge rounded-pill bg-primary': appt.status === 'Booked',
                                            'badge rounded-pill bg-danger': appt.status === 'Cancelled'
                                        }">
                                            {{ appt.status }}
                                        </span>
                                    </td>
                                    <td>
                                        <button
                                            class="btn btn-outline-primary rounded-pill px-3 py-1 shadow-sm d-flex align-items-center gap-2" @click="viewTreatmentModal(appt)">
                                            <i class="bi bi-info-circle"></i> <span>Details</span>
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <div class="modal fade" id="viewTreatmentModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title w-100 text-center">Appointment Details</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <p><strong>Doctor:</strong> {{ selectedAppt?.doctor?.name }}</p>
                        <p><strong>Patient:</strong> {{ selectedAppt?.patient?.name }}</p>
                        <p><strong>Date & Time:</strong> {{ selectedAppt?.date }} | {{ selectedAppt?.time }}</p>
                        <p><strong>Contact:</strong> +91 {{ selectedAppt?.patient?.contact || 'N/A' }}</p>
                        <hr>
                        <p><strong>Diagnosis:</strong> {{ selectedAppt?.treatment?.diagnosis || 'Not Available' }}
                        </p>
                        <p><strong>Prescription:</strong>
                            {{ selectedAppt?.treatment?.prescription || 'Not Available' }}
                        </p>
                        <p><strong>Notes:</strong> {{ selectedAppt?.treatment?.notes || 'No additional notes' }}</p>
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