import React, { useState, useEffect, useRef } from "react";
import { IoIosArrowBack, IoIosArrowForward } from "react-icons/io";
import capital from "../images/thub.jpg";

import {
  FaSeedling,
  FaShoppingCart,
  FaHandshake,
  FaTruck,
  FaMapMarkedAlt,
  FaUsers,
  FaBriefcase,
  FaBoxOpen,
  FaStore
} from "react-icons/fa";

import "../styles/HomePage.css";

import green_crop from "../images/green_crop.mp4";
import mission from "../images/Vision.png";
import home from "../images/home.mp4";

import inputs from "../images/inputs.png";
import orders from "../images/orders.png";
import consultancy from "../images/consultancy.png";
import supplychain from "../images/supplychain.png";
import franchiseCard from "../images/franchisecard.png";

import { useLang } from "../components/LangContext";
import WhatsAppChatWidget from "./WhatsAppChatWidget";
import Climate from "./Climate";
import { FaXTwitter, FaFacebookF, FaLinkedin, FaInstagram, FaWhatsapp } from "react-icons/fa6";

import logo1 from "../images/capsber.png";
import logo2 from "../images/infarmsys.jpg";
import logo3 from "../images/dibbble.png";
import logo4 from "../images/aigenix.png";
import logo5 from "../images/fin.png";
import logo6 from "../images/nyasta.png";
import logo7 from "../images/yk.png";
import logo8 from "../images/osc.png";
import logo9 from "../images/bal.png";
import logo10 from "../images/rukart.png";
import logo11 from "../images/viswa.png";
import logo12 from "../images/efpolymer.png";


const CountUp = ({ target, duration = 2000 }) => {
  const [count, setCount] = useState(0);
  const elementRef = useRef(null);
  const [hasStarted, setHasStarted] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !hasStarted) {
          setHasStarted(true);
        }
      },
      { threshold: 0.1 }
    );

    if (elementRef.current) {
      observer.observe(elementRef.current);
    }

    return () => observer.disconnect();
  }, [hasStarted]);

  useEffect(() => {
    if (!hasStarted) return;

    let start = 0;
    const increment = target / (duration / 16);
    const timer = setInterval(() => {
      start += increment;
      if (start >= target) {
        setCount(target);
        clearInterval(timer);
      } else {
        setCount(Math.floor(start));
      }
    }, 16);

    return () => clearInterval(timer);
  }, [hasStarted, target, duration]);

  return <span ref={elementRef}>{count}+</span>;
};

