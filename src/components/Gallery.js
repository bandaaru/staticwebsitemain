import React, { useState } from "react";
import "../styles/Gallery.css";
import logo from "../images/l.png";
import { useLang } from "./LangContext";

// Import real images from the images directory
import img1 from "../images/AgriTech.jpg";
import img2 from "../images/FPO.jpeg";
import img3 from "../images/Tractor.jpeg";
import img4 from "../images/ai_crops.png";
import img5 from "../images/banana_high_tech_farm.png";
import img7 from "../images/Overview.jpg";
import img8 from "../images/Solutions.jpg";

// Sub-gallery images (reusing some for demonstration)
import sub1_1 from "../images/Ai.jpg";
import sub1_2 from "../images/AgriTech.jpg";
import sub2_1 from "../images/FPO.jpeg";
import sub2_2 from "../images/Overview.jpg";
import sub3_1 from "../images/Tractor.jpeg";
import sub3_2 from "../images/HomeTech.jpg";

import { Link } from "react-router-dom";

const CategoryCardSlider = ({ images, title, category, onClick }) => {
    const [currentIndex, setCurrentIndex] = React.useState(0);

    React.useEffect(() => {
        if (images.length <= 1) return;

        const interval = setInterval(() => {
            setCurrentIndex((prevIndex) => (prevIndex + 1) % images.length);
        }, 2500); // Slightly faster for smoother feel

        return () => clearInterval(interval);
    }, [images.length]);

    return (
        <div className="gallery-card" onClick={onClick}>
            <div className="image-wrapper slider-wrapper">
                {images.map((img, index) => (
                    <img
                        key={img.id}
                        src={img.src}
                        alt={`${title} - ${index + 1}`}
                        className={`slider-image ${index === currentIndex ? 'active' : ''}`}
                    />
                ))}
                <div className="card-overlay">
                    <div className="overlay-content">
                        <span className="card-category">{category}</span>
                        <h3>{title}</h3>
                        <div className="card-action">
                            <span>Explore Photos</span>
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

const Gallery = () => {
    const { t } = useLang();
    const [activeSection, setActiveSection] = useState(null);

    const gallerySections = [
        {
            id: 1,
            src: img1,
            title: "Smart Agri-Tech",
            category: "Innovation",
            images: [
                { id: 101, src: sub1_1, title: "Precision Farming" },
                { id: 102, src: sub1_2, title: "Smart Irrigation" },
                { id: 103, src: img4, title: "Crop Monitoring" }
            ]
        },
        {
            id: 2,
            src: img2,
            title: "FPO Engagement",
            category: "Community",
            images: [
                { id: 201, src: sub2_1, title: "Farmer Meet" },
                { id: 202, src: sub2_2, title: "Digital Literacy Workshop" }
            ]
        },
        {
            id: 3,
            src: img3,
            title: "Modern Mechanization",
            category: "Infrastructure",
            images: [
                { id: 301, src: sub3_1, title: "Advanced Tractors" },
                { id: 302, src: sub3_2, title: "IoT in Farming" }
            ]
        },
        {
            id: 4,
            src: img4,
            title: "AI-Driven Insights",
            category: "Technology",
            images: [
                { id: 401, src: img4, title: "AI Analysis" },
                { id: 402, src: sub1_1, title: "Data Visualization" }
            ]
        },
        {
            id: 5,
            src: img5,
            title: "High-Tech Farming",
            category: "Sustainability",
            images: [
                { id: 501, src: img5, title: "Greenhouse Tech" },
                { id: 502, src: img1, title: "Sustainable Methods" }
            ]
        },
        {
            id: 7,
            src: img7,
            title: "Operational Excellence",
            category: "Overview",
            images: [
                { id: 701, src: img7, title: "Workflow Management" },
                { id: 702, src: img8, title: "Logistics Optimization" }
            ]
        },
        {
            id: 8,
            src: img8,
            title: "Strategic Solutions",
            category: "Business",
            images: [
                { id: 801, src: img8, title: "Market Strategy" },
                { id: 802, src: img2, title: "Farmer Collaboration" }
            ]
        },
    ];

    const handleCardClick = (sectionId) => {
        setActiveSection(sectionId);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const handleBack = () => {
        setActiveSection(null);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const currentSection = gallerySections.find(s => s.id === activeSection);

    return (
        <div className="gallery-page">
          

            <div className="gallery-container">
                {!activeSection ? (
                    <>
                        <div className="gallery-header">
                            <span className="pre-title">Our Visual Journey</span>
                            <h2>AgriFabriX in Action</h2>
                            <div className="underline"></div>
                        </div>

                        <div className="gallery-grid">
                            {gallerySections.map((section) => (
                                <CategoryCardSlider
                                    key={section.id}
                                    images={section.images}
                                    title={section.title}
                                    category={section.category}
                                    onClick={() => handleCardClick(section.id)}
                                />
                            ))}
                        </div>
                    </>
                ) : (
                    <div className="sub-gallery">
                        <div className="sub-gallery-header">
                            <button className="back-button" onClick={handleBack}>
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
                                Back to Gallery
                            </button>
                            <div className="section-title">
                                <span className="pre-title">{currentSection.category}</span>
                                <h2>{currentSection.title}</h2>
                            </div>
                        </div>

                        <div className="sub-gallery-grid">
                            {currentSection.images.map((img) => (
                                <div key={img.id} className="sub-gallery-item">
                                    <div className="sub-image-wrapper">
                                        <img src={img.src} alt={img.title} />
                                        <div className="sub-item-info">
                                            <h3>{img.title}</h3>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                <div className="gallery-cta">
                    <div className="cta-content">
                        <h3>Be Part of Our Story</h3>
                        <p>We are constantly growing and capturing new milestones. Join us in revolutionizing the future of farming.</p>
                        <Link to="/OnboardingForm" className="cta-button">Partner With Us</Link>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Gallery;
