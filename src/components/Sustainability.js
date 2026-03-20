import React, { useEffect } from "react";
import "../styles/Sustainable.css"; // Kept for backward compatibility
import sustainabilityVideo from "../images/sustainabilityVideo.mp4";
// import sustainableBg from "../images/Susatainable.png"; // Unused in original, commented out
import { useLang } from "../components/LangContext";
import WhatsAppChatWidget from "./WhatsAppChatWidget";
import Climate from "./Climate";

const Sustainability = () => {
  const { t } = useLang();

  // Scroll to top when page loads
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <div className="sustainability-modern-wrapper" style={{ width: "100%", minHeight: "100vh", backgroundColor: "#fdfdfd" }}>
      <style>{`
        .sus-hero {
          position: relative;
          height: 80vh;
          min-height: 500px;
          display: flex;
          align-items: center;
          justify-content: center;
          overflow: hidden;
        }
        .sus-video {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          object-fit: cover;
          z-index: 0;
        }
        .sus-overlay {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, rgba(10, 40, 20, 0.8) 100%);
          z-index: 1;
        }
        .sus-hero-content {
          position: relative;
          z-index: 2;
          text-align: center;
          color: #ffffff;
          max-width: 800px;
          padding: 0 20px;
          animation: fadeUpIn 1.2s ease-out forwards;
        }
        .sus-hero-title {
          font-size: 3.5rem;
          font-weight: 800;
          margin-bottom: 20px;
          letter-spacing: -0.5px;
          line-height: 1.2;
          text-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        .sus-hero-desc {
          font-size: 1.25rem;
          font-weight: 400;
          opacity: 0.95;
          text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        .sus-main {
          max-width: 1200px;
          margin: 0 auto;
          padding: 80px 24px;
          font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
          color: #333;
        }
        .sus-section {
          margin-bottom: 100px;
        }
        .sus-section-title {
          font-size: 1.8rem;
          font-weight: 800;
          color: #115e59; /* Modern teal/green */
          margin-bottom: 24px;
          text-align: center;
        }
        .sus-section-title::after {
          content: "";
          display: block;
          width: 80px;
          height: 4px;
          background: linear-gradient(90deg, #10b981, #059669);
          margin: 16px auto 0;
          border-radius: 4px;
        }
        .sus-text {
          font-size: 1.125rem;
          line-height: 1.8;
          color: #4b5563;
          text-align: center;
          max-width: 850px;
          margin: 0 auto 24px;
        }
        .sus-esg-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
          gap: 32px;
          margin-top: 60px;
        }
        .sus-esg-card {
          background: #ffffff;
          border-radius: 20px;
          padding: 40px 32px;
          box-shadow: 0 10px 40px rgba(0, 0, 0, 0.04);
          transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
          border: 1px solid #f3f4f6;
          border-top: 6px solid #10b981;
          display: flex;
          flex-direction: column;
        }
        .sus-esg-card:hover {
          transform: translateY(-12px);
          box-shadow: 0 20px 40px rgba(16, 185, 129, 0.12);
        }
        .sus-esg-card h3 {
          font-size: 1.5rem;
          font-weight: 700;
          color: #064e3b;
          margin-bottom: 24px;
          display: flex;
          align-items: center;
          gap: 12px;
        }
        .sus-esg-card ul {
          list-style: none;
          padding: 0;
          margin: 0;
          flex-grow: 1;
        }
        .sus-esg-card li {
          margin-bottom: 16px;
          padding-left: 32px;
          position: relative;
          color: #4b5563;
          line-height: 1.6;
          font-size: 1.05rem;
        }
        .sus-esg-card li::before {
          content: "✓";
          position: absolute;
          left: 0;
          top: 0;
          color: #ffffff;
          background: linear-gradient(135deg, #10b981, #059669);
          width: 20px;
          height: 20px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 12px;
          font-weight: bold;
          margin-top: 4px;
        }
        @keyframes fadeUpIn {
          0% { opacity: 0; transform: translateY(30px); }
          100% { opacity: 1; transform: translateY(0); }
        }
        
        /* Staggered animations for elements */
        .sus-animate-1 { animation: fadeUpIn 1s cubic-bezier(0.16, 1, 0.3, 1) 0.2s both; }
        .sus-animate-2 { animation: fadeUpIn 1s cubic-bezier(0.16, 1, 0.3, 1) 0.4s both; }
        .sus-animate-3 { animation: fadeUpIn 1s cubic-bezier(0.16, 1, 0.3, 1) 0.6s both; }

        @media (max-width: 768px) {
          .sus-hero { height: 60vh; min-height: 400px; }
          .sus-hero-title { font-size: 2.25rem; }
          .sus-hero-desc { font-size: 1.1rem; }
          .sus-section-title { font-size: 2rem; }
          .sus-esg-grid { grid-template-columns: 1fr; }
          .sus-main { padding: 50px 16px; }
        }
      `}</style>

      {/* Hero Section */}
      <div className="sus-hero">
        <video
          src={sustainabilityVideo}
          className="sus-video"
          autoPlay
          loop
          muted
          playsInline
        />
        <div className="sus-overlay"></div>
        <div className="sus-hero-content">
          <h2 className="sus-hero-title">{t("sustain_hero_title")}</h2>
          <p className="sus-hero-desc">{t("sustain_hero_desc")}</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="sus-main">
        {/* Intro Section */}
        <div className="sus-section sus-animate-1">
          <p className="sus-text" style={{ fontSize: "1.25rem", color: "#374151" }}>
            {t("sustain_intro_p1")}
          </p>
          <p className="sus-text">
            {t("sustain_intro_p2")}
          </p>
        </div>

        {/* Commitment Section */}
        <div className="sus-section sus-animate-2">
          <h2 className="sus-section-title">{t("sustain_commitment_heading")}</h2>
          <p className="sus-text">{t("sustain_commitment_p")}</p>
        </div>

        {/* ESG Section */}
        <div className="sus-section sus-animate-3">
          <h2 className="sus-section-title">{t("sustain_esg_heading")}</h2>
          <div className="sus-esg-grid">
            <div className="sus-esg-card">
              <h3>{t("sustain_esg_e_title")}</h3>
              <ul>
                <li>{t("sustain_esg_e_li_1")}</li>
                <li>{t("sustain_esg_e_li_2")}</li>
                <li>{t("sustain_esg_e_li_3")}</li>
              </ul>
            </div>
            <div className="sus-esg-card">
              <h3>{t("sustain_esg_s_title")}</h3>
              <ul>
                <li>{t("sustain_esg_s_li_1")}</li>
                <li>{t("sustain_esg_s_li_2")}</li>
                <li>{t("sustain_esg_s_li_3")}</li>
              </ul>
            </div>
            <div className="sus-esg-card">
              <h3>{t("sustain_esg_g_title")}</h3>
              <ul>
                <li>{t("sustain_esg_g_li_1")}</li>
                <li>{t("sustain_esg_g_li_2")}</li>
                <li>{t("sustain_esg_g_li_3")}</li>
              </ul>
            </div>
          </div>
        </div>

        <WhatsAppChatWidget />
        <Climate />

        {/* Game Changer Section */}
        <div className="sus-section sus-animate-3" style={{ marginTop: "80px", textAlign: "center" }}>
          <h2 className="sus-section-title">
            {t("sustain_game_changer_heading")}
          </h2>
          <p className="sus-text" style={{ maxWidth: "900px", fontSize: "1.25rem", lineHeight: "2", textAlign: "center", margin: "30px auto" }}>
            <span style={{ fontWeight: "700", color: "#059669" }}>{t("sustain_changer_li_1")}</span>
            <span style={{ margin: "0 12px", color: "#d1d5db" }}>|</span>
            <span style={{ fontWeight: "700", color: "#059669" }}>{t("sustain_changer_li_2")}</span>
            <span style={{ margin: "0 12px", color: "#d1d5db" }}>|</span>
            <span style={{ fontWeight: "700", color: "#059669" }}>{t("sustain_changer_li_3")}</span>
            <span style={{ margin: "0 12px", color: "#d1d5db" }}>|</span>
            <span style={{ fontWeight: "700", color: "#059669" }}>{t("sustain_changer_li_4")}</span>
          </p>
          <p style={{ maxWidth: "850px", margin: "40px auto 100px", fontSize: "1.2rem", color: "#4b5563", lineHeight: "1.8", fontWeight: "500" }}>
            {t("sustain_closing_p")}
          </p>
        </div>
      </div>
    </div>
  );
};

export default Sustainability;