const HomePage = () => {
  const { t } = useLang();


  const [showContactInterests, setShowContactInterests] = useState(false);




  const [currentSlide, setCurrentSlide] = useState(1);
  const [zoomOut, setZoomOut] = useState(false);


  const logos = [
    logo1,
    logo2,
    logo3,
    logo4,
    logo5,
    logo6,
    logo7,
    logo8,
    logo9,
    logo10,
    logo11,
    logo12
  ];
  const partnerLinks = [
    "https://capsber.com/",
    "https://farmsys.co/",
    "https://dibbleag.com/",
    "https://www.ai-genix.net/",
    "https://finozen.co.in/",
    "https://nyasta.in/",
    "https://yklaboratories.com/",
    "https://oscillomachines.com/",
    "https://www.balwaan.in/",
    "https://rukart.co/",
    "https://www.vishwaagrotech.com/",
    "https://efpolymer.com/",
  ];
  const [formData, setFormData] = useState({
    firstName: "",
    surname: "",
    email: "",
    phone: "",
    message: "",
    interests: []
  });
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };
  const handleCheckboxChange = (e) => {
    const { value, checked } = e.target;
    setFormData((prev) => {
      if (checked) {
        return { ...prev, interests: [...prev.interests, value] };
      } else {
        return {
          ...prev,
          interests: prev.interests.filter((item) => item !== value),
        };
      }
    });
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.interests.length === 0) {
      alert("Please select at least one interest.");
      return;
    }
    try {
      const response = await fetch("https://admin.agrifabrix.in/api/static/Contact", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      if (response.ok) {
        // Use translated success alert
        alert(t("contact_alert_success"));
        setFormData({ firstName: "", surname: "", email: "", phone: "", message: "", interests: [] });
      } else {
        // Use translated failure alert
        alert(data.error || t("contact_alert_failed"));
        console.error("Server Error:", data);
      }
    } catch (err) {
      // Use translated error alert
      alert(t("contact_alert_error"));
      console.error("Fetch Error:", err);
    }
  };

  useEffect(() => {
    let lastY = window.scrollY;

    const handleScroll = () => {
      const current = window.scrollY;

      if (current > lastY) {
        setZoomOut(true);   // scroll down → zoom OUT
      } else {
        setZoomOut(false);  // scroll up → zoom IN
      }

      lastY = current;
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);




const slides = [
  {
    title: t("home_slide_1_title"),
    description: t("home_slide_1_desc"),
    video: green_crop,
    link: "/Solutions",
  },
  {
    title: t("home_slide_2_title"),
    description: t("home_slide_2_desc"),
    video: home,
    link: "/Technology",
  },
];

  const prevSlide = () => {
    setCurrentSlide((prev) =>
      prev === 0 ? slides.length - 1 : prev - 1
    );
  };

  const nextSlide = () => {
    setCurrentSlide((prev) =>
      prev === slides.length - 1 ? 0 : prev + 1
    );
  };

  // ⭐ AUTO SLIDE EVERY 8 SECONDS ⭐
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentSlide((prev) =>
        prev === slides.length - 1 ? 0 : prev + 1
      );
    }, 8000);

    return () => clearInterval(interval);
  }, [slides.length]);


  // ⭐ SCROLL ANIMATION TRIGGER ⭐
  useEffect(() => {
    const elements = document.querySelectorAll(
      ".fade-in-up, .fade-in-left, .fade-in-right"
    );

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("show");
          }
        });
      },
      { threshold: 0.2 }
    );

    elements.forEach((el) => observer.observe(el));
  }, []);


  return (
    <div className="homepage">



      {/* ================= HERO CAROUSEL ================= */}
<section className="hero-carousel" id="home">

  <div className="hero-slide" key={currentSlide}>

    {/* Video or Image */}
    {slides[currentSlide].video ? (
      <video
        className="hero-carousel-video"
        autoPlay
        muted
        loop
        playsInline
      >
        <source src={slides[currentSlide].video} type="video/mp4" />
      </video>
    ) : (
      <img
        src={slides[currentSlide].image}
        alt={t("home_image_alt_crop")}
        className="hero-carousel-image"
      />
    )}

    {/* Text on media */}
    <div
      className={`hero-text-overlay no-overlay-text 
      ${currentSlide === 0 ? "first-slide-spacing" : ""}
      ${currentSlide === 1 ? "text-right-slide black-text" : ""}
      `}
    >
      <h1>{slides[currentSlide].title}</h1>
      <p>{slides[currentSlide].description}</p>

      <a href={slides[currentSlide].link} className="learn-more">
        {t("home_button_learn_more")}
      </a>
    </div>

  </div>

</section>



      <section className="highlights">

        <div className="highlight ai">
          <div className="highlight-text">
            <h1>{t("home_highlight_ai_title")}</h1>
            <p>{t("home_highlight_ai_desc")}</p>
          </div>
        </div>

        <div className="highlight finance">
          <div className="highlight-text">
            <h1>{t("home_highlight_finance_title")}</h1>
            <p>{t("home_highlight_finance_desc")}</p>
          </div>
        </div>

        <div className="highlight blockchain">
          <div className="highlight-text">
            <h1>{t("home_highlight_blockchain_title")}</h1>
            <p>{t("home_highlight_blockchain_desc")}</p>
          </div>
        </div>

      </section>


      <div className="section-border top-border"></div>

      <section className="vision-mission new-layout paint-section">

        <div className="vision-section">   {/* ⭐ Missing wrapper added */}

          <div className="vision-image-box">
            <img
              src={mission}
              alt={t("home_image_alt_mission")}
              className={zoomOut ? "zoom-out" : ""}
            />
          </div>

          <div className="vision-text-box">
            <h2>{t("home_vision_heading")}</h2>
            <p>{t("home_vision_text")}</p>

            <h2>{t("home_mission_heading")}</h2>
            <p>{t("home_mission_text")}</p>
          </div>

        </div>

      </section>
      <div className="section-border bottom-border"></div>


      {/* ================= FRANCHISE PROMO SECTION ================= */}
      <section className="franchise-promo-container">
        <div className="franchise-promo-card">
          
          <div className="franchise-promo-left">
            <div className="promo-trust-text">
              <span className="trust-black">Build Trust First </span>
              <span className="trust-green">DIGITISE </span>
              <span className="trust-black">Later </span>
              <span className="trust-orange">FRANCHISE </span>
              <span className="trust-red">Only When Ready</span>
            </div>
            
            <h2 className="promo-heading">{t("home_franchise_promo_heading")}</h2>
            <p className="promo-subheading">{t("home_franchise_promo_subheading")}</p>
            
            <a href="/Franchise" className="promo-cta-btn">
              {t("home_franchise_promo_button")}
            </a>
            
            <ul className="promo-features-list">
              <li>{t("home_franchise_promo_bullet1")}</li>
              <li>{t("home_franchise_promo_bullet2")}</li>
              <li>{t("home_franchise_promo_bullet3")}</li>
            </ul>
          </div>

          <div className="franchise-promo-right">
            <img src={franchiseCard} alt="Franchise Earning Potential" className="promo-earning-bubble" />
          </div>

        </div>
      </section>

      {/* WhatsApp + Climate */}
      <WhatsAppChatWidget />
      <Climate />




<section className="services" id="solutions">

  <div className="solutions-layout">
    <div className="service-grid">

      <div className="service-item tall">
        <img src={inputs} alt="Inputs" className="service-img" />
        <div className="service-text-block">
          <h3>{t("home_offering_inputs_title")}</h3>
          <p>{t("home_offering_inputs_desc")}</p>
        </div>
      </div>

      <div className="service-item">
        <img src={orders} alt="Orders" className="service-img" />
        <div className="service-text-block">
          <h3>{t("home_offering_ordering_title")}</h3>
          <p>{t("home_offering_ordering_desc")}</p>
        </div>
      </div>

      <div className="service-item tall">
        <img src={consultancy} alt="Consultancy" className="service-img" />
        <div className="service-text-block">
          <h3>{t("home_offering_consultancy_title")}</h3>
          <p>{t("home_offering_consultancy_desc")}</p>
        </div>
      </div>

      <div className="service-item">
        <img src={supplychain} alt="Supply Chain" className="service-img" />
        <div className="service-text-block">
          <h3>{t("home_offering_supply_title")}</h3>
          <p>{t("home_offering_supply_desc")}</p>
        </div>
      </div>

    </div>
  </div>

</section>

      {/* ================= PARTNERS LOGOS ================= */}
      <section className="partners-logos" id="partners">
        <h2 className="partners-title">{t("partner_network_heading")}</h2>
        <p className="partners-subtitle">{t("partner_network_subtitle")}</p>
        <div className="partners-slider">
          <div className="partners-track">
            {logos.map((logo, idx) => (
              <a
                key={idx}
                href={partnerLinks[idx]}
                target="_blank"
                rel="noopener noreferrer"
                className="partner-logo"
                aria-label={`Partner link ${idx + 1}`}
              >
                <img src={logo} alt={`logo-${idx}`} />
              </a>
            ))}
            {/* duplicate for infinite scroll */}
            {logos.map((logo, idx) => (
              <a
                key={`dup-${idx}`}
                href={partnerLinks[idx]}
                target="_blank"
                rel="noopener noreferrer"
                className="partner-logo"
                aria-label={`Partner link duplicate ${idx + 1}`}
              >
                <img src={logo} alt={`logo-dup-${idx}`} />
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* ================= IMPACT COUNTERS ================= */}
      <section className="impact-section">
        <div className="impact-container">
          <h2 className="impact-title">Driving Agricultural Transformation</h2>
          <p className="impact-subtitle">Our growing measurable contribution to the global agri-ecosystem</p>

          <div className="impact-grid">
            <div className="impact-card">
              <div className="impact-icon-wrapper">
                <FaStore className="impact-icon" />
              </div>
              <div className="impact-numbers"><CountUp target={4} /></div>
              <div className="impact-label">Franchises</div>
            </div>

            <div className="impact-card">
              <div className="impact-icon-wrapper">
                <FaUsers className="impact-icon" />
              </div>
              <div className="impact-numbers"><CountUp target={4500} /></div>
              <div className="impact-label">FPO/Farmers</div>
            </div>

            <div className="impact-card">
              <div className="impact-icon-wrapper">
                <FaMapMarkedAlt className="impact-icon" />
              </div>
              <div className="impact-numbers"><CountUp target={15000} /></div>
              <div className="impact-label">Acres</div>
            </div>
            
            <div className="impact-card">
              <div className="impact-icon-wrapper">
                <FaBoxOpen className="impact-icon" />
              </div>
              <div className="impact-numbers"><CountUp target={400} /></div>
              <div className="impact-label">Products</div>
            </div>

            <div className="impact-card">
              <div className="impact-icon-wrapper">
                <FaTruck className="impact-icon" />
              </div>
              <div className="impact-numbers"><CountUp target={20} /></div>
              <div className="impact-label">Supplier</div>
            </div>

            <div className="impact-card">
              <div className="impact-icon-wrapper">
                <FaSeedling className="impact-icon" />
              </div>
              <div className="impact-numbers"><CountUp target={20} /></div>
              <div className="impact-label">Crops</div>
            </div>
          </div>
        </div>
      </section>

      {/* ================= CONTACT SECTION ================= */}
      <section className="contact-section-two-column">
        {/* LEFT GREEN CUBOID */}
        <div className="contact-cuboid">
          <h2>{t("contact_main_heading")}</h2>
          <h3>{t("contact_contact_us_heading")}</h3>
          <p><strong>{t("contact_label_email")}:</strong>info@agrifabrix.com</p>
          <p><strong>{t("contact_label_phone")}:</strong> +91-7075483505</p>
          <p className="timing">
            {t("contact_support_hours")}
          </p>
        </div>

        {/* RIGHT WHITE FORM */}
        <div className="contact-form-box" id="contact-form">
          <h2>{t("contact_form_heading")}</h2>
          <form onSubmit={handleSubmit}>
            <label>{t("contact_label_first_name")}</label>
            <input
              type="text"
              name="firstName"
              placeholder={t("contact_placeholder_first_name")}
              required
              value={formData.firstName}
              onChange={handleChange}
            />
            <label>{t("contact_label_surname")}</label>
            <input
              type="text"
              name="surname"
              placeholder={t("contact_placeholder_surname")}
              required
              value={formData.surname}
              onChange={handleChange}
            />
            <label>{t("contact_label_email")}</label>
            <input
              type="email"
              name="email"
              placeholder={t("contact_placeholder_email")}
              required
              value={formData.email}
              onChange={handleChange}
            />
            <label>{t("contact_label_phone")}</label>
            <input
              type="tel"
              name="phone"
              placeholder={t("contact_placeholder_phone")}
              required
              value={formData.phone}
              onChange={handleChange}
            />

            <div className="custom-dropdown">
              <div
                className="dropdown-header input-like"
                onClick={() => setShowContactInterests(!showContactInterests)}
              >
                {formData.interests.length > 0
                  ? `${formData.interests.length} selected`
                  : "Area of Interest"}
                <span className={`dropdown-arrow ${showContactInterests ? 'open' : ''}`}>▼</span>
              </div>
              {showContactInterests && (
                <div className="checkbox-group dropdown-body">
                  {[
                    "InputFabriX",
                    "CreditFabriX",
                    "TraceFabriX",
                    "SupplyFabriX",
                    "TradeFabriX",
                    "Franchise",
                    "Careers",
                  ].map((option) => (
                    <label key={option}>
                      <input
                        type="checkbox"
                        value={option}
                        checked={formData.interests.includes(option)}
                        onChange={handleCheckboxChange}
                      />{" "}
                      {option}
                    </label>
                  ))}
                </div>
              )}
            </div>

            <label>{t("contact_label_message")}</label>
            <textarea
              name="message"
              placeholder={t("contact_placeholder_message")}
              required
              value={formData.message}
              onChange={handleChange}
            ></textarea>

            <button type="submit">{t("contact_button_submit")}</button>
          </form>
        </div>
      </section>

      <section
        className="contact-details-container"
        onClick={() =>
          window.open(
            "https://maps.app.goo.gl/jn5ZAvv5Y22GucTE6"
          )
        }
      >
        <div className="contact-bg-overlay">
          <h2 className="contact-heading">{t("contact_details_heading")}</h2>
          <p className="contact-address">
            {t("footer_address")}
          </p>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
