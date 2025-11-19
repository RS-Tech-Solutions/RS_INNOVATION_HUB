import React from 'react';
import Header from '../components/Header';
import HeroSection from '../components/HeroSection';
import ProgramsSection from '../components/ProgramsSection';
import SuccessStoriesSection from '../components/SuccessStoriesSection';
import EventsSection from '../components/EventsSection';
import TestimonialsSection from '../components/TestimonialsSection';
import ContactSection from '../components/ContactSection';
import Footer from '../components/Footer';

const HomePage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <Header />
      <main>
        <HeroSection />
        <ProgramsSection />
        <SuccessStoriesSection />
        <EventsSection />
        <TestimonialsSection />
        <ContactSection />
      </main>
      <Footer />
    </div>
  );
};

export default HomePage;