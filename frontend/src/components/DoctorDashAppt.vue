<script>
import axios from 'axios';

export default {
    data() {
        return {
            jwt_token: "",
            doctor_appt_data: [],
            selectedAppt: null,
            addTreatment: { diagnosis: "", prescription: "", notes: "" }
        }
    },
    methods: {
        async doctorDashAppt() {
            try {
                const res = await axios.get("http://127.0.0.1:5000/api/doctor_dash/apptPage", {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${this.jwt_token}`
                    }
                })
                this.doctor_appt_data = res.data.appointments
            } catch (err) {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/login")
            }
        },
        async doctorDashCancelAppt(apptId) {
            if (!confirm("Are you sure you want to cancel this appointment?")) {
                return;
            }
            try {
                const res = await axios.put(`http://127.0.0.1:5000/api/appt/cancel/${apptId}`, {}, {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${this.jwt_token}`
                    }
                })
                // alert("Appointment cancelled successfully!");
                this.doctorDashAppt()
            } catch (err) {
                alert(err.response?.data?.msg || "Failed to cancel appointment")
            }
        },
        openTreatmentModal(appt) {
            this.selectedAppt = appt
            const modal = new bootstrap.Modal(document.getElementById("viewTreatmentModal"));
            modal.show();
        },
        openAddTreatmentModal(appt) {
            this.selectedAppt = appt
            this.addTreatment = { diagnosis: "", prescription: "", notes: "" }
            const modal = new bootstrap.Modal(document.getElementById("addTreatmentModal"))
            modal.show()
        },
        async doctorAddTreatment(appt_id) {
            try {
                const res = await axios.post(`http://127.0.0.1:5000/api/doctor_dash/apptPage/${appt_id}/treatment`,
                    this.addTreatment,
                    {
                        headers: {
                            "Content-Type": "application/json",
                            "Authorization": `Bearer ${this.jwt_token}`
                        }
                    })
                this.doctorDashAppt()
                this.addTreatment = { diagnosis: "", prescription: "", notes: "" }
                const modal = bootstrap.Modal.getInstance(document.getElementById("addTreatmentModal"))
                modal.hide()
            } catch (err) {
                alert("Failed to add " + (err.response?.data?.msg || ""));
                this.addTreatment = { diagnosis: "", prescription: "", notes: "" }
            }
        }

    },
    mounted() {
        const jwt = localStorage.getItem("token");
        if (jwt) {
            this.jwt_token = jwt;
            this.doctorDashAppt();
        } else {
            this.$router.push("/login");
            alert("Please login to access Dashboard.");
        }
    }
}
</script>

<template>
    <div v-if="jwt_token">
        <div class="container mt-4 px-4">

            <!-- Booked -->
            <div v-if="doctor_appt_data.filter(a => a.status === 'Booked').length">
                <h5 class="mb-3">Booked Appointments</h5>
                <div v-for="appt in doctor_appt_data.filter(a => a.status === 'Booked')" :key="appt.id"
                    class="card shadow-sm p-3 mb-4">
                    <div class="row g-3 align-items-center">
                        <div class="col-md-2 text-center">
                            <img src="https://randomuser.me/api/portraits/men/20.jpg"
                                class="rounded-circle img-fluid border" alt="Patient">
                        </div>
                        <div class="col-md-7">
                            <h5 class="fw-bold">{{ appt.patientName }}</h5>
                            <p class="mb-0"><strong>Date & Time:</strong> {{ appt.date }} | {{ appt.time }}</p>
                            <p class="mb-0">
                                <strong class="me-1">Status:</strong>
                                <span class="badge rounded-pill bg-primary"> {{ appt.status }}</span>
                            </p>
                        </div>
                        <div class="col-md-3 text-end">
                            <button class="btn btn-primary btn-sm mb-2 w-100 shadow-sm"
                                @click="openAddTreatmentModal(appt)">Add Treatment</button>
                            <button class="btn btn-outline-danger btn-sm w-100 shadow-sm"
                                @click="doctorDashCancelAppt(appt.id)">Cancel Appointment</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Completed -->
            <div v-if="doctor_appt_data.filter(a => a.status === 'Completed').length">
                <h5 class="mb-3">Completed Appointments</h5>
                <div v-for="appt in doctor_appt_data.filter(a => a.status === 'Completed')" :key="appt.id"
                    class="card shadow-sm p-3 mb-4">
                    <div class="row g-3 align-items-center">
                        <div class="col-md-2 text-center">
                            <img src="https://randomuser.me/api/portraits/men/20.jpg"
                                class="rounded-circle img-fluid border" alt="Patient">
                        </div>
                        <div class="col-md-7">
                            <h5 class="fw-bold">{{ appt.patientName }}</h5>
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

            <!-- Cancelled -->
            <div v-if="doctor_appt_data.filter(a => a.status === 'Cancelled').length">
                <h5 class="mb-3">Cancelled Appointments</h5>
                <div v-for="appt in doctor_appt_data.filter(a => a.status === 'Cancelled')" :key="appt.id"
                    class="card shadow-sm p-3 mb-4">
                    <div class="row g-3 align-items-center">
                        <div class="col-md-2 text-center">
                            <img src="https://randomuser.me/api/portraits/men/20.jpg"
                                class="rounded-circle img-fluid border" alt="Patient">
                        </div>
                        <div class="col-md-7">
                            <h5 class="fw-bold">{{ appt.patientName }}</h5>
                            <p class="mb-0"><strong>Date & Time:</strong> {{ appt.date }} | {{ appt.time }}</p>
                            <p class="mb-0">
                                <strong class="me-1">Status:</strong>
                                <span class="badge rounded-pill bg-danger">{{ appt.status }}</span>
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="doctor_appt_data.length === 0" class="alert alert-secondary text-center">
                No appointments found
            </div>

            <!-- Treatment Modal -->
            <div class="modal fade" id="viewTreatmentModal" tabindex="-1" aria-hidden="true">
                <div class="modal-dialog modal-lg modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Treatment Details</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <h6 class="fw-bold">{{ selectedAppt?.patientName }}</h6>
                            <p><strong>Date & Time:</strong> {{ selectedAppt?.date }} | {{ selectedAppt?.time }}</p>
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

            <!-- Add Treatment Modal -->
            <div class="modal fade" id="addTreatmentModal" tabindex="-1" aria-hidden="true">
                <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title w-100 text-center">Add Treatment</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <form @submit.prevent="doctorAddTreatment(selectedAppt.id)">
                                <div class="mb-3">
                                    <label class="form-label">Diagnosis</label>
                                    <textarea v-model="addTreatment.diagnosis" class="form-control" required></textarea>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Prescription</label>
                                    <textarea v-model="addTreatment.prescription" class="form-control"
                                        required></textarea>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Notes</label>
                                    <textarea v-model="addTreatment.notes" class="form-control" required></textarea>
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
    </div>

    <div v-else class="alert alert-danger text-center">
        Please login to access Dashboard
    </div>
</template>