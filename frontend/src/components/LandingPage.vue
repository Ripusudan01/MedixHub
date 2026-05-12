<script>
import doctorImg from '../assets/doctor2.jpeg'

export default {
    data() {
        return {
            doctorImg
        }
    },
    methods: {
        scrollToSection(id) {
            const el = document.getElementById(id)
            if (el) {
                el.scrollIntoView({ behavior: 'smooth' })
                history.replaceState(null, '', window.location.pathname)
            }
        }
    }
}
</script>

<template>
    <!-- Navbar -->
    <div id="home">
        <nav class="navbar navbar-expand-lg shadow-sm">
            <div class="container">
                <a class="navbar-brand" href="" @click.prevent="scrollToSection('home')">MedixHub<sup>+</sup></a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse justify-content-center" id="navbarNav">
                    <ul class="navbar-nav mb-2 mb-lg-0">
                        <li class="nav-item"><a class="nav-link" href=""
                                @click.prevent="scrollToSection('home')">Home</a></li>
                        <li class="nav-item"><a class="nav-link" href="" @click.prevent="scrollToSection('foot')">About
                                Us</a></li>
                        <li class="nav-item"><a class="nav-link" href=""
                                @click.prevent="scrollToSection('services')">Services</a></li>
                        <li class="nav-item"><a class="nav-link" href=""
                                @click.prevent="scrollToSection('foot')">Contact Us</a></li>
                    </ul>
                </div>
                <router-link to="/login" class="btn btn-gradient ms-lg-3">
                    Login / Sign up
                </router-link>
            </div>
        </nav>

        <!-- Main -->
        <section class="main py-4 mb-5">
            <div class="container">
                <div class="row align-items-center">
                    <div class="col-lg-6 order-1 order-lg-1 text-center text-lg-start">
                        <h1 class="fw-bold mb-3">24/7 Healthcare made simple, reliable, and caring for you</h1>
                        <p class="text-muted mb-4">
                            Your health, our priority — expert doctors, timely care, and complete support under one
                            roof
                        </p>

                        <div class="d-none d-lg-block">
                            <router-link to="/login" class="btn btn-gradient">
                                Book Appointment <i class="bi bi-arrow-right ms-2"></i>
                            </router-link>
                        </div>
                    </div>

                    <div class="col-lg-6 text-center order-2 order-lg-2">
                        <div class="doctor-circle">
                            <img :src="doctorImg" alt="Doctor" class="doctor-circle-img" />
                        </div>
                    </div>

                    <div class="col-12 text-center order-3 d-lg-none mt-3">
                        <router-link to="/login" class="btn btn-gradient">
                            Book Appointment <i class="bi bi-arrow-right ms-2"></i>
                        </router-link>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <!-- Partners Section -->
    <section class="partners-section py-5">
        <div class="container">
            <h3 class="text-center mb-4 section-title">Our Partners</h3>
            <div class="d-flex justify-content-center align-items-center gap-5 flex-wrap py-3">
                <div class="text-center">
                    <i class="bi bi-lightning-charge-fill partner-icon" aria-hidden="true"></i>
                    <div class="partner-name">Lightbox</div>
                </div>
                <div class="text-center">
                    <i class="bi bi-cpu-fill partner-icon" aria-hidden="true"></i>
                    <div class="partner-name">CoreOS</div>
                </div>
                <div class="text-center">
                    <i class="bi bi-building partner-icon" aria-hidden="true"></i>
                    <div class="partner-name">Acme Corp</div>
                </div>
                <div class="text-center">
                    <i class="bi bi-shield-lock-fill partner-icon" aria-hidden="true"></i>
                    <div class="partner-name">Watchtower</div>
                </div>
                <div class="text-center">
                    <i class="bi bi-diagram-3-fill partner-icon" aria-hidden="true"></i>
                    <div class="partner-name">PictelAI</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Services Section -->
    <section id="services" class="services-section py-5">
        <div class="container">
            <h3 class="text-center mb-4 section-title">Our Services</h3>
            <div class="row justify-content-center g-4">
                <div class="col-md-4">
                    <div class="card p-4 text-center services-card">
                        <i class="bi bi-heart-pulse service-icon mb-3"></i>
                        <h5 class="fw-semibold">Medical Check-Ups</h5>
                        <p class="text-muted mb-3 text-start">Comprehensive health check-ups for timely diagnosis,
                            preventive care, and maintaining your family’s overall well-being.</p>
                        <a href="https://wa.me/919507444356" target="_blank" class="btn btn-gradient mt-auto"><i
                                class="bi bi-whatsapp me-2"></i>Booking</a>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card p-4 text-center services-card">
                        <i class="bi bi-person-badge service-icon mb-3"></i>
                        <h5 class="fw-semibold">Expert Doctors</h5>
                        <p class="text-muted mb-3 text-start">Consult leading specialists across fields for personalized
                            care, expert guidance, and reliable health solutions anytime.</p>
                        <a href="https://wa.me/919507444356" target="_blank" class="btn btn-gradient mt-auto"><i
                                class="bi bi-whatsapp me-2"></i>Booking</a>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card p-4 text-center services-card">
                        <i class="bi bi-bag-plus service-icon mb-3"></i>
                        <h5 class="fw-semibold">24/7 Pharmacy</h5>
                        <p class="text-muted mb-3 text-start">Order medicines anytime with doorstep delivery. Pharmacy
                            partners ensure genuine medicines and quick service.</p>
                        <a href="https://wa.me/919507444356" target="_blank" class="btn btn-gradient mt-auto"><i
                                class="bi bi-whatsapp me-2"></i>Booking</a>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Testimonials Section -->
    <section class="testimonials-section py-5">
        <div class="container">
            <h3 class="text-center fw-semibold mb-4 section-title">What our patients say</h3>
            <div class="row justify-content-center g-4 align-items-stretch">
                <div class="col-md-6 col-lg-5">
                    <div class="testimonial-card">
                        <p class="testimonial-text">
                            MedixHub transformed my healthcare experience; booking is easy,
                            and doctors are professional, caring, and reliable.
                        </p>

                        <div class="testimonial-footer">
                            <img src="https://randomuser.me/api/portraits/men/32.jpg" alt="Ajay Sharma"
                                class="testimonial-avatar" />
                            <div>
                                <div class="testimonial-name">Ajay Sharma</div>
                                <div class="testimonial-role">Patient</div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-md-6 col-lg-5">
                    <div class="testimonial-card">
                        <p class="testimonial-text">
                            The staff was kind and supportive, and the facilities were
                            modern and well-maintained. I felt truly cared for.
                        </p>

                        <div class="testimonial-footer">
                            <img src="https://randomuser.me/api/portraits/men/36.jpg" alt="Rahul Verma"
                                class="testimonial-avatar" />
                            <div>
                                <div class="testimonial-name">Rahul Verma</div>
                                <div class="testimonial-role">Patient</div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-md-6 col-lg-5">
                    <div class="testimonial-card">
                        <p class="testimonial-text">
                            I used MedixHub for regular check-ups and was impressed with
                            efficiency. No long waits, everything was smooth.
                        </p>

                        <div class="testimonial-footer">
                            <img src="https://randomuser.me/api/portraits/men/39.jpg" alt="Md Ashik Rahman"
                                class="testimonial-avatar" />
                            <div>
                                <div class="testimonial-name">Md Ashik Rahman</div>
                                <div class="testimonial-role">Patient</div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-md-6 col-lg-5">
                    <div class="testimonial-card">
                        <p class="testimonial-text">
                            From consultation to pharmacy, everything was available under
                            one roof. MedixHub makes healthcare accessible.
                        </p>

                        <div class="testimonial-footer">
                            <img src="https://randomuser.me/api/portraits/women/40.jpg" alt="Radhika Singh"
                                class="testimonial-avatar" />
                            <div>
                                <div class="testimonial-name">Radhika Singh</div>
                                <div class="testimonial-role">Patient</div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer id="foot" class="custom-footer">
        <div class="container py-5">
            <div class="row">
                <div class="col-md-4 mb-4 mb-md-0">
                    <h4 class="footer-logo mb-3">MedixHub<sup>+</sup></h4>
                    <p class="footer-address mb-3 text-white-50">MedixHub makes healthcare simple, accessible, and
                        reliable with expert
                        doctors, trusted pharmacies, and 24/7 support.</p>
                    <div class="footer-socials d-flex gap-3">
                        <a href="#" class="footer-icon"><i class="bi bi-youtube"></i></a>
                        <a href="#" class="footer-icon"><i class="bi bi-instagram"></i></a>
                        <a href="https://wa.me/919507444356" target="_blank" class="footer-icon"><i
                                class="bi bi-whatsapp"></i></a>
                    </div>
                </div>
                <div class="col-md-2 mb-4 mb-md-0">
                    <h6 class="footer-title">Quick Links</h6>
                    <ul class="footer-links">
                        <li><a href="#">Career</a></li>
                        <li><a href="#">Blog</a></li>
                        <li><a href="" @click.prevent="scrollToSection('services')">Services</a></li>
                    </ul>
                </div>

                <div class="col-md-3 mb-4 mb-md-0">
                    <h6 class="footer-title">Branch</h6>
                    <ul class="footer-links">
                        <li>Delhi</li>
                        <li>Chennai</li>
                        <li>Kolkata</li>
                        <li>Mumbai</li>
                    </ul>
                </div>
                <div class="col-md-3">
                    <h6 class="footer-title">Contact Us</h6>
                    <ul class="footer-links">
                        <li><i class="bi bi-envelope me-2"></i><a href="mailto:info@medixhub.com">info@medixhub.com</a>
                        </li>
                        <li><i class="bi bi-telephone me-2"></i><a href="tel:+01723456789">+01723456789</a></li>
                        <li>
                            <p><i class="bi bi-geo-alt-fill me-2"></i>Mumbai - 400051, India</p>
                        </li>
                    </ul>
                </div>

            </div>
            <hr class="footer-divider my-4" />
            <div class="text-center text-white-50 small">
                Copyright &copy; <span style="color: #4084F6;">MedixHub</span> 2025. All Rights Reserved.
            </div>
        </div>
    </footer>
    <a href="https://wa.me/919507444356" class="whatsapp-float-icon" target="_blank">
        <i class="bi bi-whatsapp"></i>
    </a>
