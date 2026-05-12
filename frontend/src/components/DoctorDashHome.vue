<script>
import axios from "axios";
import { Bar } from "vue-chartjs";
import {
    Chart as ChartJS,
    BarElement,
    CategoryScale,
    LinearScale,
    Title,
    Tooltip
} from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale, Title, Tooltip);

export default {
    components: { Bar },
    data() {
        return {
            jwt_token: "",
            doctor_data: {},
            next7Days: [],
            newDoctor: { selected_dates: [], shift_start: "", shift_end: "" },
            chartData: {
                labels: [],
                datasets: [{
                    label: "Appointments",
                    data: [],
                    backgroundColor: ["#007bff", "#28a745", "#dc3545"]
                }]
            },
            chartOptions: {
                responsive: true,
                plugins: {
                    legend: { position: "bottom" },
                    title: { display: true, text: "Appointment Overview" },
                },
            }
        }
    },
    methods: {
        async doctorDashHome() {
            try {
                const res = await axios.get("http://127.0.0.1:5000/api/doctor_dash/homePage", {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${this.jwt_token}`
                    }
                })
                this.doctor_data = res.data
            } catch (err) {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/login")
            }
        },
        generateNext7Days() {
            const today = new Date();
            this.next7Days = [];

            for (let i = 0; i < 7; i++) {
                const date = new Date(today);
                date.setDate(today.getDate() + i);

                this.next7Days.push({
                    date: date.toISOString().split("T")[0],
                    label: date.toDateString()
                });
            }
        },
        async doctorDashAvailability() {
            try {
                const res = await axios.post("http://127.0.0.1:5000/api/doctor_dash/homePage",
                    this.newDoctor,
                    {
                        headers: {
                            "Content-Type": "application/json",
                            "Authorization": `Bearer ${this.jwt_token}`
                        }
                    })
                this.doctorDashHome()
                this.newDoctor = { selected_dates: [], shift_start: "", shift_end: "" }
                const modal = bootstrap.Modal.getInstance(document.getElementById("availabilityModal"))
                modal.hide()
            } catch (err) {
                alert("Failed to save " + (err.response?.data?.msg || ""));
                this.newDoctor = { selected_dates: [], shift_start: "", shift_end: "" }
            }
        },
        async doctorDashChart() {
            try {
                const res = await axios.get("http://127.0.0.1:5000/api/doctor_dash/chart", {
                    headers: { Authorization: `Bearer ${this.jwt_token}` },
                });
                const data = res.data.appointmentStatus || [];

                this.chartData = {
                    labels: data.map(d => d.status),
                    datasets: [{
                        label: "Appointments",
                        data: data.map(d => d.count),
                        backgroundColor: ["#007bff", "#28a745", "#dc3545"]
                    }]
                };
            } catch (err) {
                console.error(err);
            }
        }
    },
    mounted() {
        const jwt = localStorage.getItem("token");
        if (jwt) {
            this.jwt_token = jwt;
            this.doctorDashHome();
            this.generateNext7Days()
            this.doctorDashChart()
        } else {
            this.$router.push("/login");
            alert("Please login to access Dashboard.");
        }
    }
}
</script>

<template>
    <div v-if="jwt_token">
        <div class="d-flex dashboard-body mt-2">
            <div class="content">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <div class="btn btn-light border">
                        <i class="bi bi-calendar-check me-2"></i> Last Update: Oct 2025 - Nov 2025
                    </div>
                    <button class="btn text-white shadow-sm report-button"
                        style="background-color: #4084f6; border-radius: 0.5rem;" data-bs-toggle="modal"
                        data-bs-target="#availabilityModal">
                        <i class="bi bi-calendar-check me-1"></i> Set Availability
                    </button>
                </div>
                <div class="row g-4">
                    <div class="col-md-4">
                        <div class="card card-custom p-3">
                            <h6 class="fw-bold"><i class="bi bi-calendar-check me-2"></i>Appointments</h6>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Today</span>
                                <span>{{ doctor_data.appointments?.today }}</span>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Upcoming</span>
                                <span>{{ doctor_data.appointments?.upcoming }}</span>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Completed</span>
                                <span>{{ doctor_data.appointments?.completed }}</span>
                            </div>
                        </div>
                    </div>

                    <div class="col-md-4">
                        <div class="card card-custom p-3">
                            <h6 class="fw-bold"><i class="bi bi-file-medical me-2"></i>Treatments</h6>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Today</span>
                                <span>{{ doctor_data.treatments?.today }}</span>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">This Week</span>
                                <span>{{ doctor_data.treatments?.week }}</span>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Total</span>
                                <span>{{ doctor_data.treatments?.total }}</span>
                            </div>
                        </div>
                    </div>

                    <div class="col-md-4">
                        <div class="card card-custom p-3">
                            <h6 class="fw-bold"><i class="bi bi-currency-rupee me-2"></i>Revenue</h6>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Today</span>
                                <span>3,200</span>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">This Week</span>
                                <span>18,750</span>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">This Month</span>
                                <span>72,500</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card card-custom-chart p-3 mt-4">
                    <h6 class="fw-bold mb-3">
                        <i class="bi bi-bar-chart-fill me-2"></i> Appointment Statistics
                    </h6>
                    <div v-if="chartData && chartData.datasets && chartData.datasets[0].data.length">
                        <Bar :data="chartData" :options="chartOptions" style="max-height: 350px;" />
                    </div>
                    <div v-else class="text-center text-muted py-5">
                        No appointment data available yet
                    </div>
                </div>

                <div class="card card-custom p-3 mt-4">
                    <h6 class="mb-3 fw-bold"><i class="bi bi-calendar me-2"></i>Recent Appointments</h6>
                    <div class="table-responsive">
                        <table class="table align-middle">
                            <thead>
                                <tr>
                                    <th class="text-muted">#</th>
                                    <th class="text-muted">Patient Name</th>
                                    <th class="text-muted">Date</th>
                                    <th class="text-muted">Time</th>
                                    <th class="text-muted">Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-if="!doctor_data.recent_patients || doctor_data.recent_patients?.length === 0">
                                    <td colspan="5" class="text-center text-muted">No recent appointments found</td>
                                </tr>
                                <tr v-else v-for="(patient, index) in doctor_data.recent_patients"
                                    :key="patient.appointment_id">
                                    <td>{{ index + 1 }}</td>
                                    <td>{{ patient.patientName }}</td>
                                    <td>{{ patient.date }}</td>
                                    <td>{{ patient.time }}</td>
                                    <td>
                                        <span class="badge rounded-pill" :class="{
                                            'bg-primary': patient.status === 'Booked',
                                            'bg-success': patient.status === 'Completed',
                                            'bg-danger': patient.status === 'Cancelled'
                                        }">
                                            {{ patient.status }}
                                        </span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        <div class="modal fade" id="availabilityModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title w-100 text-center">Set Your Availability</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="doctorDashAvailability">
                            <div class="mb-3">
                                <label class="form-label fw-semibold">Select Dates</label>
                                <div v-for="day in next7Days" :key="day.date" class="form-check">
                                    <label class="form-check-label">
                                        <input class="form-check-input me-2" type="checkbox" :value="day.date"
                                            v-model="newDoctor.selected_dates" />
                                        {{ day.label }}
                                    </label>
                                </div>
                            </div>

                            <div class="mb-3 row">
                                <div class="col">
                                    <label class="form-label fw-semibold">Start Time</label>
                                    <input type="time" v-model="newDoctor.shift_start" class="form-control" required />
                                </div>
                                <div class="col">
                                    <label class="form-label fw-semibold">End Time</label>
                                    <input type="time" v-model="newDoctor.shift_end" class="form-control" required />
                                </div>
                            </div>

                            <button type="submit" class="btn btn-primary w-100">
                                <i class="bi bi-check-circle me-1"></i> Save Availability
                            </button>
                        </form>
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
    padding: 20px;
}

.card-custom {
    border-radius: 16px;
    border: none;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.card-custom-chart {
    border-radius: 16px;
    border: none;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.report-button:hover {
    transform: scale(1.03);
    transition: 0.2s ease-in-out;
}
</style>