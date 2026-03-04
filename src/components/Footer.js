import React, { useState } from "react";
import "../styles/Footer.css";
import logo from "../images/l.png";
import { FaFacebook, FaLinkedin, FaWhatsapp, FaYoutube } from "react-icons/fa";
import { FaXTwitter } from "react-icons/fa6";
import { FaInstagram } from "react-icons/fa6";
import { useLang } from "../components/LangContext"; // 👈 Import the custom hook

const Footer = () => {
  const { t } = useLang(); // 👈 Access the global translation function
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      // Use translated alert message
      alert(t("footer_alert_valid_email"));
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("https://admin.agrifabrix.in/api/static/Subscribe", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();

      if (response.ok) {
        // Use translated alert messages, falling back to data.message
        alert(data.message || t("footer_alert_success"));
        setEmail("");
      } else {
        // Use translated alert messages, falling back to data.error
        alert(data.error || t("footer_alert_failed"));
      }
    } catch (error) {
      // Use translated alert message for network/catch error
      alert(t("footer_alert_error"));
      console.error("Error subscribing:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-logo-section">
          <img
            src={logo}
            alt={t("footer_logo_alt")} // 👈 Translated alt text
            className="footer-logo"
          />
          <div className="footer-social-icons">
            <div className="social-icons">
              <a href="https://www.linkedin.com/company/agrifabrix/" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn"><FaLinkedin /></a>
              {/* <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" aria-label="X"><FaXTwitter /></a> */}
              <a href="https://www.instagram.com/agrifabrix_123/" target="_blank" rel="noopener noreferrer" aria-label="X"><FaInstagram /></a>
              <a href="https://www.facebook.com/people/Samruddhi-Eco-Agrifabrix/61572279958575/" target="_blank" rel="noopener noreferrer" aria-label="Facebook"><FaFacebook /></a>
              <a href="https://youtube.com/@samruddhiecoagrifabrix?si=0ODm3aDBH7niGv4e" target="_blank" rel="noopener noreferrer" aria-label="YouTube"><FaYoutube /></a>
              <a href={`https://wa.me/${7075483505}`} target="_blank" rel="noopener noreferrer" aria-label="WhatsApp"><FaWhatsapp /></a>
            </div>
          </div>
          {/* Note: The address itself is considered static/non-translatable data */}
          <p className="company-desc">
            T-Hub,Phase 2, Plot No 1/C, Sy No 83/1, Raidurgam,<br />
            Knowledge City Rd, Panmaktha, Serilingampalle, Hyderabad, Telangana 500081.
          </p>
          {/* <p className="company-desc" >
            {t("footer_address")}
          </p> */}
        </div>

        <div className="footer-sections">

          {/* Company Section */}
          <div className="footer-nav">
            <h2>{t("footer_company_heading")}</h2>
            <ul>
              <li><a href="/About">{t("footer_link_about")}</a></li>
              <li><a href="/About">{t("footer_link_leadership")}</a></li>
              <li><a href="/Careers">{t("careers")}</a></li>
              <li><a href="/partners">{t("footer_link_partners")}</a></li>
            </ul>
          </div>

          {/* Solutions Section */}
          <div className="footer-nav">
            <h2>{t("footer_solutions_heading")}</h2>
            <ul>
              <li><a href="https://store.agrifabrix.in/" target="_blank" rel="noopener noreferrer">{t("footer_link_marketplace")}</a></li>
              <li><a href="/CreditFabriX">{t("footer_link_financial")}</a></li>
              <li><a href="/Sustainability">{t("footer_link_sustainability")}</a></li>
              <li><a href="/Solutions">{t("footer_link_ai_blockchain")}</a></li>
            </ul>
          </div>

          {/* Support & Resources Section */}
          <div className="footer-nav">
            <h2>{t("footer_support_heading")}</h2>
            <ul>
              <li><a href="/Contact">{t("footer_link_help_center")}</a></li>
              <li><a href="/Contact">{t("footer_link_support")}</a></li>
              <li><a href="/contact">{t("footer_link_contact")}</a></li>
              <li><a href="/PrivacyPolicy">{t("footer_link_privacy")}</a></li>
              <li><a href="/CancellationPolicy">{t("footer_link_cancellation")}</a></li>
              <li><a href="/TermsAndConditions">{t("footer_link_terms")}</a></li>
              <li><a href="/ShippingPolicy">{t("footer_link_shipping")}</a></li>
            </ul>
          </div>

          {/* Newsletter Section */}
          <div className="footer-subscribe">
            <h2>{t("footer_newsletter_heading")}</h2>
            <p>{t("footer_newsletter_desc")}</p>
            <form className="subscribe-form" onSubmit={handleSubmit}>
              <input
                type="email"
                placeholder={t("footer_email_placeholder")} // 👈 Translated placeholder
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <button type="submit" disabled={loading}>
                {/* Translated button text based on loading state */}
                {loading ? t("footer_subscribing_text") : t("footer_subscribe_button")}
              </button>
            </form>
          </div>
        </div>
      </div>

      {/* Footer Bottom Section (Copyright) */}
      <div className="footer-bottom">
        <p>{t("footer_copyright")}</p>
      </div>
    </footer>
  );
};

export default Footer;