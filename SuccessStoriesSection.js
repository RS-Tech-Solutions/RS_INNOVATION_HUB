import React from 'react';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { Building2, TrendingUp, Users, ArrowUpRight } from 'lucide-react';
import { mockData } from '../mock';

const SuccessStoriesSection = () => {
  const { successStories } = mockData;

  return (
    <section id="success" className="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <Badge className="mb-4 bg-green-100 text-green-700 hover:bg-green-200">
            Success Stories
          </Badge>
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Transforming <span className="text-green-600">Lives & Careers</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Meet our alumni who have successfully transitioned their careers, built successful startups, and achieved their dreams through our programs.
          </p>
        </div>

        {/* Success Stories Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
          {successStories.map((story) => (
            <Card key={story.id} className="group hover:shadow-2xl transition-all duration-500 hover:scale-105 border-0 shadow-lg overflow-hidden">
              <div className="h-48 relative">
                <img 
                  src={story.image}
                  alt={story.name}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
                <div className="absolute bottom-4 left-4 right-4">
                  <div className="flex items-center space-x-3">
                    <Avatar className="w-12 h-12 border-2 border-white">
                      <AvatarImage src={story.image} alt={story.name} />
                      <AvatarFallback className="bg-blue-600 text-white font-semibold">
                        {story.name.split(' ').map(n => n[0]).join('')}
                      </AvatarFallback>
                    </Avatar>
                    <div>
                      <h3 className="font-bold text-white">{story.name}</h3>
                      <p className="text-gray-200 text-sm flex items-center">
                        <Building2 className="w-3 h-3 mr-1" />
                        {story.company}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              
              <CardContent className="p-6">
                <div className="mb-4">
                  <Badge className="bg-green-100 text-green-700 mb-3">
                    <TrendingUp className="w-3 h-3 mr-1" />
                    {story.achievement}
                  </Badge>
                  <p className="text-gray-700 leading-relaxed">
                    {story.story}
                  </p>
                </div>
                
                <Button 
                  variant="ghost" 
                  className="w-full justify-between text-blue-600 hover:bg-blue-50 group/btn"
                >
                  Read Full Story
                  <ArrowUpRight className="w-4 h-4 group-hover/btn:translate-x-1 group-hover/btn:-translate-y-1 transition-transform" />
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Call to Action */}
        <div className="text-center bg-white rounded-2xl p-8 shadow-lg border">
          <div className="max-w-2xl mx-auto">
            <h3 className="text-2xl font-bold text-gray-900 mb-4">
              Ready to Write Your Success Story?
            </h3>
            <p className="text-gray-600 mb-6">
              Join thousands of professionals who have transformed their careers through our comprehensive programs. Your success story could be next!
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                size="lg"
                className="bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 text-white hover:scale-105 transition-all duration-300"
                onClick={() => document.querySelector('#programs')?.scrollIntoView({ behavior: 'smooth' })}
              >
                <Users className="w-5 h-5 mr-2" />
                View Programs
              </Button>
              <Button 
                size="lg"
                variant="outline"
                className="border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white hover:scale-105 transition-all duration-300"
                onClick={() => document.querySelector('#contact')?.scrollIntoView({ behavior: 'smooth' })}
              >
                Get Started Today
              </Button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default SuccessStoriesSection;