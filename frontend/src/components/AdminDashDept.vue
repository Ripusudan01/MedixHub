<script>
import axios from 'axios';

export default {
    data() {
        return {
            jwt_token: "",
            admin_dept_data: [],
            newDept: {
                deptName: "",
                deptDescription: ""
            },
            searchText: ""
        }
    },
    methods: {
        async adminDashDept() {
            try {
                const res = await axios.get("http://127.0.0.1:5000/api/admin_dash/deptPage", {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${this.jwt_token}`
                    }
                })
                this.admin_dept_data = res.data.department
            } catch (err) {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/login")
            }
        },
        async adminAddDept() {
            try {
                const res = await axios.post("http://127.0.0.1:5000/api/admin_dash/deptPage",
                    this.newDept,
                    {
                        headers: {
                            "Content-Type": "application/json",
                            "Authorization": `Bearer ${this.jwt_token}`
                        }
                    })
                this.adminDashDept()
                this.newDept = { deptName: "", deptDescription: "" }
                const modal = bootstrap.Modal.getInstance(document.getElementById("addDeptModal"))
                modal.hide()
            } catch (err) {
                alert("Failed to add " + (err.response?.data?.msg || ""));
                this.newDept = { deptName: "", deptDescription: "" }
            }
        }
    },
    mounted() {
        const jwt = localStorage.getItem("token");
        if (jwt) {
            this.jwt_token = jwt;
            this.adminDashDept();
        } else {
            this.$router.push("/login");
            alert("Please login to access Dashboard.");
        }
    },
    computed: {
        deptFilter() {
            if (!this.searchText) return this.admin_dept_data;
            const q = this.searchText.toLowerCase();
            return this.admin_dept_data.filter(d =>
                d.name.toLowerCase().includes(q)
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
                    <button class="btn btn-outline-primary shadow-sm" data-bs-toggle="modal" data-bs-target="#addDeptModal">
                        <i class="bi bi-building-add me-1"></i>Department
                    </button>
                    <button class="btn btn-outline-secondary shadow-sm">
                        <i class="bi bi-upload me-1"></i> Export to CSV
                    </button>
                </div>

                <div class="card card-custom p-3">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h6 class="fw-bold">
                            <i class="bi bi-diagram-3 me-2"></i>Department List
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
                                    <th class="text-muted">Total Doctors</th>
                                    <th class="text-muted">Description</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-if="!deptFilter || deptFilter.length === 0">
                                    <td colspan="3" class="text-center text-muted">No department found</td>
                                </tr>
                                <tr v-for="dept in deptFilter" :key="dept.id">
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
        <!-- Add Department -->
        <div class="modal fade" id="addDeptModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title w-100 text-center">Add Department</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <div class="modal-body">
                        <form @submit.prevent="adminAddDept">
                            <div class="mb-3">
                                <label class="form-label">Name</label>
                                <input type="text" v-model="newDept.deptName" class="form-control" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Description</label>
                                <textarea type="text" v-model="newDept.deptDescription" class="form-control"
                                    required></textarea>
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