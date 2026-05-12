<script>
import axios from 'axios';

export default {
    data() {
        return {
            jwt_token: "",
            patient_doctor_data: [],
            searchText: "",
            selectedDoctor: null,
            selectedSlot: null
        }
    },
    methods: {
        async patientDashDoctor() {
            try {
                const res = await axios.get("http://127.0.0.1:5000/api/patient_dash/doctorPage", {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${this.jwt_token}`
                    }
                })
                this.patient_doctor_data = res.data.doctors
            } catch (err) {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/login")
            }
        },
        openDoctorSlotModal(doctor) {
            this.selectedDoctor = doctor;
            this.selectedSlot = null;
            const modal = new bootstrap.Modal(document.getElementById("doctorModal"));
            modal.show();
        },
        selectSlot(date, time) {
            this.selectedSlot = { date, time };
        },
        async confirmBooking() {
            try {
                await axios.post("http://127.0.0.1:5000/api/patient_dash/doctorPage", {
                    doctor_id: this.selectedDoctor.id,
                    date: this.selectedSlot.date,
                    time: this.selectedSlot.time.start
                }, {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${this.jwt_token}`
                    }
                });
                alert('Appointment booked successfully!');
                const modal = bootstrap.Modal.getInstance(document.getElementById("doctorModal"))
                modal.hide()
                this.$router.push(`/patient/${this.$route.params.id}/dashboard/appointment`);
            } catch (err) {
                alert("Booking failed " + err.response?.data?.msg || "");
            }
        }
    },
    mounted() {
        const jwt = localStorage.getItem("token");
        if (jwt) {
            this.jwt_token = jwt;
            this.patientDashDoctor();
        } else {
            this.$router.push("/login");
            alert("Please login to access Dashboard.");
        }
    },
    computed: {
        doctorSearch() {
            if (!this.searchText) {
                return this.patient_doctor_data;
            }
            const q = this.searchText.toLowerCase();
            return this.patient_doctor_data.filter(d =>
                d.fullname.toLowerCase().includes(q) ||
                (d.specialization && d.specialization.toLowerCase().includes(q))
            );
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
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h6 class="fw-bold">
                            <i class="bi bi-heart-pulse-fill me-2"></i>Doctor List
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
                                    <th class="text-muted">Specialization</th>
                                    <th class="text-muted">Department</th>
                                    <th class="text-muted">Availability</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-if="!doctorSearch || doctorSearch.length === 0">
                                    <td colspan="4" class="text-center text-muted">No doctor found</td>
                                </tr>
                                <tr v-for="doctor in doctorSearch" :key="doctor.id">
                                    <td>{{ doctor.fullname }}</td>
                                    <td>{{ doctor.specialization }}</td>
                                    <td>{{ doctor.department }}</td>
                                    <td>
                                        <button
                                            class="btn btn-outline-primary rounded-pill px-3 py-1 shadow-sm d-flex align-items-center gap-2"
                                            @click="openDoctorSlotModal(doctor)">
                                            <i class="bi bi-calendar-check"></i>
                                            <span>View Slots</span>
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- View Slot Modal -->
        <div class="modal fade" id="doctorModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable modal-lg">
                <div class="modal-content">
                    <div class="modal-header flex-column text-center">
                        <h5 class="modal-title fw-bold mb-1" v-if="selectedDoctor">
                            {{ selectedDoctor.fullname }}
                            <span class="text-muted"> - {{ selectedDoctor.specialization }}</span>
                        </h5>
                        <small class="text-muted">
                            Department: {{ selectedDoctor?.department }} •
                            Fee: ₹500 •
                            Experience: 5+ yrs
                        </small>
                        <button type="button" class="btn-close position-absolute end-0 top-0 m-3"
                            data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div v-if="selectedDoctor">
                            <div
                                v-if="selectedDoctor.availability && Object.values(selectedDoctor.availability).some(slots => slots.length > 0)">
                                <div v-for="(slots, date) in selectedDoctor.availability" :key="date">
                                    <div v-if="slots.length > 0" class="mb-2">
                                        <strong class="me-2">{{ date }}:</strong>
                                        <button v-for="slot in slots" :key="slot.start" class="btn btn-sm me-2 mb-2"
                                            :class="selectedSlot && selectedSlot.date === date && selectedSlot.time.start === slot.start ? 'btn-primary' : 'btn-outline-primary'"
                                            @click="selectSlot(date, slot)">
                                            {{ slot.start }} - {{ slot.end }}
                                        </button>
                                    </div>
                                </div>
                            </div>
                            <div v-else class="text-muted text-center">No slots available</div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button"
                            class="btn btn-primary rounded-pill px-4 py-2 shadow-sm d-flex align-items-center"
                            @click="confirmBooking" :disabled="!selectedSlot">
                            <i class="bi bi-check2-circle me-2"></i>
                            Confirm Booking
                        </button>
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