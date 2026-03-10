
import React, { useState } from "react";
import { Link } from "react-router-dom";
import "../styles/AnnouncementBar.css";
// import { FaTractor, FaStore, FaChartLine } from "react-icons/fa"; // Assuming these icons are available or we can use text/emojis

const AnnouncementBar = () => {
    const [isHovered, setIsHovered] = useState(false);

    // Updated Agri-tech focused content
    const content = "🚀 EMPOWERING AGRICULTURE WITH TECHNOLOGY  |  🌿 NON-CHEMICAL SUSTAINABLE FARMING SOLUTIONS  |  💼 OWN AN AGRIFABRIX FRANCHISE TODAY  |  🚀 EMPOWERING AGRICULTURE WITH TECHNOLOGY  |  🌿 NON-CHEMICAL SUSTAINABLE FARMING SOLUTIONS  |  💼 OWN AN AGRIFABRIX FRANCHISE TODAY  |  ";

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
