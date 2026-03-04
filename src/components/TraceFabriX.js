import React from "react";
import { Link } from "react-router-dom";
import "../styles/TraceFabriX.css";
import traceImage from "../images/TraceFabriX.jpg";
import { useLang } from "../components/LangContext"; // 👈 Import the custom hook
import WhatsAppChatWidget from "./WhatsAppChatWidget"; // Import the WhatsApp widget
import Climate from "./Climate";
import croptrack from "../images/croptrack.png";
import qualityComp from "../images/quality_comp.png";
import digitalCert from "../images/digital_cert.png";
import aiCrops from "../images/ai_crops.png";
import { color } from "framer-motion";

const TraceFabriX = () => {
  const { t } = useLang(); // 👈 Access the global translation function
  const offeringImages = [
    croptrack,
    qualityComp,
    digitalCert,
    aiCrops
  ];

  // Define offerings using translation keys
  const offerings = [
    {
      title: t("trace_offering_1_title"),
      body: t("trace_offering_1_body"),
    },
    {
      title: t("trace_offering_2_title"),
      body: t("trace_offering_2_body"),
    },
    {
      title: t("trace_offering_3_title"),
      body: t("trace_offering_3_body"),
    },
    {
      title: t("trace_offering_4_title"),
      body: t("trace_offering_4_body"),
    },
  ];

  // Define benefits using translation keys
  const benefits = [
    {
      title: t("trace_benefit_1_title"),
      body: t("trace_benefit_1_body"),
    },
    {
      title: t("trace_benefit_2_title"),
      body: t("trace_benefit_2_body"),
    },
    {
      title: t("trace_benefit_3_title"),
      body: t("trace_benefit_3_body"),
    },
  ];

  return (
    <section className="tracefabrx-section">
      {/* HERO SECTION */}
      <div className="tracefabrx-hero video-hero">

        {/* VIDEO BACKGROUND */}
        <video
          className="trace-hero-video"
          autoPlay
          loop
          muted
          playsInline
        >
          <source src={require("../images/trace_crop.mp4")} type="video/mp4" />
        </video>

        {/* OVERLAY */}
        <div className="trace-hero-overlay"></div>

        {/* TEXT CONTENT */}
        <div className="tracefabrx-content trace-hero-text">
          <h2><strong>{t("trace_hero_title")}</strong></h2>
          <h3>{t("trace_hero_subtitle")}</h3>
          <p>{t("trace_hero_desc")}</p>
        </div>

      </div>

      <div className="tracefabrx-container">


        <div className="tracefabrx-section-content leaf-decor">
          <div className="tracefabrx-label">
            <h3>{t("trace_offerings_heading")}</h3>
          </div>

          <div className="tracefabrx-card-grid fixed-2x2">
            {offerings.map((item, idx) => (
              <div
                className="tracefabrx-card"
                key={idx}
                style={{ backgroundImage: `url(${offeringImages[idx]})` }}
              >
                <div className="trace-card-overlay"></div>

                <div className="trace-card-content">
                  <div className="tracefabrx-title-item">{item.title}</div>
                  <div className="tracefabrx-body-item">{item.body}</div>
                </div>
              </div>
            ))}
          </div>
        </div>



        {/* HOW IT HELPS */}
        <div className="tracefabrx-benefits-section">
          <div className="tracefabrx-label">
            <h3 >{t("trace_benefits_heading")}</h3>
          </div>

          <div className="tracefabrx-benefits-grid three-col">
            {benefits.map((item, idx) => (
              <div className="tracefabrx-benefit-box" key={idx}>

                {/* White Icon Circle (placeholder) */}
                <div className="trace-benefit-icon">
                  <span>✔</span>
                </div>

                <h3 className="trace-benefit-title">{item.title}</h3>
                <p className="trace-benefit-body">{item.body}</p>
              </div>
            ))}
          </div>
        </div>

        <WhatsAppChatWidget />
        <Climate />
        {/* CTA BUTTON */}
        <div className="tracefabrx-button-container">
          <Link to="/OnboardingForm">
            <button className="tracefabrx-button">
              {t("trace_button_cta")}
            </button>
          </Link>
        </div>
      </div>
    </section>
  );
};

export default TraceFabriX;
