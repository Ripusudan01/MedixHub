<script>
import axios from 'axios';

export default {
    data() {
        return {
            jwt_token: "",
            admin_doctor_data: [],
            admin_doctor_data_depart: [],
            newDoctor: { fullname: "", username: "", password: "", specialization: "", department_id: ""},
            searchText: "",
            selectedDoctor: { id: "", fullname: "", password: "", username: "", specialization: "", department_id: "" },
        }
    },
    methods: {
        async adminDashDoctor() {
            try {
                const res = await axios.get("http://127.0.0.1:5000/api/admin_dash/doctorPage", {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${this.jwt_token}`
                    }
                })
                this.admin_doctor_data = res.data.doctors
                this.admin_doctor_data_depart = res.data.departments
            } catch (err) {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/login")
            }
        },
        async adminAddDoctor() {
            try {
                const res = await axios.post("http://127.0.0.1:5000/api/admin_dash/doctorPage",
                    this.newDoctor,
                    {
                        headers: {
                            "Content-Type": "application/json",
                            "Authorization": `Bearer ${this.jwt_token}`
                        }
                    })
                this.adminDashDoctor()
                this.newDoctor = { fullname: "", username: "", password: "", specialization: "", department_id: "" }
                const modal = bootstrap.Modal.getInstance(document.getElementById("addDoctorModal"))
                modal.hide()
            } catch (err) {
                alert("Failed to add " + (err.response?.data?.msg || ""));
                this.newDoctor = { fullname: "", username: "", password: "", specialization: "", department_id: "" }
            }
        },
        openEditDoctor(doctor) {
            this.selectedDoctor = { ...doctor }
            const modal = new bootstrap.Modal(document.getElementById("editDoctorModal"));
            modal.show();
        },
        async adminUpdateDoctor() {
            try {
                const res = await axios.put(`http://127.0.0.1:5000/api/admin_dash/doctorPage/${this.selectedDoctor.id}`,
                    this.selectedDoctor,
                    {
                        headers: {
                            "Content-Type": "application/json",
                            "Authorization": `Bearer ${this.jwt_token}`
                        }
                    })
                this.adminDashDoctor()
                const modal = bootstrap.Modal.getInstance(document.getElementById("editDoctorModal"));
                modal.hide();
            } catch (err) {
                alert("Failed to update " + (err.response?.data?.msg || ""));
            }
        },
        async adminUpdateStatus(doctor) {
            if (!confirm(`Are you sure you want to ${doctor.status ? 'block' : 'unblock'} ${doctor.fullname}`)) {
                return;
            }
            try {
                await axios.patch(`http://127.0.0.1:5000/api/admin_dash/doctorPage/${doctor.id}/status`, {}, {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${this.jwt_token}`
                    }
                })
                this.adminDashDoctor()
            } catch (err) {
                alert("Failed to update status " + (err.response?.data?.msg || ""))
            }
        },
        async adminDeleteDoctor(doctor) {
            if (!confirm(`Are you sure you want to delete doctor ${doctor.fullname}`)) {
                return;
            }
            try {
                await axios.delete(`http://127.0.0.1:5000/api/admin_dash/doctorPage/${doctor.id}/delete`, {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${this.jwt_token}`
                    }
                })
                this.adminDashDoctor()
            } catch (err) {
                alert("Failed to delete doctor " + (err.response?.data?.msg || ""))
            }
        }
    },
    mounted() {
        const jwt = localStorage.getItem("token");
        if (jwt) {
            this.jwt_token = jwt;
            this.adminDashDoctor()
        } else {
            this.$router.push("/login");
            alert("Please login to access Dashboard.");
        }
    },
    computed: {
        doctorFilter() {
            if (!this.searchText) {
                return this.admin_doctor_data;
            }
            const q = this.searchText.toLowerCase();
            return this.admin_doctor_data.filter(d =>
                d.fullname.toLowerCase().includes(q) ||
                (d.specialization && d.specialization.toLowerCase().includes(q))
            );
        }
    }
}
</script>

