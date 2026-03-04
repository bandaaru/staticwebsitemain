import React from "react";
import { Link } from "react-router-dom";
import "../styles/Financial.css";
import loan from "../images/loan.jpg";
import { FaMoneyCheckAlt, FaShoppingCart, FaFileInvoiceDollar } from "react-icons/fa";
import { useLang } from "../components/LangContext";
import WhatsAppChatWidget from "./WhatsAppChatWidget";
import Climate from "./Climate";
import farmerLoanVideo from "../images/farmer_loan.mp4";

const CreditFabriX = () => {
  const { t } = useLang();

  return (
    <section className="cred-section">
      {/* ================= HERO VIDEO ================= */}
      <div className="cred-hero">

        <video
          className="cred-video"
          autoPlay
          loop
          muted
          playsInline
        >
          <source src={farmerLoanVideo} type="video/mp4" />
        </video>

        <div className="cred-overlay"></div>

        <div className="cred-hero-text">
          <h2><strong>{t("credit_hero_title")}</strong></h2>
          <h3>{t("credit_hero_subtitle")}</h3>
          <p>{t("credit_hero_desc")}</p>
        </div>

      </div>

      <div className="cred-container">

        {/* ================= INTRO ================= */}
        <div className="cred-content leaf-decor"></div>

        <div className="cred-border cred-border-top"></div>

        <div className="cred-intro-box">
          <p>{t("credit_intro_p1")}</p>
          <p>{t("credit_intro_p2")}</p>
        </div>

        <div className="cred-border cred-border-bottom"></div>

        {/* ================= SOLUTIONS ================= */}
        <div className="cred-solutions">
          <div className="cred-solutions-grid">

            {/* Loan Card */}
            <div className="cred-solution-box">
              <div className="cred-solution-icon"><FaMoneyCheckAlt /></div>
              <h4>{t("loan_card_title")}</h4>
              <p className="cred-solution-sub">{t("loan_card_subtitle")}</p>

              <p>{t("loan_li_1")}</p>
              <p>{t("loan_li_2")}</p>
              <p>{t("loan_li_3")}</p>
              <p>{t("loan_li_4")}</p>

              <p><strong>{t("loan_benefits").split(":")[0]}:</strong> {t("loan_benefits").split(":")[1]}</p>
            </div>

            {/* BNPL Card */}
            <div className="cred-solution-box">
              <div className="cred-solution-icon"><FaShoppingCart /></div>
              <h4>{t("bnpl_card_title")}</h4>
              <p className="cred-solution-sub">{t("bnpl_card_subtitle")}</p>

              <p>{t("bnpl_li_1")}</p>
              <p>{t("bnpl_li_2")}</p>
              <p>{t("bnpl_li_3")}</p>
              <p>{t("bnpl_li_4")}</p>

              <p><strong>{t("bnpl_benefits").split(":")[0]}:</strong> {t("bnpl_benefits").split(":")[1]}</p>
            </div>

            {/* Invoice Card */}
            <div className="cred-solution-box">
              <div className="cred-solution-icon"><FaFileInvoiceDollar /></div>
              <h4>{t("invoice_card_title")}</h4>
              <p className="cred-solution-sub">{t("invoice_card_subtitle")}</p>

              <p>{t("invoice_li_1")}</p>
              <p>{t("invoice_li_2")}</p>
              <p>{t("invoice_li_3")}</p>
              <p>{t("invoice_li_4")}</p>

              <p><strong>{t("invoice_benefits").split(":")[0]}:</strong> {t("invoice_benefits").split(":")[1]}</p>
            </div>

          </div>
        </div>

        <WhatsAppChatWidget />
        <Climate />

        {/* ================= APPLY STEPS ================= */}
        <div className="cred-content leaf-decor">
          <div className="cred-label">
            <h3>{t("credit_apply_heading")}</h3>
          </div>

          <div className="cred-apply-steps">

            <div className="cred-apply-image">
              <img src={loan} alt={t("credit_apply_image_alt")} />
            </div>

            <div className="cred-step-list">

              <div className="cred-step-item">
                <div className="cred-step-number">1</div>
                <p><strong>{t("credit_apply_step_1").split(":")[0]}:</strong> {t("credit_apply_step_1").split(":")[1]}</p>
              </div>

              <div className="cred-step-item">
                <div className="cred-step-number">2</div>
                <p><strong>{t("credit_apply_step_2").split(":")[0]}:</strong> {t("credit_apply_step_2").split(":")[1]}</p>
              </div>

              <div className="cred-step-item">
                <div className="cred-step-number">3</div>
                <p><strong>{t("credit_apply_step_3").split(":")[0]}:</strong> {t("credit_apply_step_3").split(":")[1]}</p>
              </div>

            </div>

          </div>
        </div>

        {/* ================= WHY CHOOSE ================= */}
        <div className="cred-content leaf-decor">
          <div className="cred-label">
            <h3>{t("credit_why_choose_heading")}</h3>
          </div>

          <div className="cred-why-box">

            <ul>
              <li>{t("credit_why_li_1")}</li>
              <li>{t("credit_why_li_2")}</li>
              <li>{t("credit_why_li_3")}</li>
              <li>{t("credit_why_li_4")}</li>
            </ul>

            <p className="cred-highlight">{t("credit_why_highlight")}</p>

            <Link to="/OnboardingForm">
              <button className="cred-btn">{t("credit_button_apply")}</button>
            </Link>
          </div>
        </div>

      </div>
    </section>
  );
};

export default CreditFabriX;
