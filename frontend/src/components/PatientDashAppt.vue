<script>
import axios from 'axios';

export default {
    data() {
        return {
            jwt_token: "",
            patient_appt_data: [],
            selectedAppt: null
        }
    },
    methods: {
        async patientDashAppt() {
            try {
                const res = await axios.get("http://127.0.0.1:5000/api/patient_dash/apptPage", {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${this.jwt_token}`
                    }
                })
                this.patient_appt_data = res.data.appointments
            } catch (err) {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/login")
            }
        },
        async patientDashCancelAppt(apptId) {
            try {
                const res = await axios.put(`http://127.0.0.1:5000/api/appt/cancel/${apptId}`, {}, {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${this.jwt_token}`
                    }
                })
                alert("Appointment cancelled successfully!");
                this.patientDashAppt()
            } catch (err) {
                alert(err.response?.data?.msg || "Failed to cancel appointment")
            }
        },
        openTreatmentModal(appt) {
            this.selectedAppt = appt
            const modal = new bootstrap.Modal(document.getElementById("treatmentModal"));
            modal.show();
        }
    },
    mounted() {
        const jwt = localStorage.getItem("token");
        if (jwt) {
            this.jwt_token = jwt;
            this.patientDashAppt();
        } else {
            this.$router.push("/login");
            alert("Please login to access Dashboard.");
        }
    }
}
</script>

<template>
    <div v-if="jwt_token">
        <div class="container px-4 py-3">
            <!-- Booked -->
            <div v-if="patient_appt_data.filter(a => a.status === 'Booked').length">
                <h5 class="mb-3">Booked Appointments</h5>
                <div v-for="appt in patient_appt_data.filter(a => a.status === 'Booked')" :key="appt.id"
                    class="card shadow-sm p-3 mb-4">
                    <div class="row g-3 align-items-center">
                        <div class="col-md-2 text-center">
                            <img src="https://cdn.pixabay.com/photo/2023/12/21/06/23/doctor-8461303_960_720.jpg"
                                class="rounded-circle img-fluid border" alt="Doctor">
                        </div>
                        <div class="col-md-7">
                            <h5 class="fw-bold">{{ appt.doctorName }}</h5>
                            <p class="text-muted mb-1">{{ appt.specialization }}</p>
                            <p class="mb-1"><strong>Address:</strong> Andheri East, Mumbai - 400051, India</p>
                            <p class="mb-0"><strong>Date & Time:</strong> {{ appt.date }} | {{ appt.time }}</p>
                            <p class="mb-0">
                                <strong class="me-1">Status:</strong>
                                <span class="badge rounded-pill bg-primary">{{ appt.status }}</span>
                            </p>
                        </div>
                        <div class="col-md-3 text-end">
                            <button class="btn btn-primary btn-sm mb-2 w-100 shadow-sm">Pay Online</button>
                            <button class="btn btn-outline-danger btn-sm w-100 shadow-sm"
                                @click="patientDashCancelAppt(appt.id)">Cancel Appointment</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Completed -->
            <div v-if="patient_appt_data.filter(a => a.status === 'Completed').length">
                <h5 class="mb-3">Completed Appointments</h5>
                <div v-for="appt in patient_appt_data.filter(a => a.status === 'Completed')" :key="appt.id"
                    class="card shadow-sm p-3 mb-4">
                    <div class="row g-3 align-items-center">
                        <div class="col-md-2 text-center">
                            <img src="https://cdn.pixabay.com/photo/2023/12/21/06/23/doctor-8461303_960_720.jpg"
                                class="rounded-circle img-fluid border" alt="Doctor">
                        </div>
                        <div class="col-md-7">
                            <h5 class="fw-bold">{{ appt.doctorName }}</h5>
                            <p class="text-muted mb-1">{{ appt.specialization }}</p>
                            <p class="mb-1"><strong>Address:</strong> Andheri East, Mumbai - 400051, India</p>
                            <p class="mb-0"><strong>Date & Time:</strong> {{ appt.date }} | {{ appt.time }}</p>
                            <p class="mb-0">
                                <strong class="me-1">Status:</strong>
                                <span class="badge rounded-pill bg-success">{{ appt.status }}</span>
                            </p>
                        </div>
                        <div class="col-md-3 text-end">
                            <button class="btn btn-primary btn-sm w-100 shadow-sm" @click="openTreatmentModal(appt)">
                                See Details
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="modal fade" id="treatmentModal" tabindex="-1" aria-hidden="true">
                <div class="modal-dialog modal-lg modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Treatment Details</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <h6 class="fw-bold">{{ selectedAppt?.doctorName }}</h6>
                            <p><strong>Date & Time:</strong> {{ selectedAppt?.date }} | {{ selectedAppt?.time }}</p>
                            <hr>
                            <p><strong>Diagnosis:</strong> {{ selectedAppt?.treatment?.diagnosis || 'Not Available' }}
                            </p>
                            <p>
                                <strong>Prescription:</strong> {{ selectedAppt?.treatment?.prescription || 'Not Available' }}
                            </p>
                            <p>
                                <strong>Notes:</strong> {{ selectedAppt?.treatment?.notes || 'No additional notes' }}
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Cancelled -->
            <div v-if="patient_appt_data.filter(a => a.status === 'Cancelled').length">
                <h5 class="mb-3">Cancelled Appointments</h5>
                <div v-for="appt in patient_appt_data.filter(a => a.status === 'Cancelled')" :key="appt.id"
                    class="card shadow-sm p-3 mb-4">
                    <div class="row g-3 align-items-center">
                        <div class="col-md-2 text-center">
                            <img src="https://cdn.pixabay.com/photo/2023/12/21/06/23/doctor-8461303_960_720.jpg"
                                class="rounded-circle img-fluid border" alt="Doctor">
                        </div>
                        <div class="col-md-7">
                            <h5 class="fw-bold">{{ appt.doctorName }}</h5>
                            <p class="text-muted mb-1">{{ appt.specialization }}</p>
                            <p class="mb-1"><strong>Address:</strong> Andheri East, Mumbai - 400051, India</p>
                            <p class="mb-0"><strong>Date & Time:</strong> {{ appt.date }} | {{ appt.time }}</p>
                            <p class="mb-0">
                                <strong class="me-1">Status:</strong>
                                <span class="badge rounded-pill bg-danger">{{ appt.status }}</span>
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="patient_appt_data.length === 0" class="alert alert-secondary text-center">
                No appointments found
            </div>
        </div>
    </div>

    <div class="alert alert-danger text-center" v-else>
        Please login to access Dashboard
    </div>
</template>