// Mock data for RS Innovation Hub
export const mockData = {
  hero: {
    title: "RS INNOVATION HUB",
    subtitle: "Second Incubation Center in Haryana",
    description: "Empowering the next generation through comprehensive ecosystem of employment, startup incubation, courses, internships, events, and hackathons.",
    stats: [
      { number: "500+", label: "Students Trained" },
      { number: "50+", label: "Startups Incubated" },
      { number: "100+", label: "Job Placements" },
      { number: "25+", label: "Events Conducted" }
    ]
  },
  programs: [
    {
      id: 1,
      title: "Startup Incubation",
      description: "Complete support for your startup journey from ideation to market launch",
      features: ["Mentorship", "Funding Support", "Co-working Space", "Legal Assistance"],
      duration: "6-12 months",
      category: "incubation"
    },
    {
      id: 2,
      title: "Technology Courses",
      description: "Industry-relevant courses in emerging technologies",
      features: ["Web Development", "Data Science", "AI/ML", "Mobile App Development"],
      duration: "3-6 months",
      category: "courses"
    },
    {
      id: 3,
      title: "Internship Programs",
      description: "Hands-on experience with industry partners",
      features: ["Live Projects", "Industry Mentors", "Certification", "Job Assistance"],
      duration: "2-4 months",
      category: "internship"
    },
    {
      id: 4,
      title: "Employment Training",
      description: "Skill development programs for immediate employability",
      features: ["Interview Prep", "Soft Skills", "Technical Skills", "Resume Building"],
      duration: "1-3 months",
      category: "employment"
    }
  ],
  successStories: [
    {
      id: 1,
      name: "Priya Sharma",
      company: "TechStart Solutions",
      story: "From a course participant to founding a successful fintech startup with 50+ employees",
      achievement: "₹2Cr+ Revenue",
      image: "https://images.unsplash.com/photo-1557804506-669a67965ba0?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODF8MHwxfHNlYXJjaHwyfHxzdGFydHVwfGVufDB8fHx8MTc1OTI0NDA4OXww&ixlib=rb-4.1.0&q=85"
    },
    {
      id: 2,
      name: "Rahul Gupta",
      company: "Google India",
      story: "Completed web development course and internship, now working as Senior Software Engineer",
      achievement: "₹25LPA Package",
      image: "https://images.unsplash.com/photo-1559136555-9303baea8ebd?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODF8MHwxfHNlYXJjaHwzfHxzdGFydHVwfGVufDB8fHx8MTc1OTI0NDA4OXww&ixlib=rb-4.1.0&q=85"
    },
    {
      id: 3,
      name: "Anjali Verma",
      company: "DataMind Analytics",
      story: "Transformed from housewife to data scientist through our AI/ML program",
      achievement: "Founded AI Startup",
      image: "https://images.unsplash.com/photo-1522071820081-009f0129c71c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODF8MHwxfHNlYXJjaHw0fHxzdGFydHVwfGVufDB8fHx8MTc1OTI0NDA4OXww&ixlib=rb-4.1.0&q=85"
    }
  ],
  events: [
    {
      id: 1,
      title: "HaryanaHack 2024",
      date: "March 15-17, 2024",
      type: "Hackathon",
      description: "48-hour hackathon focusing on solutions for rural development",
      participants: "200+",
      prizes: "₹5 Lakhs",
      status: "upcoming"
    },
    {
      id: 2,
      title: "Startup Showcase",
      date: "February 28, 2024",
      type: "Demo Day",
      description: "Our incubated startups presenting to investors and industry leaders",
      participants: "25 Startups",
      prizes: "Funding Opportunities",
      status: "upcoming"
    },
    {
      id: 3,
      title: "Tech Talk: AI in Agriculture",
      date: "February 10, 2024",
      type: "Workshop",
      description: "Expert session on implementing AI solutions in agricultural sector",
      participants: "100+",
      prizes: "Certificates",
      status: "completed"
    }
  ],
  testimonials: [
    {
      id: 1,
      name: "Dr. Anil Kumar",
      position: "Director, Haryana State Innovation Council",
      content: "RS Innovation Hub is setting new benchmarks in startup ecosystem development in Haryana.",
      rating: 5
    },
    {
      id: 2,
      name: "Ravi Patel",
      position: "Alumnus, Currently at Microsoft",
      content: "The comprehensive training and mentorship I received here transformed my career trajectory completely.",
      rating: 5
    },
    {
      id: 3,
      name: "Sneha Agarwal",
      position: "Founder, EcoTech Solutions",
      content: "From ideation to execution, RS Innovation Hub provided end-to-end support for my startup journey.",
      rating: 5
    }
  ]
};

// Mock form submission functions
export const mockSubmissions = {
  submitApplication: async (formData, type) => {
    console.log(`Submitting ${type} application:`, formData);
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    return { success: true, message: `Your ${type} application has been submitted successfully!` };
  },
  
  submitContact: async (formData) => {
    console.log('Submitting contact form:', formData);
    await new Promise(resolve => setTimeout(resolve, 800));
    return { success: true, message: 'Thank you for reaching out! We\'ll get back to you soon.' };
  },
  
  registerEvent: async (eventId, formData) => {
    console.log(`Registering for event ${eventId}:`, formData);
    await new Promise(resolve => setTimeout(resolve, 1200));
    return { success: true, message: 'Successfully registered for the event!' };
  }
};