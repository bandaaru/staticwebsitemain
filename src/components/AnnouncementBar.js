
import React, { useState } from "react";
import { Link } from "react-router-dom";
import "../styles/AnnouncementBar.css";
import { useLang } from "../components/LangContext";

const AnnouncementBar = () => {
    const [isHovered, setIsHovered] = useState(false);
    const { t } = useLang();

    const content = t("announcement_bar_content");

    return (
        <div
            className="announcement-bar"
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
        >
            <Link to="/franchise" className="announcement-link">
                <div className={`marquee ${isHovered ? "paused" : ""} `}>
                    <div className="marquee-content">
                        {content}
                    </div>
                    {/* Duplicate for seamless finish */}
                    <div className="marquee-content">
                        {content}
                    </div>
                </div>
            </Link>
        </div>
    );
};

export default AnnouncementBar;
