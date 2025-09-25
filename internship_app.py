import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "/components/ui/card";
import { Button } from "/components/ui/button";
import { Input } from "/components/ui/input";
import { Label } from "/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

// Types
interface User {
  id: string;
  name: string;
  email: string;
  role: 'student' | 'placementCell' | 'facultyMentor' | 'employer';
  department?: string;
  skills?: string[];
  preferences?: {
    location: string;
    minStipend: number;
    maxStipend: number;
    placementConversion: boolean;
  };
}

interface Opportunity {
  id: string;
  title: string;
  company: string;
  description: string;
  requiredSkills: string[];
  department: string;
  stipend: number;
  duration: string;
  location: string;
  placementConversion: boolean;
  applicationDeadline: string;
  postedBy: string;
  createdAt: string;
}

interface Application {
  id: string;
  studentId: string;
  opportunityId: string;
  status: 'applied' | 'approved' | 'rejected' | 'interviewScheduled' | 'offerExtended' | 'completed';
  appliedDate: string;
  mentorApproval?: {
    status: 'pending' | 'approved' | 'rejected';
    comments: string;
    date: string;
  };
  interviewDate?: string;
  feedback?: {
    rating: number;
    comments: string;
    date: string;
  };
}

// Main Component
const CampusInternshipPlacementHub: React.FC = () => {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [applications, setApplications] = useState<Application[]>([]);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [newOpportunity, setNewOpportunity] = useState<Partial<Opportunity>>({
    title: '',
    company: '',
    description: '',
    requiredSkills: [],
    department: '',
    stipend: 0,
    duration: '',
    location: '',
    placementConversion: false,
    applicationDeadline: '',
  });
  const [skillInput, setSkillInput] = useState('');

  // Mock data - in a real app, this would come from an API
  useEffect(() => {
    // Simulate user login - in real app, this would be from authentication
    setCurrentUser({
      id: 'user-1',
      name: 'Rajesh Kumar',
      email: 'rajesh.kumar@example.com',
      role: 'student',
      department: 'Computer Science',
      skills: ['JavaScript', 'React', 'Node.js', 'Python'],
      preferences: {
        location: 'Ranchi',
        minStipend: 10000,
        maxStipend: 25000,
        placementConversion: true
      }
    });

    // Mock opportunities
    setOpportunities([
      {
        id: 'opp-1',
        title: 'Frontend Developer Intern',
        company: 'Tech Solutions Inc.',
        description: 'Work on cutting-edge web applications using React and TypeScript.',
        requiredSkills: ['JavaScript', 'React', 'HTML', 'CSS'],
        department: 'Computer Science',
        stipend: 15000,
        duration: '6 months',
        location: 'Ranchi',
        placementConversion: true,
        applicationDeadline: '2023-12-15',
        postedBy: 'placement-cell-1',
        createdAt: '2023-11-01'
      },
      {
        id: 'opp-2',
        title: 'Data Science Trainee',
        company: 'Data Analytics Group',
        description: 'Analyze large datasets and build predictive models using Python and ML libraries.',
        requiredSkills: ['Python', 'Machine Learning', 'SQL', 'Data Visualization'],
        department: 'Computer Science',
        stipend: 20000,
        duration: '8 months',
        location: 'Remote',
        placementConversion: true,
        applicationDeadline: '2023-12-20',
        postedBy: 'placement-cell-1',
        createdAt: '2023-11-05'
      }
    ]);

    // Mock applications
    setApplications([
      {
        id: 'app-1',
        studentId: 'user-1',
        opportunityId: 'opp-1',
        status: 'applied',
        appliedDate: '2023-11-10',
        mentorApproval: {
          status: 'pending',
          comments: '',
          date: ''
        }
      }
    ]);
  }, []);

  const handleAddSkill = () => {
    if (skillInput && currentUser) {
      const updatedSkills = [...(currentUser.skills || []), skillInput];
      setCurrentUser({
        ...currentUser,
        skills: updatedSkills
      });
      setSkillInput('');
    }
  };

  const handleRemoveSkill = (skill: string) => {
    if (currentUser) {
      const updatedSkills = currentUser.skills?.filter(s => s !== skill) || [];
      setCurrentUser({
        ...currentUser,
        skills: updatedSkills
      });
    }
  };

  const handlePostOpportunity = () => {
    if (newOpportunity.title && newOpportunity.company) {
      const opportunity: Opportunity = {
        id: opp-${Date.now()},
        title: newOpportunity.title || '',
        company: newOpportunity.company || '',
        description: newOpportunity.description || '',
        requiredSkills: newOpportunity.requiredSkills || [],
        department: newOpportunity.department || '',
        stipend: newOpportunity.stipend || 0,
        duration: newOpportunity.duration || '',
        location: newOpportunity.location || '',
        placementConversion: newOpportunity.placementConversion || false,
        applicationDeadline: newOpportunity.applicationDeadline || '',
        postedBy: currentUser?.id || '',
        createdAt: new Date().toISOString().split('T')[0]
      };

      setOpportunities([...opportunities, opportunity]);
      setNewOpportunity({
        title: '',
        company: '',
        description: '',
        requiredSkills: [],
        department: '',
        stipend: 0,
        duration: '',
        location: '',
        placementConversion: false,
        applicationDeadline: '',
      });
    }
  };

  const handleApply = (opportunityId: string) => {
    if (currentUser) {
      const newApplication: Application = {
        id: app-${Date.now()},
        studentId: currentUser.id,
        opportunityId,
        status: 'applied',
        appliedDate: new Date().toISOString().split('T')[0],
        mentorApproval: {
          status: 'pending',
          comments: '',
          date: ''
        }
      };

      setApplications([...applications, newApplication]);
    }
  };

  const getRecommendedOpportunities = () => {
    if (!currentUser || currentUser.role !== 'student') return [];

    return opportunities.filter(opp => {
      // Simple matching algorithm - in real app would be more sophisticated
      const userSkills = currentUser.skills || [];
      const matches = opp.requiredSkills.filter(skill => 
        userSkills.some(userSkill => 
          userSkill.toLowerCase().includes(skill.toLowerCase()) || 
          skill.toLowerCase().includes(userSkill.toLowerCase())
        )
      );

      // If at least 50% of required skills match
      return matches.length >= opp.requiredSkills.length * 0.5;
    });
  };

  const renderStudentDashboard = () => {
    const recommendedOpps = getRecommendedOpportunities();
    const userApplications = applications.filter(app => app.studentId === currentUser?.id);

    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Your Profile</CardTitle>
              <CardDescription>Manage your skills and preferences</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="skills">Your Skills</Label>
                <div className="flex flex-wrap gap-2 mt-2">
                  {currentUser?.skills?.map(skill => (
                    <span key={skill} className="bg-secondary text-secondary-foreground px-2 py-1 rounded-md text-sm flex items-center">
                      {skill}
                      <button 
                        onClick={() => handleRemoveSkill(skill)}
                        className="ml-2 text-muted-foreground hover:text-foreground"
                      >
                        &times;
                      </button>
                    </span>
                  ))}
                </div>
                <div className="flex mt-2">
                  <Input
                    id="skills"
                    value={skillInput}
                    onChange={(e) => setSkillInput(e.target.value)}
                    placeholder="Add a skill"
                    className="flex-1"
                  />
                  <Button onClick={handleAddSkill} className="ml-2">Add</Button>
                </div>
              </div>

              <div>
                <Label>Preferences</Label>
                <div className="text-sm text-muted-foreground mt-1">
                  Location: {currentUser?.preferences?.location}<br />
                  Stipend: ₹{currentUser?.preferences?.minStipend} - ₹{currentUser?.preferences?.maxStipend}<br />
                  Prefers placement conversion: {currentUser?.preferences?.placementConversion ? 'Yes' : 'No'}
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Application Status</CardTitle>
              <CardDescription>Your current internship applications</CardDescription>
            </CardHeader>
            <CardContent>
              {userApplications.length === 0 ? (
                <p className="text-muted-foreground">You haven't applied to any opportunities yet.</p>
              ) : (
                <div className="space-y-4">
                  {userApplications.map(app => {
                    const opportunity = opportunities.find(opp => opp.id === app.opportunityId);
                    return (
                      <div key={app.id} className="border rounded-lg p-3">
                        <div className="flex justify-between items-start">
                          <div>
                            <h4 className="font-medium">{opportunity?.title} at {opportunity?.company}</h4>
                            <p className="text-sm text-muted-foreground">Applied on {app.appliedDate}</p>
                          </div>
                          <span className={`px-2 py-1 rounded text-xs ${
                            app.status === 'applied' ? 'bg-blue-100 text-blue-800' :
                            app.status === 'approved' ? 'bg-green-100 text-green-800' :
                            app.status === 'rejected' ? 'bg-red-100 text-red-800' :
                            app.status === 'interviewScheduled' ? 'bg-purple-100 text-purple-800' :
                            app.status === 'offerExtended' ? 'bg-amber-100 text-amber-800' :
                            'bg-green-100 text-green-800'
                          }`}>
                            {app.status.charAt(0).toUpperCase() + app.status.slice(1)}
                          </span>
                        </div>
                        {app.mentorApproval && (
                          <p className="text-sm mt-2">
                            Mentor approval: {app.mentorApproval.status}
                          </p>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Recommended Opportunities</CardTitle>
            <CardDescription>Internships matched to your skills and preferences</CardDescription>
          </CardHeader>
          <CardContent>
            {recommendedOpps.length === 0 ? (
              <p className="text-muted-foreground">No recommended opportunities at this time.</p>
            ) : (
              <div className="space-y-4">
                {recommendedOpps.map(opp => {
                  const hasApplied = applications.some(app => 
                    app.studentId === currentUser?.id && app.opportunityId === opp.id
                  );
                  
                  return (
                    <div key={opp.id} className="border rounded-lg p-4">
                      <div className="flex justify-between items-start">
                        <div>
                          <h3 className="font-semibold">{opp.title}</h3>
                          <p className="text-muted-foreground">{opp.company} • {opp.location}</p>
                          <p className="mt-2">{opp.description}</p>
                          <div className="flex flex-wrap gap-1 mt-2">
                            {opp.requiredSkills.map(skill => (
                              <span key={skill} className="bg-accent text-accent-foreground px-2 py-1 rounded-md text-xs">
                                {skill}
                              </span>
                            ))}
                          </div>
                          <div className="flex items-center mt-3 text-sm">
                            <span className="font-medium">Stipend: ₹{opp.stipend}/month</span>
                            <span className="mx-2">•</span>
                            <span>{opp.duration}</span>
                            {opp.placementConversion && (
                              <>
                                <span className="mx-2">•</span>
                                <span className="text-green-600">Placement opportunity</span>
                              </>
                            )}
                          </div>
                        </div>
                        <div>
                          {hasApplied ? (
                            <Button variant="outline" disabled>Applied</Button>
                          ) : (
                            <Button onClick={() => handleApply(opp.id)}>Apply Now</Button>
                          )}
                        </div>
                      </div>
                      <div className="text-xs text-muted-foreground mt-2">
                        Apply by: {opp.applicationDeadline}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    );
  };

  const renderPlacementCellDashboard = () => {
    return (
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Post New Opportunity</CardTitle>
            <CardDescription>Create a new internship or placement opportunity</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="title">Job Title</Label>
                <Input
                  id="title"
                  value={newOpportunity.title || ''}
                  onChange={(e) => setNewOpportunity({...newOpportunity, title: e.target.value})}
                  placeholder="e.g., Frontend Developer Intern"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="company">Company</Label>
                <Input
                  id="company"
                  value={newOpportunity.company || ''}
                  onChange={(e) => setNewOpportunity({...newOpportunity, company: e.target.value})}
                  placeholder="Company name"
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="description">Description</Label>
              <Textarea
                id="description"
                value={newOpportunity.description || ''}
                onChange={(e) => setNewOpportunity({...newOpportunity, description: e.target.value})}
                placeholder="Describe the role, responsibilities, and requirements"
                rows={3}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="department">Department</Label>
                <Select
                  value={newOpportunity.department}
                  onValueChange={(value) => setNewOpportunity({...newOpportunity, department: value})}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select department" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Computer Science">Computer Science</SelectItem>
                    <SelectItem value="Electrical Engineering">Electrical Engineering</SelectItem>
                    <SelectItem value="Mechanical Engineering">Mechanical Engineering</SelectItem>
                    <SelectItem value="Civil Engineering">Civil Engineering</SelectItem>
                    <SelectItem value="Electronics">Electronics</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="stipend">Stipend (₹)</Label>
                <Input
                  id="stipend"
                  type="number"
                  value={newOpportunity.stipend || 0}
                  onChange={(e) => setNewOpportunity({...newOpportunity, stipend: parseInt(e.target.value) || 0})}
                  placeholder="10000"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="duration">Duration</Label>
                <Select
                  value={newOpportunity.duration}
                  onValueChange={(value) => setNewOpportunity({...newOpportunity, duration: value})}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select duration" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="3 months">3 months</SelectItem>
                    <SelectItem value="6 months">6 months</SelectItem>
                    <SelectItem value="8 months">8 months</SelectItem>
                    <SelectItem value="12 months">12 months</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="location">Location</Label>
                <Input
                  id="location"
                  value={newOpportunity.location || ''}
                  onChange={(e) => setNewOpportunity({...newOpportunity, location: e.target.value})}
                  placeholder="e.g., Ranchi, Remote"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="deadline">Application Deadline</Label>
                <Input
                  id="deadline"
                  type="date"
                  value={newOpportunity.applicationDeadline || ''}
                  onChange={(e) => setNewOpportunity({...newOpportunity, applicationDeadline: e.target.value})}
                />
              </div>

              <div className="flex items-center space-x-2 mt-6">
                <input
                  id="placementConversion"
                  type="checkbox"
                  checked={newOpportunity.placementConversion || false}
                  onChange={(e) => setNewOpportunity({...newOpportunity, placementConversion: e.target.checked})}
                  className="h-4 w-4"
                />
                <Label htmlFor="placementConversion">Potential for placement conversion</Label>
              </div>
            </div>

            <div className="space-y-2">
              <Label>Required Skills (comma separated)</Label>
              <Input
                value={newOpportunity.requiredSkills?.join(', ') || ''}
                onChange={(e) => setNewOpportunity({
                  ...newOpportunity, 
                  requiredSkills: e.target.value.split(',').map(skill => skill.trim())
                })}
                placeholder="e.g., JavaScript, React, Python"
              />
            </div>
          </CardContent>
          <CardFooter>
            <Button onClick={handlePostOpportunity}>Post Opportunity</Button>
          </CardFooter>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Posted Opportunities</CardTitle>
            <CardDescription>Your current internship postings</CardDescription>
          </CardHeader>
          <CardContent>
            {opportunities.filter(opp => opp.postedBy === currentUser?.id).length === 0 ? (
              <p className="text-muted-foreground">You haven't posted any opportunities yet.</p>
            ) : (
              <div className="space-y-4">
                {opportunities
                  .filter(opp => opp.postedBy === currentUser?.id)
                  .map(opp => (
                    <div key={opp.id} className="border rounded-lg p-4">
                      <div className="flex justify-between items-start">
                        <div>
                          <h3 className="font-semibold">{opp.title}</h3>
                          <p className="text-muted-foreground">{opp.company} • {opp.location}</p>
                          <div className="flex flex-wrap gap-1 mt-2">
                            {opp.requiredSkills.map(skill => (
                              <span key={skill} className="bg-accent text-accent-foreground px-2 py-1 rounded-md text-xs">
                                {skill}
                              </span>
                            ))}
                          </div>
                        </div>
                        <div className="text-sm text-muted-foreground">
                          Applications: {applications.filter(app => app.opportunityId === opp.id).length}
                        </div>
                      </div>
                      <div className="text-xs text-muted-foreground mt-2">
                        Posted on: {opp.createdAt} • Apply by: {opp.applicationDeadline}
                      </div>
                    </div>
                  ))
                }
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    );
  };

  const renderFacultyDashboard = () => {
    const pendingApprovals = applications.filter(app => 
      app.mentorApproval?.status === 'pending'
    );

    return (
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Pending Approvals</CardTitle>
            <CardDescription>Student applications awaiting your approval</CardDescription>
          </CardHeader>
          <CardContent>
            {pendingApprovals.length === 0 ? (
              <p className="text-muted-foreground">No pending approvals at this time.</p>
            ) : (
              <div className="space-y-4">
                {pendingApprovals.map(app => {
                  const opportunity = opportunities.find(opp => opp.id === app.opportunityId);
                  return (
                    <div key={app.id} className="border rounded-lg p-4">
                      <div className="flex justify-between items-start">
                        <div>
                          <h3 className="font-semibold">{opportunity?.title} at {opportunity?.company}</h3>
                          <p className="text-muted-foreground">Applied on {app.appliedDate}</p>
                        </div>
                        <div className="flex space-x-2">
                          <Button variant="outline" size="sm">Reject</Button>
                          <Button size="sm">Approve</Button>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Approval History</CardTitle>
            <CardDescription>Your recent application decisions</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">No approval history yet.</p>
          </CardContent>
        </Card>
      </div>
    );
  };

  const renderDashboard = () => {
    if (!currentUser) {
      return (
        <div className="flex items-center justify-center h-64">
          <p>Loading...</p>
        </div>
      );
    }

    switch (currentUser.role) {
      case 'student':
        return renderStudentDashboard();
      case 'placementCell':
        return renderPlacementCellDashboard();
      case 'facultyMentor':
        return renderFacultyDashboard();
      default:
        return <div>Role not supported</div>;
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b bg-card">
        <div className="container mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-2">
              <img 
                src="https://placeholder-image-service.onrender.com/image/40x40?prompt=University%20logo%20with%20academic%20symbols&id=8a9bae52-6c34-401e-af31-7f4307c8b4a1" 
                alt="University logo with academic emblem and building silhouette" 
                className="h-10 w-10"
              />
              <h1 className="text-2xl font-bold">Campus Internship & Placement Hub</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-muted-foreground">
                {currentUser?.name} ({currentUser?.role})
              </span>
              <Button variant="outline" size="sm">Logout</Button>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="flex flex-col space-y-6">
          <div className="flex space-x-4 border-b">
            <button
              className={py-2 px-4 border-b-2 ${activeTab === 'dashboard' ? 'border-primary font-medium' : 'border-transparent'}}
              onClick={() => setActiveTab('dashboard')}
            >
              Dashboard
            </button>
            <button
              className={py-2 px-4 border-b-2 ${activeTab === 'opportunities' ? 'border-primary font-medium' : 'border-transparent'}}
              onClick={() => setActiveTab('opportunities')}
            >
              Opportunities
            </button>
            <button
              className={py-2 px-4 border-b-2 ${activeTab === 'profile' ? 'border-primary font-medium' : 'border-transparent'}}
              onClick={() => setActiveTab('profile')}
            >
              Profile
            </button>
          </div>

          {activeTab === 'dashboard' && renderDashboard()}

          {activeTab === 'opportunities' && (
            <Card>
              <CardHeader>
                <CardTitle>All Opportunities</CardTitle>
                <CardDescription>Browse all available internships and placements</CardDescription>
              </CardHeader>
              <CardContent>
                {opportunities.length === 0 ? (
                  <p className="text-muted-foreground">No opportunities available at this time.</p>
                ) : (
                  <div className="space-y-4">
                    {opportunities.map(opp => {
                      const hasApplied = applications.some(app => 
                        app.studentId === currentUser?.id && app.opportunityId === opp.id
                      );
                      
                      return (
                        <div key={opp.id} className="border rounded-lg p-4">
                          <div className="flex justify-between items-start">
                            <div>
                              <h3 className="font-semibold">{opp.title}</h3>
                              <p className="text-muted-foreground">{opp.company} • {opp.location}</p>
                              <p className="mt-2">{opp.description}</p>
                              <div className="flex flex-wrap gap-1 mt-2">
                                {opp.requiredSkills.map(skill => (
                                  <span key={skill} className="bg-accent text-accent-foreground px-2 py-1 rounded-md text-xs">
                                    {skill}
                                  </span>
                                ))}
                              </div>
                              <div className="flex items-center mt-3 text-sm">
                                <span className="font-medium">Stipend: ₹{opp.stipend}/month</span>
                                <span className="mx-2">•</span>
                                <span>{opp.duration}</span>
                                {opp.placementConversion && (
                                  <>
                                    <span className="mx-2">•</span>
                                    <span className="text-green-600">Placement opportunity</span>
                                  </>
                                )}
                              </div>
                            </div>
                            <div>
                              {hasApplied ? (
                                <Button variant="outline" disabled>Applied</Button>
                              ) : (
                                <Button onClick={() => handleApply(opp.id)}>Apply Now</Button>
                              )}
                            </div>
                          </div>
                          <div className="text-xs text-muted-foreground mt-2">
                            Posted on: {opp.createdAt} • Apply by: {opp.applicationDeadline}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </CardContent>
            </Card>
          )}

          {activeTab === 'profile' && (
            <Card>
              <CardHeader>
                <CardTitle>Your Profile</CardTitle>
                <CardDescription>Manage your personal information and preferences</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="name">Full Name</Label>
                    <Input
                      id="name"
                      value={currentUser?.name || ''}
                      disabled
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="email">Email</Label>
                    <Input
                      id="email"
                      value={currentUser?.email || ''}
                      disabled
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="department">Department</Label>
                  <Input
                    id="department"
                    value={currentUser?.department || ''}
                    disabled
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="skills">Skills</Label>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {currentUser?.skills?.map(skill => (
                      <span key={skill} className="bg-secondary text-secondary-foreground px-2 py-1 rounded-md text-sm flex items-center">
                        {skill}
                        <button 
                          onClick={() => handleRemoveSkill(skill)}
                          className="ml-2 text-muted-foreground hover:text-foreground"
                        >
                          &times;
                        </button>
                      </span>
                    ))}
                  </div>
                  <div className="flex mt-2">
                    <Input
                      value={skillInput}
                      onChange={(e) => setSkillInput(e.target.value)}
                      placeholder="Add a skill"
                      className="flex-1"
                    />
                    <Button onClick={handleAddSkill} className="ml-2">Add</Button>
                  </div>
                </div>

                <div className="space-y-4 pt-4">
                  <h3 className="font-medium">Preferences</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="location">Preferred Location</Label>
                      <Input
                        id="location"
                        value={currentUser?.preferences?.location || ''}
                        placeholder="e.g., Ranchi"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="minStipend">Minimum Stipend (₹)</Label>
                      <Input
                        id="minStipend"
                        type="number"
                        value={currentUser?.preferences?.minStipend || 0}
                      />
                    </div>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="maxStipend">Maximum Stipend (₹)</Label>
                      <Input
                        id="maxStipend"
                        type="number"
                        value={currentUser?.preferences?.maxStipend || 0}
                      />
                    </div>
                    <div className="flex items-center space-x-2 mt-6">
                      <input
                        id="placementConversion"
                        type="checkbox"
                        checked={currentUser?.preferences?.placementConversion || false}
                        className="h-4 w-4"
                      />
                      <Label htmlFor="placementConversion">Prefer opportunities with placement conversion</Label>
                    </div>
                  </div>
                </div>
              </CardContent>
              <CardFooter>
                <Button>Save Changes</Button>
              </CardFooter>
            </Card>
          )}
        </div>
      </main>

      <footer className="border-t bg-card mt-12">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <img 
                src="https://placeholder-image-service.onrender.com/image/30x30?prompt=University%20logo%20with%20academic%20symbols&id=8a9bae52-6c34-401e-af31-7f4307c8b4a1" 
                alt="University logo with academic emblem" 
                className="h-6 w-6"
              />
              <p className="text-sm text-muted-foreground">Campus Internship & Placement Hub</p>
            </div>
            <div className="text-sm text-muted-foreground">
              © {new Date().getFullYear()} Technical Education Board. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default CampusInternshipPlacementHub;