import React, { useState, useEffect } from "react";
import "../styles/Franchise.css";
// Importing assets from the project
import heroBg from "../images/franchise1.mp4";
import aiImage from "../images/Technology.jpg"; // Using existing tech image
import {
    FaStore, FaChartLine, FaHandsHelping, FaLaptopCode, FaCheckCircle,
    FaLeaf, FaCoins, FaUserTie, FaNetworkWired, FaFileContract,
    FaSeedling, FaFlask, FaWater, FaTractor, FaWarehouse, FaCreditCard,
    FaTruck, FaBullhorn, FaChalkboardTeacher, FaBoxOpen, FaRupeeSign
} from "react-icons/fa";
import { useLang } from "../components/LangContext";

const Franchise = () => {
    const { t } = useLang();
    // Scroll to top on mount (fixes navigation issue)
    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    const [formData, setFormData] = useState({
        name: "",
        email: "",
        phone: "",
        city: "",
        investment: "",
        message: ""
    });
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        const payload = {
            name: formData.name,
            email: formData.email,
            phone: formData.phone,
            city: formData.city,
            investment: formData.investment,
            message: formData.message
        };

        try {
            const response = await fetch("https://admin.agrifabrix.in/api/static/Franchise", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });

            const data = await response.json();

            if (response.ok) {
                alert(t("franchise_alert_success"));
                setFormData({ name: "", email: "", phone: "", city: "", investment: "", message: "" });
            } else {
                alert(data.error || t("franchise_alert_failed"));
            }
        } catch (error) {
            console.error("Error submitting form:", error);
            alert(t("franchise_alert_error") || "Network error. Please try again later.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="franchise-page">
            {/* HERO SECTION */}
            {/* HERO SECTION */}
            <section className="franchise-hero">
                <video
                    className="hero-bg-video"
                    src={heroBg}
                    autoPlay
                    loop
                    muted
                    playsInline
                />
                <div className="hero-overlay"></div>
                <div className="hero-content">
                    <h1>{t("franchise_hero_title")}</h1>
                    <p style={{ fontWeight: 'bold' }}>{t("franchise_hero_desc")}</p>
                    <a href="#leads-form" className="hero-cta-button">{t("franchise_hero_cta")}</a>
                </div>
            </section>

            {/* 1. IDEAL FRANCHISE PARTNER */}
            <section className="franchise-section light-bg">
                <div className="section-container">
                    <h2>{t("franchise_partner_title")}</h2>
                    <p className="section-subtitle">{t("franchise_partner_subtitle")}</p>
                    <div className="grid-4">
                        <div className="feature-card">
                            <FaUserTie className="card-icon" />
                            <h3>{t("franchise_partner_prof_title")}</h3>
                            <p>{t("franchise_partner_prof_desc")}</p>
                        </div>
                        <div className="feature-card">
                            <FaNetworkWired className="card-icon" />
                            <h3>{t("franchise_partner_net_title")}</h3>
                            <p>{t("franchise_partner_net_desc")}</p>
                        </div>
                        <div className="feature-card">
                            <FaStore className="card-icon" />
                            <h3>{t("franchise_partner_retail_title")}</h3>
                            <p>{t("franchise_partner_retail_desc")}</p>
                        </div>
                        <div className="feature-card">
                            <FaFileContract className="card-icon" />
                            <h3>{t("franchise_partner_comp_title")}</h3>
                            <p>{t("franchise_partner_comp_desc")}</p>
                        </div>
                    </div>
                </div>
            </section>

            <section className="franchise-section">
                <div className="section-container">
                    <h2>{t("franchise_scope_title")}</h2>
                    <p className="section-subtitle">{t("franchise_scope_subtitle")}</p>
                    <div className="grid-3">
                        <div className="service-card">
                            <FaLeaf className="service-icon" />
                            <h4>{t("franchise_scope_input_title")}</h4>
                            <p>{t("franchise_scope_input_desc")}</p>
                        </div>
                        <div className="service-card">
                            <FaFlask className="service-icon" />
                            <h4>{t("franchise_scope_advisory_title")}</h4>
                            <p>{t("franchise_scope_advisory_desc")}</p>
                        </div>
                        <div className="service-card">
                            <FaWater className="service-icon" />
                            <h4>{t("franchise_scope_irrigation_title")}</h4>
                            <p>{t("franchise_scope_irrigation_desc")}</p>
                        </div>
                        <div className="service-card">
                            <FaTractor className="service-icon" />
                            <h4>{t("franchise_scope_machinery_title")}</h4>
                            <p>{t("franchise_scope_machinery_desc")}</p>
                        </div>
                        <div className="service-card">
                            <FaWarehouse className="service-icon" />
                            <h4>{t("franchise_scope_harvest_title")}</h4>
                            <p>{t("franchise_scope_harvest_desc")}</p>
                        </div>
                        <div className="service-card">
                            <FaCreditCard className="service-icon" />
                            <h4>{t("franchise_scope_finance_title")}</h4>
                            <p>{t("franchise_scope_finance_desc")}</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* 3. PERKS & BENEFITS */}
            <section className="franchise-section light-bg">
                <div className="section-container">
                    <h2>{t("franchise_perks_title")}</h2>
                    <p className="section-subtitle">{t("franchise_perks_subtitle")}</p>
                    <div className="grid-4">
                        <div className="benefit-card-new">
                            <FaCheckCircle className="benefit-icon-new" />
                            <h3>{t("franchise_perks_brand_title")}</h3>
                            <p>{t("franchise_perks_brand_desc")}</p>
                        </div>
                        <div className="benefit-card-new">
                            <FaBoxOpen className="benefit-icon-new" />
                            <h3>{t("franchise_perks_supply_title")}</h3>
                            <p>{t("franchise_perks_supply_desc")}</p>
                        </div>
                        <div className="benefit-card-new">
                            <FaChalkboardTeacher className="benefit-icon-new" />
                            <h3>{t("franchise_perks_training_title")}</h3>
                            <p>{t("franchise_perks_training_desc")}</p>
                        </div>
                        <div className="benefit-card-new">
                            <FaBullhorn className="benefit-icon-new" />
                            <h3>{t("franchise_perks_marketing_title")}</h3>
                            <p>{t("franchise_perks_marketing_desc")}</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* TECHNOLOGY SECTION (Preserved) */}
            <section className="franchise-ai-tech">
                <div className="ai-image">
                    <img src={require("../images/banana_high_tech_farm.png")} alt="Modern Banana Farming" />
                </div>
                <div className="ai-content">
                    <h2>{t("franchise_tech_title")}</h2>
                    <p>{t("franchise_tech_desc")}</p>
                    <ul>
                        <li><FaLeaf color="#28a745" /> <span>{t("franchise_tech_li1")}</span></li>
                        <li><FaCoins color="#28a745" /> <span>{t("franchise_tech_li2")}</span></li>
                        <li><FaChartLine color="#28a745" /> <span>{t("franchise_tech_li3")}</span></li>
                        <li><FaCheckCircle color="#28a745" /> <span>{t("franchise_tech_li4")}</span></li>
                    </ul>
                </div>
            </section>


            {/* 5. APPLICATION PROCESS */}
            <section className="franchise-section">
                <div className="section-container">
                    <h2>{t("franchise_process_title")}</h2>
                    <div className="process-steps">
                        <div className="process-step">
                            <div className="step-num">1</div>
                            <h4>{t("franchise_process_step1_title")}</h4>
                            <p>{t("franchise_process_step1_desc")}</p>
                        </div>
                        <div className="process-connector"></div>
                        <div className="process-step">
                            <div className="step-num">2</div>
                            <h4>{t("franchise_process_step2_title")}</h4>
                            <p>{t("franchise_process_step2_desc")}</p>
                        </div>
                        <div className="process-connector"></div>
                        <div className="process-step">
                            <div className="step-num">3</div>
                            <h4>{t("franchise_process_step3_title")}</h4>
                            <p>{t("franchise_process_step3_desc")}</p>
                        </div>
                        <div className="process-connector"></div>
                        <div className="process-step">
                            <div className="step-num">4</div>
                            <h4>{t("franchise_process_step4_title")}</h4>
                            <p>{t("franchise_process_step4_desc")}</p>
                        </div>
                        <div className="process-connector"></div>
                        <div className="process-step">
                            <div className="step-num highlight">5</div>
                            <h4>{t("franchise_process_step5_title")}</h4>
                            <p>{t("franchise_process_step5_desc")}</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* FAQ */}
            <section className="franchise-faq">
                <h2>{t("franchise_faq_title")}</h2>
                <div className="faq-item">
                    <h3>{t("franchise_faq_q1")}</h3>
                    <p>{t("franchise_faq_a1")}</p>
                </div>
                <div className="faq-item">
                    <h3>{t("franchise_faq_q2")}</h3>
                    <p>{t("franchise_faq_a2")}</p>
                </div>
                <div className="faq-item">
                    <h3>{t("franchise_faq_q3")}</h3>
                    <p>{t("franchise_faq_a3")}</p>
                </div>
            </section>

            {/* APPLICATION FORM */}
            <section id="leads-form" className="franchise-application">
                <h2>{t("franchise_form_title")}</h2>
                <p>{t("franchise_form_subtitle")}</p>

                <form className="application-form" onSubmit={handleSubmit}>

                    <div className="form-group">
                        <label>{t("franchise_form_name")}</label>
                        <input
                            type="text"
                            name="name"
                            value={formData.name}
                            onChange={handleChange}
                            required
                            placeholder={t("franchise_form_name_placeholder")}
                        />
                    </div>

                    <div className="form-group">
                        <label>{t("franchise_form_email")}</label>
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            required
                            placeholder={t("franchise_form_email_placeholder")}
                        />
                    </div>

                    <div className="form-group">
                        <label>{t("franchise_form_phone")}</label>
                        <input
                            type="tel"
                            name="phone"
                            value={formData.phone}
                            onChange={handleChange}
                            required
                            placeholder={t("franchise_form_phone_placeholder")}
                        />
                    </div>

                    <div className="form-group">
                        <label>{t("franchise_form_location")}</label>
                        <input
                            type="text"
                            name="city"
                            value={formData.city}
                            onChange={handleChange}
                            required
                            placeholder={t("franchise_form_location_placeholder")}
                        />
                    </div>

                    <div className="form-group">
                        <label>{t("franchise_form_investment")}</label>
                        <select name="investment" value={formData.investment} onChange={handleChange} required>
                            <option value="">{t("franchise_form_investment_placeholder")}</option>
                            <option value="5-10 Lakhs">₹5 - ₹10 Lakhs</option>
                            <option value="10-15 Lakhs">₹10 - ₹15 Lakhs</option>
                            <option value="15-25 Lakhs">₹15 - ₹25 Lakhs</option>
                            <option value="25+ Lakhs">₹25 Lakhs+</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label>{t("franchise_form_message")}</label>
                        <textarea
                            name="message"
                            value={formData.message}
                            onChange={handleChange}
                            placeholder={t("franchise_form_message_placeholder")}
                            rows="4"
                        ></textarea>
                    </div>

                    <button type="submit" className="submit-button" disabled={loading}>
                        {loading ? t("franchise_form_submitting") : t("franchise_form_submit")}
                    </button>

                </form>
            </section>
        </div>
    );
};

export default Franchise;
