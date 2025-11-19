import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from './ui/dialog';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Calendar, MapPin, Users, Gift, Clock, Trophy } from 'lucide-react';
import { mockData, mockSubmissions } from '../mock';
import { toast } from 'sonner';

const EventsSection = () => {
  const { events } = mockData;
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [registrationData, setRegistrationData] = useState({
    name: '',
    email: '',
    phone: '',
    organization: ''
  });

  const handleRegister = (event) => {
    setSelectedEvent(event);
    setIsDialogOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      const result = await mockSubmissions.registerEvent(selectedEvent.id, registrationData);
      
      if (result.success) {
        toast.success(result.message);
        setIsDialogOpen(false);
        setRegistrationData({ name: '', email: '', phone: '', organization: '' });
      }
    } catch (error) {
      toast.error('Registration failed. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleInputChange = (field, value) => {
    setRegistrationData(prev => ({ ...prev, [field]: value }));
  };

  const getEventTypeColor = (type) => {
    const colors = {
      'Hackathon': 'bg-red-100 text-red-700 border-red-200',
      'Demo Day': 'bg-blue-100 text-blue-700 border-blue-200',
      'Workshop': 'bg-green-100 text-green-700 border-green-200'
    };
    return colors[type] || 'bg-gray-100 text-gray-700 border-gray-200';
  };

  const getStatusColor = (status) => {
    return status === 'upcoming' 
      ? 'bg-orange-100 text-orange-700' 
      : 'bg-green-100 text-green-700';
  };

  return (
    <section id="events" className="py-20 bg-white">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <Badge className="mb-4 bg-purple-100 text-purple-700 hover:bg-purple-200">
            Events & Hackathons
          </Badge>
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Participate in <span className="text-purple-600">Innovation Challenges</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Join our exciting events, hackathons, and workshops to network with like-minded innovators, showcase your skills, and win amazing prizes.
          </p>
        </div>

        {/* Events Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
          {events.map((event) => (
            <Card key={event.id} className="group hover:shadow-2xl transition-all duration-500 hover:scale-105 border-0 shadow-lg overflow-hidden">
              <div className="h-48 bg-gradient-to-br from-purple-50 to-blue-50 relative">
                <img 
                  src="https://images.pexels.com/photos/933964/pexels-photo-933964.jpeg"
                  alt={event.title}
                  className="w-full h-full object-cover opacity-90"
                />
                <div className="absolute inset-0 bg-gradient-to-br from-purple-600/20 to-blue-600/20"></div>
                <div className="absolute top-4 right-4">
                  <Badge className={getStatusColor(event.status)}>
                    {event.status === 'upcoming' ? 'Upcoming' : 'Completed'}
                  </Badge>
                </div>
                <div className="absolute bottom-4 left-4">
                  <Badge className={getEventTypeColor(event.type)} variant="outline">
                    {event.type}
                  </Badge>
                </div>
              </div>
              
              <CardHeader>
                <CardTitle className="text-xl font-bold text-gray-900 group-hover:text-purple-600 transition-colors">
                  {event.title}
                </CardTitle>
                <CardDescription className="text-gray-600">
                  {event.description}
                </CardDescription>
              </CardHeader>
              
              <CardContent>
                <div className="space-y-3 mb-6">
                  <div className="flex items-center text-sm text-gray-600">
                    <Calendar className="w-4 h-4 mr-2 text-purple-600" />
                    {event.date}
                  </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <Users className="w-4 h-4 mr-2 text-purple-600" />
                    {event.participants}
                  </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <Trophy className="w-4 h-4 mr-2 text-purple-600" />
                    {event.prizes}
                  </div>
                </div>
                
                {event.status === 'upcoming' ? (
                  <Button 
                    onClick={() => handleRegister(event)}
                    className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white group-hover:scale-105 transition-all duration-300"
                  >
                    Register Now
                  </Button>
                ) : (
                  <Button variant="outline" className="w-full" disabled>
                    Event Completed
                  </Button>
                )}
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Upcoming Events Highlight */}
        <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl p-8 text-white text-center">
          <h3 className="text-2xl font-bold mb-4">
            Don't Miss Our Biggest Event of the Year!
          </h3>
          <p className="text-purple-100 mb-6 max-w-2xl mx-auto">
            HaryanaHack 2024 is coming soon with ₹5 Lakhs in prizes. Register now to secure your spot in Haryana's largest hackathon.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              size="lg"
              className="bg-white text-purple-600 hover:bg-gray-100 hover:scale-105 transition-all duration-300"
              onClick={() => handleRegister(events.find(e => e.title === 'HaryanaHack 2024'))}
            >
              <Calendar className="w-5 h-5 mr-2" />
              Register for HaryanaHack
            </Button>
            <Button 
              size="lg"
              variant="outline"
              className="border-white text-white hover:bg-white hover:text-purple-600 hover:scale-105 transition-all duration-300"
            >
              View All Events
            </Button>
          </div>
        </div>

        {/* Registration Dialog */}
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle className="text-xl font-bold">
                Register for {selectedEvent?.title}
              </DialogTitle>
              <DialogDescription>
                Fill in your details to register for this event. Registration is free!
              </DialogDescription>
            </DialogHeader>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="reg-name">Full Name *</Label>
                  <Input 
                    id="reg-name"
                    value={registrationData.name}
                    onChange={(e) => handleInputChange('name', e.target.value)}
                    required 
                    className="mt-1"
                  />
                </div>
                <div>
                  <Label htmlFor="reg-phone">Phone Number *</Label>
                  <Input 
                    id="reg-phone"
                    type="tel"
                    value={registrationData.phone}
                    onChange={(e) => handleInputChange('phone', e.target.value)}
                    required 
                    className="mt-1"
                  />
                </div>
              </div>
              
              <div>
                <Label htmlFor="reg-email">Email Address *</Label>
                <Input 
                  id="reg-email"
                  type="email"
                  value={registrationData.email}
                  onChange={(e) => handleInputChange('email', e.target.value)}
                  required 
                  className="mt-1"
                />
              </div>
              
              <div>
                <Label htmlFor="reg-organization">Organization/College</Label>
                <Input 
                  id="reg-organization"
                  value={registrationData.organization}
                  onChange={(e) => handleInputChange('organization', e.target.value)}
                  className="mt-1"
                  placeholder="Your current organization or college"
                />
              </div>
              
              <div className="flex gap-3 pt-4">
                <Button type="button" variant="outline" onClick={() => setIsDialogOpen(false)} className="flex-1">
                  Cancel
                </Button>
                <Button type="submit" disabled={isSubmitting} className="flex-1 bg-purple-600 hover:bg-purple-700">
                  {isSubmitting ? 'Registering...' : 'Complete Registration'}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>
    </section>
  );
};

export default EventsSection;