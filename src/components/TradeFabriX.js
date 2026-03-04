import React from 'react';
import { Link } from 'react-router-dom';
import "../styles/TradeFabriX.css";
import tradeImage from "../images/TradeFabriX.jpg";
import marketLinkVideo from "../images/marketlink.mp4";

import { useLang } from "../components/LangContext";
import WhatsAppChatWidget from "./WhatsAppChatWidget";
import Climate from "./Climate";

const TradeFabriX = () => {
  const { t } = useLang();

  // Define offerings using translation keys
  const offerings = [
    {
      title: t("trade_offering_1_title"),
      body: t("trade_offering_1_body"),
    },
    {
      title: t("trade_offering_2_title"),
      body: t("trade_offering_2_body"),
    },
    {
      title: t("trade_offering_3_title"),
      body: t("trade_offering_3_body"),
    },
    {
      title: t("trade_offering_4_title"),
      body: t("trade_offering_4_body"),
    }
  ];

  // Define benefits using translation keys
  const benefits = [
    {
      title: t("trade_benefit_1_title"),
      body: t("trade_benefit_1_body"),
    },
    {
      title: t("trade_benefit_2_title"),
      body: t("trade_benefit_2_body"),
    },
    {
      title: t("trade_benefit_3_title"),
      body: t("trade_benefit_3_body"),
    }
  ];

  return (
    <section className="trad-section">
      {/* HERO SECTION — VIDEO HERO */}
      <div className="trad-hero video-hero">

        {/* Background Video */}
        <video
          className="hero-video"
          autoPlay
          loop
          muted
          playsInline
        >
          <source src={marketLinkVideo} type="video/mp4" />
        </video>

        {/* Dark Overlay */}
        <div className="hero-overlay"></div>

        {/* Text on video */}
        <div className="hero-text">
          <h2><strong>{t("trade_hero_title")}</strong></h2>
          <h3>{t("trade_hero_subtitle")}</h3>
          <p>{t("trade_hero_desc")}</p>
        </div>

      </div>

      <div className="trad-container">


        {/* KEY OFFERINGS */}
        <div className="trad-section-content trad-leaf">
          <div className="trad-label">
            <h3>{t("trade_offerings_heading")}</h3>
          </div>
          <div className="trad-card-grid">
            {offerings.map((item, idx) => (
              <div className="trad-card" key={idx}>
                <div className="trad-title-item">{item.title}</div>
                <div className="trad-body-item">{item.body}</div>
              </div>
            ))}
          </div>
        </div>

        <WhatsAppChatWidget />
        <Climate />

        {/* HOW IT HELPS */}
        <div className="trad-section-content trad-leaf">
          <div className="trad-label">
            <h3>{t("trade_benefits_heading")}</h3>
          </div>
          <div className="trad-card-grid">
            {benefits.map((item, idx) => (
              <div className="trad-card" key={idx}>
                <div className="trad-title-item">{item.title}</div>
                <div className="trad-body-item">{item.body}</div>
              </div>
            ))}
          </div>
        </div>

        {/* CTA BUTTON */}
        <div className="trad-btn-container">
          <Link to="/OnboardingForm">
            <button className="trad-btn">
              {t("trade_button_cta")}
            </button>
          </Link>
        </div>

      </div>
    </section>
  );
};

export default TradeFabriX;
