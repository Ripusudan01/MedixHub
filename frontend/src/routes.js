import { createWebHistory, createRouter } from "vue-router";

import ErrorPage from "./components/ErrorPage.vue";
import LandingPage from "./components/LandingPage.vue";
import LoginPage from "./components/LoginPage.vue";
import RegisterPage from "./components/RegisterPage.vue";

import AdminLayoutPage from "./components/AdminLayoutPage.vue";
import AdminDashHome from "./components/AdminDashHome.vue";
import AdminDashDoctor from "./components/AdminDashDoctor.vue";
import AdminDashDept from "./components/AdminDashDept.vue";
import AdminDashPatient from "./components/AdminDashPatient.vue";
import AdminDashAppt from "./components/AdminDashAppt.vue";

import PatientLayoutPage from "./components/PatientLayoutPage.vue";
import PatientDashHome from "./components/PatientDashHome.vue";
import PatientDashDept from "./components/PatientDashDept.vue";
import PatientDashDoctor from "./components/PatientDashDoctor.vue";
import PatientDashAppt from "./components/PatientDashAppt.vue";

import DoctorLayoutPage from "./components/DoctorLayoutPage.vue";
import DoctorDashHome from "./components/DoctorDashHome.vue";
import DoctorDashPatient from "./components/DoctorDashPatient.vue";
import DoctorDashAppt from "./components/DoctorDashAppt.vue";

const routes = [
  { path: "/", component: LandingPage },
  { path: "/login", component: LoginPage },
  { path: "/register", component: RegisterPage },

  // Admin Routes
  {
    path: "/admin/dashboard",
    component: AdminLayoutPage,
    children: [
      { path: "", component: AdminDashHome },
      { path: "doctor", component: AdminDashDoctor },
      { path: "patient", component: AdminDashPatient },
      { path: "appointment", component: AdminDashAppt },
      { path: "department", component: AdminDashDept },
    ],
  },

  // Patient Routes
  {
    path: "/patient/:id/dashboard",
    component: PatientLayoutPage,
    children: [
      { path: "", component: PatientDashHome },
      { path: "department", component: PatientDashDept },
      { path: "doctor", component: PatientDashDoctor },
      { path: "appointment", component: PatientDashAppt },
    ],
  },

  // Doctor Routes
  {
    path: "/doctor/:id/dashboard",
    component: DoctorLayoutPage,
    children: [
      { path: "", component: DoctorDashHome },
      { path: "patient", component: DoctorDashPatient },
      { path: "appointment", component: DoctorDashAppt },
    ],
  },

  { path: "/:pathMatch(.*)*", component: ErrorPage },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});
