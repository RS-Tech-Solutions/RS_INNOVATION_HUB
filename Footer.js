import React from 'react';
import { Button } from './ui/button';
import { Separator } from './ui/separator';
import { Rocket, Mail, Phone, MapPin, Facebook, Twitter, Linkedin, Instagram, Youtube } from 'lucide-react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  const footerLinks = {
    programs: [
      { label: 'Startup Incubation', href: '#programs' },
      { label: 'Technology Courses', href: '#programs' },
      { label: 'Internship Programs', href: '#programs' },
      { label: 'Employment Training', href: '#programs' }
    ],
    company: [
      { label: 'About Us', href: '#about' },
      { label: 'Success Stories', href: '#success' },
      { label: 'Events', href: '#events' },
      { label: 'Contact Us', href: '#contact' }
    ],
    resources: [
      { label: 'Blog', href: '#blog' },
      { label: 'Resources', href: '#resources' },
      { label: 'Career Support', href: '#career' },
      { label: 'Alumni Network', href: '#alumni' }
    ]
  };

  const socialLinks = [
    { icon: Facebook, href: '#', label: 'Facebook' },
    { icon: Twitter, href: '#', label: 'Twitter' },
    { icon: Linkedin, href: '#', label: 'LinkedIn' },
    { icon: Instagram, href: '#', label: 'Instagram' },
    { icon: Youtube, href: '#', label: 'YouTube' }
  ];

  const scrollToSection = (href) => {
    if (href.startsWith('#')) {
      const element = document.querySelector(href);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  return (
    <footer className=\"bg-gray-900 text-white\">
      <div className=\"container mx-auto px-4 sm:px-6 lg:px-8 py-12\">
        {/* Main Footer Content */}
        <div className=\"grid md:grid-cols-2 lg:grid-cols-5 gap-8 mb-8\">
          {/* Brand Section */}
          <div className=\"lg:col-span-2\">
            <div className=\"flex items-center space-x-2 mb-4\">
              <div className=\"w-10 h-10 bg-gradient-to-tr from-blue-500 to-purple-500 rounded-lg flex items-center justify-center\">
                <Rocket className=\"w-6 h-6 text-white\" />
              </div>
              <div className=\"flex flex-col\">
                <span className=\"text-xl font-bold text-white\">RS Innovation</span>
                <span className=\"text-xs text-gray-400 -mt-1\">HUB</span>
              </div>
            </div>
            
            <p className=\"text-gray-300 mb-6 leading-relaxed\">
              Empowering the next generation through comprehensive ecosystem of employment, startup incubation, courses, internships, events, and hackathons. Building Haryana's innovation future.
            </p>
            
            <div className=\"space-y-3\">
              <div className=\"flex items-center space-x-3\">
                <MapPin className=\"w-5 h-5 text-blue-400\" />
                <span className=\"text-gray-300\">Sector 14, Gurugram, Haryana 122001</span>
              </div>
              <div className=\"flex items-center space-x-3\">
                <Phone className=\"w-5 h-5 text-blue-400\" />
                <span className=\"text-gray-300\">+91 98765 43210</span>
              </div>
              <div className=\"flex items-center space-x-3\">
                <Mail className=\"w-5 h-5 text-blue-400\" />
                <span className=\"text-gray-300\">info@rsinnovationhub.com</span>
              </div>
            </div>
          </div>

          {/* Programs */}
          <div>
            <h3 className=\"text-lg font-semibold text-white mb-4\">Programs</h3>
            <ul className=\"space-y-2\">
              {footerLinks.programs.map((link, index) => (
                <li key={index}>
                  <button
                    onClick={() => scrollToSection(link.href)}
                    className=\"text-gray-300 hover:text-blue-400 transition-colors duration-200 text-sm\"
                  >
                    {link.label}
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className=\"text-lg font-semibold text-white mb-4\">Company</h3>
            <ul className=\"space-y-2\">
              {footerLinks.company.map((link, index) => (
                <li key={index}>
                  <button
                    onClick={() => scrollToSection(link.href)}
                    className=\"text-gray-300 hover:text-blue-400 transition-colors duration-200 text-sm\"
                  >
                    {link.label}
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className=\"text-lg font-semibold text-white mb-4\">Resources</h3>
            <ul className=\"space-y-2\">
              {footerLinks.resources.map((link, index) => (
                <li key={index}>
                  <button
                    onClick={() => scrollToSection(link.href)}
                    className=\"text-gray-300 hover:text-blue-400 transition-colors duration-200 text-sm\"
                  >
                    {link.label}
                  </button>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Newsletter Section */}
        <div className=\"bg-gray-800 rounded-lg p-6 mb-8\">
          <div className=\"grid md:grid-cols-2 gap-6 items-center\">
            <div>
              <h3 className=\"text-xl font-bold text-white mb-2\">Stay Updated</h3>
              <p className=\"text-gray-300\">Get the latest updates on events, programs, and opportunities.</p>
            </div>
            <div className=\"flex gap-3\">
              <input
                type=\"email\"
                placeholder=\"Enter your email address\"
                className=\"flex-1 px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500\"
              />
              <Button className=\"bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 px-6\">
                Subscribe
              </Button>
            </div>
          </div>
        </div>

        <Separator className=\"bg-gray-700 mb-8\" />

        {/* Bottom Section */}
        <div className=\"flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0\">
          {/* Copyright */}
          <div className=\"text-gray-400 text-sm\">
            © {currentYear} RS Innovation Hub. All rights reserved. | Second Incubation Center in Haryana
          </div>

          {/* Social Links */}
          <div className=\"flex items-center space-x-4\">
            <span className=\"text-gray-400 text-sm\">Follow us:</span>
            {socialLinks.map((social, index) => {
              const Icon = social.icon;
              return (
                <a
                  key={index}
                  href={social.href}
                  aria-label={social.label}
                  className=\"w-8 h-8 bg-gray-800 rounded-full flex items-center justify-center hover:bg-blue-600 transition-colors duration-300 group\"
                >
                  <Icon className=\"w-4 h-4 text-gray-400 group-hover:text-white\" />
                </a>
              );
            })}
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;