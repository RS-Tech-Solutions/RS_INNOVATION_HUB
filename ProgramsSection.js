import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Clock, Users, ArrowRight, GraduationCap, Briefcase, Rocket, Code } from 'lucide-react';
import { mockData, mockSubmissions } from '../mock';
import { toast } from 'sonner';

const ProgramsSection = () => {
  const { programs } = mockData;
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selectedProgram, setSelectedProgram] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    experience: '',
    motivation: ''
  });

  const categoryIcons = {
    incubation: Rocket,
    courses: Code,
    internship: Users,
    employment: Briefcase
  };

  const filteredPrograms = selectedCategory === 'all' 
    ? programs 
    : programs.filter(program => program.category === selectedCategory);

  const handleApply = (program) => {
    setSelectedProgram(program);
    setIsDialogOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      const result = await mockSubmissions.submitApplication({
        ...formData,
        program: selectedProgram.title
      }, selectedProgram.category);
      
      if (result.success) {
        toast.success(result.message);
        setIsDialogOpen(false);
        setFormData({ name: '', email: '', phone: '', experience: '', motivation: '' });
      }
    } catch (error) {
      toast.error('Something went wrong. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <section id="programs" className="py-20 bg-white">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <Badge className="mb-4 bg-blue-100 text-blue-700 hover:bg-blue-200">
            Our Programs
          </Badge>
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Comprehensive <span className="text-blue-600">Learning Ecosystem</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            From startup incubation to skill development, we offer diverse programs designed to accelerate your career and entrepreneurial journey.
          </p>
        </div>

        {/* Category Filter */}
        <div className="flex flex-wrap justify-center gap-3 mb-12">
          <Button 
            variant={selectedCategory === 'all' ? 'default' : 'outline'}
            onClick={() => setSelectedCategory('all')}
            className="transition-all duration-300 hover:scale-105"
          >
            All Programs
          </Button>
          <Button 
            variant={selectedCategory === 'incubation' ? 'default' : 'outline'}
            onClick={() => setSelectedCategory('incubation')}
            className="transition-all duration-300 hover:scale-105"
          >
            <Rocket className="w-4 h-4 mr-2" />
            Incubation
          </Button>
          <Button 
            variant={selectedCategory === 'courses' ? 'default' : 'outline'}
            onClick={() => setSelectedCategory('courses')}
            className="transition-all duration-300 hover:scale-105"
          >
            <Code className="w-4 h-4 mr-2" />
            Courses
          </Button>
          <Button 
            variant={selectedCategory === 'internship' ? 'default' : 'outline'}
            onClick={() => setSelectedCategory('internship')}
            className="transition-all duration-300 hover:scale-105"
          >
            <Users className="w-4 h-4 mr-2" />
            Internships
          </Button>
          <Button 
            variant={selectedCategory === 'employment' ? 'default' : 'outline'}
            onClick={() => setSelectedCategory('employment')}
            className="transition-all duration-300 hover:scale-105"
          >
            <Briefcase className="w-4 h-4 mr-2" />
            Employment
          </Button>
        </div>

        {/* Programs Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-2 gap-8">
          {filteredPrograms.map((program) => {
            const Icon = categoryIcons[program.category];
            return (
              <Card key={program.id} className="group hover:shadow-2xl transition-all duration-500 hover:scale-105 border-0 shadow-lg overflow-hidden">
                <div className="h-48 bg-gradient-to-br from-blue-50 to-purple-50 relative">
                  <img 
                    src="https://images.unsplash.com/photo-1733925457822-64c3e048fa1b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDF8MHwxfHNlYXJjaHw0fHxpbm5vdmF0aW9uJTIwaHVifGVufDB8fHx8MTc1OTI0NDA4M3ww&ixlib=rb-4.1.0&q=85"
                    alt={program.title}
                    className="w-full h-full object-cover opacity-80"
                  />
                  <div className="absolute inset-0 bg-gradient-to-br from-blue-600/20 to-purple-600/20"></div>
                  <div className="absolute top-4 left-4">
                    <div className="w-12 h-12 bg-white/90 rounded-lg flex items-center justify-center">
                      <Icon className="w-6 h-6 text-blue-600" />
                    </div>
                  </div>
                </div>
                
                <CardHeader>
                  <div className="flex items-center justify-between mb-2">
                    <CardTitle className="text-xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors">
                      {program.title}
                    </CardTitle>
                    <Badge variant="secondary" className="bg-blue-100 text-blue-700">
                      <Clock className="w-3 h-3 mr-1" />
                      {program.duration}
                    </Badge>
                  </div>
                  <CardDescription className="text-gray-600 text-base">
                    {program.description}
                  </CardDescription>
                </CardHeader>
                
                <CardContent>
                  <div className="mb-6">
                    <h4 className="font-semibold text-gray-900 mb-3">Key Features:</h4>
                    <div className="flex flex-wrap gap-2">
                      {program.features.map((feature, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {feature}
                        </Badge>
                      ))}
                    </div>
                  </div>
                  
                  <Button 
                    onClick={() => handleApply(program)}
                    className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white group-hover:scale-105 transition-all duration-300"
                  >
                    Apply Now
                    <ArrowRight className="ml-2 w-4 h-4" />
                  </Button>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Application Dialog */}
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle className="text-xl font-bold">
                Apply for {selectedProgram?.title}
              </DialogTitle>
              <DialogDescription>
                Fill in your details to apply for this program. We'll get back to you within 24 hours.
              </DialogDescription>
            </DialogHeader>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="name">Full Name *</Label>
                  <Input 
                    id="name"
                    value={formData.name}
                    onChange={(e) => handleInputChange('name', e.target.value)}
                    required 
                    className="mt-1"
                  />
                </div>
                <div>
                  <Label htmlFor="phone">Phone Number *</Label>
                  <Input 
                    id="phone"
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => handleInputChange('phone', e.target.value)}
                    required 
                    className="mt-1"
                  />
                </div>
              </div>
              
              <div>
                <Label htmlFor="email">Email Address *</Label>
                <Input 
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => handleInputChange('email', e.target.value)}
                  required 
                  className="mt-1"
                />
              </div>
              
              <div>
                <Label htmlFor="experience">Experience Level *</Label>
                <Select value={formData.experience} onValueChange={(value) => handleInputChange('experience', value)} required>
                  <SelectTrigger className="mt-1">
                    <SelectValue placeholder="Select your experience level" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="beginner">Beginner (0-1 years)</SelectItem>
                    <SelectItem value="intermediate">Intermediate (1-3 years)</SelectItem>
                    <SelectItem value="experienced">Experienced (3+ years)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div>
                <Label htmlFor="motivation">Why do you want to join this program? *</Label>
                <Textarea 
                  id="motivation"
                  value={formData.motivation}
                  onChange={(e) => handleInputChange('motivation', e.target.value)}
                  required 
                  className="mt-1 min-h-20"
                  placeholder="Tell us about your goals and motivation..."
                />
              </div>
              
              <div className="flex gap-3 pt-4">
                <Button type="button" variant="outline" onClick={() => setIsDialogOpen(false)} className="flex-1">
                  Cancel
                </Button>
                <Button type="submit" disabled={isSubmitting} className="flex-1 bg-blue-600 hover:bg-blue-700">
                  {isSubmitting ? 'Submitting...' : 'Submit Application'}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>
    </section>
  );
};

export default ProgramsSection;