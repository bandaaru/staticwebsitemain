import { LangProvider } from './components/LangContext';
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import HomePage from "./components/HomePage";
// import Contact from "./components/Contact";
import Solutions from "./components/Solutions";
import Technology from "./components/Technology";
import CancellationPolicy from './components/CancellationPolicy';
import TermsAndConditions from './components/TermsAndConditions';
import ShippingPolicy from './components/ShippingPolicy';
import PrivacyPolicy from './components/PrivacyPolicy';
import Partners from "./components/Partners";
import Sustainability from "./components/Sustainability";
import CreditFabriX from "./components/CreditFabriX";
import About from "./components/About";
import Footer from "./components/Footer";
import SupplyFabriX from "./components/SupplyFabriX";
import TraceFabriX from "./components/TraceFabriX";
import InputFabriX from "./components/InputFabriX";
import TradeFabriX from "./components/TradeFabriX";
import OnboardingForm from "./components/OnboardingForm"; // ✅ Import OnboardingForm
import ScrollToTop from "./components/ScrollToTop"; // ✅ Import ScrollToTop component
import Climate from "./components/Climate";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import AnnouncementBar from "./components/AnnouncementBar";
import Franchise from "./components/Franchise";
import Gallery from "./components/Gallery";
import Apply from "./components/Apply";




// CSS imports
import "./styles/HomePage.css";
import "./styles/Navbar.css";
import "./styles/Solutions.css";
// import "./styles/Contact.css";
import "./styles/Technology.css";
import "./styles/Partner.css";
import "./styles/Sustainable.css";
import "./styles/Financial.css";
import "./styles/Footer.css";
import "./styles/SupplyFabriX.css";
import "./styles/InputFabriX.css";
import "./styles/TradeFabriX.css";
import "./styles/TraceFabriX.css";
import "./styles/onboarding.css";
import "./styles/Gallery.css";


function App() {
  return (
    <LangProvider>

      <Router>
        <ScrollToTop /> {/* ✅ Add scroll-to-top component here */}
        <AnnouncementBar />
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          {/* <Route path="/Contact" element={<Contact />} /> */}
          <Route path="/Solutions" element={<Solutions />} />
          <Route path="/Technology" element={<Technology />} />
          <Route path="/CancellationPolicy" element={<CancellationPolicy />} />
          <Route path="/TermsAndConditions" element={<TermsAndConditions />} />
          <Route path="/ShippingPolicy" element={<ShippingPolicy />} />
          <Route path="/PrivacyPolicy" element={<PrivacyPolicy />} />
          <Route path="/Sustainability" element={<Sustainability />} />
          <Route path="/CreditFabriX" element={<CreditFabriX />} />
          <Route path="/TraceFabriX" element={<TraceFabriX />} />
          <Route path="/TradeFabriX" element={<TradeFabriX />} />
          <Route path="/InputFabriX" element={<InputFabriX />} />
          <Route path="/SupplyFabriX" element={<SupplyFabriX />} />
          <Route path="/Partners" element={<Partners />} />
          <Route path="/About" element={<About />} />
          <Route path="/Climate" element={<Climate />} />
          <Route path="/OnboardingForm" element={<OnboardingForm />} />
          <Route path="/franchise" element={<Franchise />} />
          <Route path="/gallery" element={<Gallery />} />
          <Route path="/Careers" element={<Apply />} />

        </Routes>
        <Footer />
      </Router>
    </LangProvider>
  );
}

export default App;