<template>
    <div v-if="jwt_token">
        <div class="d-flex dashboard-body">
            <div class="content px-4 py-3">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <button class="btn btn-outline-primary shadow-sm" data-bs-toggle="modal" data-bs-target="#addDoctorModal">
                        <i class="bi bi-person-plus-fill me-1"></i>Doctor
                    </button>
                    <button class="btn btn-outline-secondary shadow-sm">
                        <i class="bi bi-upload me-1"></i> Export to CSV
                    </button>
                </div>

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
                                    <th class="text-muted">Email</th>
                                    <th class="text-muted">Joined Date</th>
                                    <th class="text-muted">Status</th>
                                    <th class="text-muted">Department</th>
                                    <th class="text-muted">Specialization</th>
                                    <th class="text-muted">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-if="!doctorFilter || doctorFilter.length === 0">
                                    <td colspan="7" class="text-center text-muted">No doctor found</td>
                                </tr>
                                <tr v-for="doctor in doctorFilter" :key="doctor.id">
                                    <td>{{ doctor.fullname }}</td>
                                    <td>{{ doctor.username }}</td>
                                    <td>{{ doctor.joined_on }}</td>
                                    <td>
                                        <span class="badge rounded-pill" :class="doctor.status ? 'bg-success' : 'bg-danger'">
                                            {{ doctor.status ? 'Active' : 'Blocked' }}
                                        </span>
                                    </td>
                                    <td>{{ doctor.department_name }}</td>
                                    <td>{{ doctor.specialization }}</td>
                                    <td>
                                        <i class="bi bi-pencil-square me-2 fs-5" style="cursor:pointer"
                                            @click="openEditDoctor(doctor)"></i>
                                        <i class="bi"
                                            :class="doctor.status ? 'bi-slash-circle text-danger me-2 fs-5' : 'bi-check-circle text-success me-2 fs-5'"
                                            style="cursor:pointer" @click="adminUpdateStatus(doctor)"></i>
                                        <i class="bi bi-trash3-fill text-danger fs-5" style="cursor:pointer" @click="adminDeleteDoctor(doctor)"></i>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        <!-- Add Doctor Modal -->
        <div class="modal fade" id="addDoctorModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title w-100 text-center">Add Doctor</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <div class="modal-body">
                        <form @submit.prevent="adminAddDoctor">
                            <div class="mb-3">
                                <label class="form-label">Fullname</label>
                                <input type="text" v-model="newDoctor.fullname" class="form-control" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Username</label>
                                <input type="email" v-model="newDoctor.username" class="form-control" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Password</label>
                                <input type="password" v-model="newDoctor.password" class="form-control" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Specialization</label>
                                <input type="text" v-model="newDoctor.specialization" class="form-control" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Department</label>
                                <select v-model="newDoctor.department_id" class="form-select" required>
                                    <option value="" disabled>Choose</option>
                                    <option v-for="dept in admin_doctor_data_depart" :key="dept.id" :value="dept.id">
                                        {{ dept.name }}
                                    </option>
                                </select>
                            </div>
                            <button type="submit" class="btn btn-primary w-100">
                                <i class="bi bi-check-circle me-1"></i> Save
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        <!-- Update Doctor Modal -->
        <div class="modal fade" id="editDoctorModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title w-100 text-center">Update Doctor</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <div class="modal-body">
                        <form @submit.prevent="adminUpdateDoctor">
                            <div class="mb-3">
                                <label class="form-label">Fullname</label>
                                <input type="text" v-model="selectedDoctor.fullname" class="form-control" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Username</label>
                                <input type="email" v-model="selectedDoctor.username" class="form-control" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Password</label>
                                <input type="password" v-model="selectedDoctor.password" class="form-control"
                                    placeholder="Leave blank to keep current password">
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Specialization</label>
                                <input type="text" v-model="selectedDoctor.specialization" class="form-control"
                                    required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Department</label>
                                <select v-model="selectedDoctor.department_id" class="form-select" required>
                                    <option value="" disabled>Choose</option>
                                    <option v-for="dept in admin_doctor_data_depart" :key="dept.id" :value="dept.id">
                                        {{ dept.name }}
                                    </option>
                                </select>
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