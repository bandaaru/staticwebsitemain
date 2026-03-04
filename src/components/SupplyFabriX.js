import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/SupplyFabriX.css';
import supplyImage from '../images/SupplyFabriX.jpg';
import ricebagsVideo from "../images/ricebags.mp4";

import { useLang } from "../components/LangContext";
import WhatsAppChatWidget from "./WhatsAppChatWidget";
import Climate from "./Climate";

const SupplyFabriX = () => {
    const { t } = useLang();

    const offerings = [
        { title: t("supply_offering_1_title"), body: t("supply_offering_1_body") },
        { title: t("supply_offering_2_title"), body: t("supply_offering_2_body") },
        { title: t("supply_offering_3_title"), body: t("supply_offering_3_body") },
        { title: t("supply_offering_4_title"), body: t("supply_offering_4_body") },
    ];

    const benefits = [
        { title: t("supply_benefit_1_title"), body: t("supply_benefit_1_body") },
        { title: t("supply_benefit_2_title"), body: t("supply_benefit_2_body") },
        { title: t("supply_benefit_3_title"), body: t("supply_benefit_3_body") },
    ];

    return (
        <section className="sup-section">
            {/* HERO SECTION */}
            <div className="sup-hero">

                {/* Background Video */}
                <video
                    className="sup-video"
                    src={ricebagsVideo}
                    autoPlay
                    loop
                    muted
                    playsInline
                />

                {/* Dark Overlay */}
                <div className="sup-video-overlay"></div>

                {/* Text Content */}
                <div className="sup-content sup-video-text">
                    <h2><strong>{t("supply_hero_title")}</strong></h2>
                    <h3>{t("supply_hero_subtitle")}</h3>
                    <p>{t("supply_hero_desc")}</p>
                </div>

            </div>

            <div className="sup-container">


                <WhatsAppChatWidget />
                <Climate />

                {/* OFFERINGS */}
                <div className="sup-leaf-decor">
                    <div className="sup-label">
                        <h3>{t("supply_offerings_heading")}</h3>
                    </div>

                    <div className="sup-card-grid">
                        {offerings.map((item, i) => (
                            <div className="sup-card" key={i}>
                                <div className="sup-title-item">{item.title}</div>
                                <div className="sup-body-item">{item.body}</div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* BENEFITS */}
                <div className="sup-leaf-decor">
                    <div className="sup-label">
                        <h3>{t("supply_benefits_heading")}</h3>
                    </div>

                    <div className="sup-card-grid">
                        {benefits.map((item, i) => (
                            <div className="sup-card" key={i}>
                                <div className="sup-title-item">{item.title}</div>
                                <div className="sup-body-item">{item.body}</div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* CTA BUTTON */}
                <div className="sup-button-container">
                    <Link to="/OnboardingForm">
                        <button className="sup-button">
                            {t("supply_button_cta")}
                        </button>
                    </Link>
                </div>

            </div>
        </section>
    );
};

export default SupplyFabriX;
