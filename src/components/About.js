
import React from "react";
import "../styles/About.css";
import ceoImage from "../images/1.jpg";
import cfoImage from "../images/2.jpg";
import Climate from "./Climate"

import {
  FaLeaf,
  FaEye,
  FaLightbulb,
  FaHandHoldingUsd,
  FaUsers,
  FaLinkedin,
} from "react-icons/fa";
import overviewImage from "../images/Overview.jpg";
import journeyImage from "../images/Mission.jpg";
import WhatsAppChatWidget from "./WhatsAppChatWidget"; // Import the WhatsApp widget
import { useLang } from "../components/LangContext"; // 👈 Import the custom hook

const About = () => {
  const { t } = useLang(); // 👈 Access the global translation function

  // Founders data updated to use translation keys for designation
  const founders = [
    {
      name: "Mendu Srinivasulu",
      designationKey: "designation_ceo", // Use key
      image: ceoImage,
      linkedin: "https://www.linkedin.com/in/mendu-srinivasulu-65731817/",
    },
    {
      name: "Suresh Naraparaju",
      designationKey: "designation_cfo", // Use key
      image: cfoImage,
      linkedin: "https://www.linkedin.com/in/suresh-naraparaju",
    },
  ];

  return (
    <div className="about-us">
      {/* Hero Section */}
      <header className="her-section">
        <h1>{t("about_hero_heading")}</h1>
      </header>

      {/* Company Overview */}
      <section className="company-overview">
        <div className="overview-content">

          {/* LEFT SIDE – VIDEO */}
          <video
            className="overview-video"
            // src={require("../images/happy_farmer.mp4")}
            src={require("../images/about.mp4")}
            autoPlay
            muted
            loop
            playsInline
          />

          {/* RIGHT SIDE – TEXT */}
          <div className="text-content">
            <h2>{t("about_overview_heading")}</h2>
            <p>{t("about_overview_para")}</p>
            <ul>
              <li>{t("about_overview_li_1")}</li>
              <li>{t("about_overview_li_2")}</li>
              <li>{t("about_overview_li_3")}</li>
            </ul>
          </div>

        </div>
      </section>

      <WhatsAppChatWidget />
      <Climate />
      {/* Mission Section */}
      <section className="journey-section">
        <div className="journey-content">

          {/* LEFT SIDE — TEXT */}
          <div className="journey-text-content">
            <h2>{t("about_mission_heading")}</h2>
            <p>{t("about_mission_subtext")}</p>
            <ul>
              <li>{t("about_mission_li_1")}</li>
              <li>{t("about_mission_li_2")}</li>
              <li>{t("about_mission_li_3")}</li>
            </ul>
          </div>

          {/* RIGHT SIDE — VIDEO */}
          <video
            className="journey-video"
            // src={require("../images/farmer_walking.mp4")}
            src={require("../images/pesti.mp4")}
            autoPlay
            loop
            muted
            playsInline
          />
        </div>
      </section>


      {/* Core Values */}
      <section className="values-section">
        <div className="value-slice">
          <div className="value-text-wrapper">
            <h3>{t("value_sustainability_title")}</h3>
            <p>{t("value_sustainability_desc")}</p>
          </div>
        </div>

        <div className="value-slice">
          <div className="value-text-wrapper">
            <h3>{t("value_transparency_title")}</h3>
            <p>{t("value_transparency_desc")}</p>
          </div>
        </div>

        <div className="value-slice">
          <div className="value-text-wrapper">
            <h3>{t("value_innovation_title")}</h3>
            <p>{t("value_innovation_desc")}</p>
          </div>
        </div>

        <div className="value-slice">
          <div className="value-text-wrapper">
            <h3>{t("value_financial_title")}</h3>
            <p>{t("value_financial_desc")}</p>
          </div>
        </div>

        <div className="value-slice">
          <div className="value-text-wrapper">
            <h3>{t("value_collaboration_title")}</h3>
            <p>{t("value_collaboration_desc")}</p>
          </div>
        </div>
      </section>



      {/* Founders & Leadership */}
      <section className="leadership">
        <h2>{t("about_leadership_heading")}</h2>
        <div className="leaders-container">
          {founders.map((founder, index) => (
            <div className="leader" key={index}>
              <div className="leader-image-container">
                <img
                  src={founder.image}
                  alt={founder.name}
                  className="leader-image"
                />
                <a
                  href={founder.linkedin}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="linkedin-icon"
                  aria-label={`LinkedIn profile for ${founder.name}`}
                >
                  <FaLinkedin />
                </a>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Founders Message */}
      <section className="founders-message">
        <h2>{t("about_message_heading")}</h2>
        <p>{t("about_message_para")}</p>
        <h3>{t("about_message_cta")}</h3>
      </section>
    </div>
  );
};

export default About;