</template>

<style scoped>
.doctor-circle {
    width: 450px;
    height: 450px;
    border-radius: 50%;
    overflow: hidden;
    margin: 0 auto;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
    background-color: #fff;
}

.doctor-circle-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.navbar-brand {
    font-weight: bolder;
    font-size: 1.5rem;
    letter-spacing: 0.5px;
    color: #4084F6 !important;
}

.nav-link {
    color: #0A0E31;
    font-weight: 500;
    margin: 0 10px;
}

.nav-link:hover {
    color: #4084F6;
}

.btn-gradient {
    background: linear-gradient(to left, #4084F6, #5268F8);
    border: none;
    color: #fff;
    padding: 10px 27px;
    border-radius: 50px;
    font-weight: 500;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: 0.3s;
}

.btn-gradient:hover {
    opacity: 0.9;
    transform: scale(1.05);
}

.main h1 {
    font-size: 2.1rem;
    line-height: 1.3;
    color: #4084F6;
}

.partners-section {
    background: #E3EDFF;
}

.partner-icon {
    font-size: 30px;
    color: #fff;
    background: linear-gradient(90deg, #4084F6, #5268F8);
    padding: 12px;
    border-radius: 12px;
    display: inline-block;
}

.partner-name {
    color: #4084F6;
    font-weight: 600;
    font-size: 1.1rem;
    margin-top: 2px;
    letter-spacing: 0.5px;
}

.services-card {
    border-radius: 20px;
    box-shadow: 0 4px 12px rgba(64, 132, 246, 0.07);
    background: #fff;
    height: 100%;
    transition: transform 0.3s ease;
    display: flex;
    flex-direction: column;
}

.services-card:hover {
    transform: translateY(-5px);
}

.service-icon {
    font-size: 48px;
    color: #4084F6;
}

.testimonial-card {
    background: #fff;
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 8px 30px rgba(64, 132, 246, 0.08);
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.testimonial-text {
    font-size: 1rem;
    line-height: 1.6;
    color: #0A0E31;
    margin-bottom: 20px;
}

.testimonial-footer {
    display: flex;
    align-items: center;
    gap: 14px;
}

.testimonial-avatar {
    width: 55px;
    height: 55px;
    border-radius: 50%;
    object-fit: cover;
    flex-shrink: 0;
}

.testimonial-name {
    font-weight: 600;
    color: #4084F6;
    font-size: 1rem;
}

.testimonial-role {
    font-size: 0.85rem;
    color: #6b7a99;
}

.section-title {
    color: #0A0E31;
    font-weight: 600;
}

.custom-footer {
    background: #0A0E31;
    color: #fff;
}

.footer-logo {
    font-weight: bold;
    font-size: 1.6rem;
    color: #4084F6;
}

.footer-address {
    font-size: 1rem;
    color: #bac9e6;
    line-height: 1.7;
}

.footer-title {
    color: #fff;
    font-weight: 600;
    margin-bottom: 1rem;
    font-size: 1.05rem;
}

.footer-links {
    list-style: none;
    padding: 0;
    margin: 0;
    color: #bac9e6;
    font-size: 1rem;
}

.footer-links li {
    margin-bottom: 0.5rem;
}

.footer-links a {
    text-decoration: none;
    color: #bac9e6;
    transition: color 0.2s;
}

.footer-links a:hover {
    color: #4084F6;
}

.footer-socials .footer-icon {
    color: #bac9e6;
    font-size: 1.6rem;
    transition: color 0.2s;
}

.footer-socials .footer-icon:hover {
    color: #4084F6;
}

.footer-divider {
    border-color: #24395c;
    margin-top: 1.5rem;
}

.whatsapp-float-icon {
    position: fixed;
    width: 60px;
    height: 60px;
    bottom: 40px;
    right: 40px;
    background-color: #25d366;
    color: #fff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
    box-shadow: 2px 2px 3px #999;
    animation: waves 2s infinite;
}

@keyframes waves {
    0% {
        box-shadow: 0 0 0 0 rgba(37, 211, 102, 0.7);
    }

    70% {
        box-shadow: 0 0 0 15px rgba(37, 211, 102, 0);
    }

    100% {
        box-shadow: 0 0 0 0 rgba(37, 211, 102, 0);
    }
}


/* Large Tablets & Small Laptops (≤1200px) */
@media (max-width: 1200px) {

    .main h1 {
        font-size: 2rem;
    }

    .doctor-circle {
        width: 380px;
        height: 380px;
    }
}

/* Tablets (≤992px) */
@media (max-width: 992px) {

    .navbar-brand {
        font-size: 1.4rem;
    }

    .main {
        text-align: center;
        padding: 40px 0;
    }

    .main h1 {
        font-size: 1.8rem;
        line-height: 1.3;
    }

    .main p {
        font-size: 1rem;
    }

    .doctor-circle {
        width: 320px;
        height: 320px;
        margin-top: 20px;
    }

    .services-card {
        height: auto;
    }
}

/* Mobile Devices (≤768px) */
@media (max-width: 768px) {

    nav .container {
        padding: 0 12px;
    }

    .navbar-brand {
        font-size: 1.25rem;
    }

    .nav-link {
        margin: 6px 0;
        text-align: center;
    }

    .doctor-circle {
        width: 360px;
        height: 360px;
        margin: 0 auto 10px auto;
    }

    .main {
        padding-top: 15px;
        padding-bottom: 15px;
    }

    .main h1 {
        font-size: 1.55rem;
        margin-bottom: 12px;
    }

    .main p {
        font-size: 0.95rem;
    }

    .services-card {
        padding: 20px;
    }

    .service-icon {
        font-size: 38px;
    }

    .testimonial-card {
        flex-direction: column;
        padding: 20px;
    }

    .testimonial-avatar {
        width: 64px;
        height: 64px;
    }

    .footer-title {
        margin-top: 20px;
    }
}

/* Small Phones (≤576px) */
@media (max-width: 576px) {

    .main {
        padding-top: 10px;
        padding-bottom: 10px;
        text-align: center;
    }

    .doctor-circle {
        width: 320px;
        height: 320px;
        margin: 0 auto 10px auto;
    }

    .main h1 {
        font-size: 1.35rem;
        line-height: 1.25;
    }

    .main p {
        font-size: 0.9rem;
        margin-bottom: 14px;
    }

    .btn-gradient {
        padding: 8px 16px;
        font-size: 0.85rem;
    }

    .partner-icon {
        font-size: 22px;
        padding: 8px;
    }

    .services-card p {
        font-size: 0.9rem;
    }

    .testimonial-text {
        font-size: 0.9rem;
    }

    .whatsapp-float-icon {
        width: 50px;
        height: 50px;
        font-size: 26px;
        bottom: 25px;
        right: 25px;
    }
}

/* Extra Small Phones (≤400px) */
@media (max-width: 400px) {
    .doctor-circle {
        width: 280px;
        height: 280px;
    }

    .main h1 {
        font-size: 1.25rem;
    }

    .navbar-brand {
        font-size: 1.15rem;
    }

    .services-card {
        padding: 15px;
    }

    .testimonial-avatar {
        width: 55px;
        height: 55px;
    }
}
</style>