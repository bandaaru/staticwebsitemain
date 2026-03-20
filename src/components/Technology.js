import React, { useEffect } from 'react';
import '../styles/Technology.css';
import { FaRobot, FaDatabase, FaGlobe, FaLeaf, FaLock, FaChartLine } from 'react-icons/fa';
import TechnologyVideo from '../images/TechnologyVideo.mp4';
import { useLang } from "../components/LangContext"; // 👈 Import the custom hook
import WhatsAppChatWidget from "./WhatsAppChatWidget"; // Import the WhatsApp widget
import Climate from "./Climate"

const Technology = () => {
    const { t } = useLang(); // 👈 Access the global translation function

    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);
    
    return (
        <div className="technology">
            {/* Hero Section - Matched with Sustainability Format */}
            <div className="sus-hero">
                <video 
                    src={TechnologyVideo} 
                    className="sus-video" 
                    autoPlay 
                    loop 
                    muted 
                    playsInline
                />
                <div className="sus-overlay"></div>
                <div className="sus-hero-content">
                    <h2 className="sus-hero-title">
                        Technology<br />
                        <span style={{ fontSize: "0.6em", fontWeight: "bold" }}>(AI & Blockchain-Powered AgTech)</span>
                    </h2>
                    <p className="sus-hero-desc">{t("tech_hero_desc")}</p>
                </div>
            </div>

            {/* AI & ML Section */}
            <div className="tech-section">
                <h2>{t("tech_ai_heading")}</h2>
                <p>{t("tech_ai_desc")}</p>
                <div className="tech-grid-container">
                    <div className="grid-3">
                        <div className="service-card">
                            <div className="icon-wrapper"><FaRobot /></div>
                            <h4>{t("tech_ai_card_1_title")}</h4>
                            <p>{t("tech_ai_card_1_p")}</p>
                        </div>
                        <div className="service-card">
                            <div className="icon-wrapper"><FaChartLine /></div>
                            <h4>{t("tech_ai_card_2_title")}</h4>
                            <p>{t("tech_ai_card_2_p")}</p>
                        </div>
                        <div className="service-card">
                            <div className="icon-wrapper"><FaLeaf /></div>
                            <h4>{t("tech_ai_card_3_title")}</h4>
                            <p>{t("tech_ai_card_3_p")}</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Blockchain Section */}
            <div className="tech-section alt-bg">
                <h2>{t("tech_blockchain_heading")}</h2>
                <p>{t("tech_blockchain_desc")}</p>
                <div className="tech-grid-container">
                    <div className="grid-3">
                        <div className="service-card">
                            <div className="icon-wrapper"><FaDatabase /></div>
                            <h4>{t("tech_bc_card_1_title")}</h4>
                            <p>{t("tech_bc_card_1_p")}</p>
                        </div>
                        <div className="service-card">
                            <div className="icon-wrapper"><FaLock /></div>
                            <h4>{t("tech_bc_card_2_title")}</h4>
                            <p>{t("tech_bc_card_2_p")}</p>
                        </div>
                        <div className="service-card">
                            <div className="icon-wrapper"><FaGlobe /></div>
                            <h4>{t("tech_bc_card_3_title")}</h4>
                            <p>{t("tech_bc_card_3_p")}</p>
                        </div>
                    </div>
                </div>
            </div>
             <WhatsAppChatWidget />
             <Climate/>

            {/* Digital Twin Section */}
            <div className="tech-section">
                <h2>{t("tech_digital_twin_heading")}</h2>
                <p>{t("tech_digital_twin_desc")}</p>
                <div className="tech-grid-container">
                    <div className="grid-3">
                        <div className="service-card">
                            <div className="icon-wrapper"><FaGlobe /></div>
                            <h4>{t("tech_dt_card_1_title")}</h4>
                            <p>{t("tech_dt_card_1_p")}</p>
                        </div>
                        <div className="service-card">
                            <div className="icon-wrapper"><FaLeaf /></div>
                            <h4>{t("tech_dt_card_2_title")}</h4>
                            <p>{t("tech_dt_card_2_p")}</p>
                        </div>
                        <div className="service-card">
                            <div className="icon-wrapper"><FaDatabase /></div>
                            <h4>{t("tech_dt_card_3_title")}</h4>
                            <p>{t("tech_dt_card_3_p")}</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Why AgriFabriX? */}
            <div className="why-agri">
                <h2>Why AgriFabriX's Technology is a Game Changer</h2>
                <div className="benefits">
                    <div className="benefit"><FaChartLine className="tech-icon" /> <p>{t("tech_why_li_1")}</p></div>
                    <div className="benefit"><FaLock className="tech-icon" /> <p>{t("tech_why_li_2")}</p></div>
                    <div className="benefit"><FaGlobe className="tech-icon" /> <p>{t("tech_why_li_3")}</p></div>
                    <div className="benefit"><FaLeaf className="tech-icon" /> <p>{t("tech_why_li_4")}</p></div>
                    <div className="benefit"><FaDatabase className="tech-icon" /> <p>{t("tech_why_li_5")}</p></div>
                </div>
            </div>
        </div>
    );
};

export default Technology;