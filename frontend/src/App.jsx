import React, { useState, useEffect } from "react";
import { Header } from "./components/Header";
import { Sidebar } from "./components/Sidebar";
import { OverviewView } from "./views/OverviewView";
import { CompetencyView } from "./views/CompetencyView";
import { LearningPathView } from "./views/LearningPathView";
import { RecommendationsView } from "./views/RecommendationsView";
import { AssessmentsView } from "./views/AssessmentsView";
import { QuizPlayerView } from "./views/QuizPlayerView";
import { TutorView } from "./views/TutorView";
import { AdminAnalyticsView } from "./views/AdminAnalyticsView";
import { ProfileSettingsView } from "./views/ProfileSettingsView";
import { VirtualLabView } from "./views/VirtualLabView";
import { api } from "./api";

export function App() {
  const [activeTab, setActiveTab] = useState("overview");
  const [currentRole, setCurrentRole] = useState("JSO");
  const [profileData, setProfileData] = useState(null);
  const [learningPathData, setLearningPathData] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [activeQuiz, setActiveQuiz] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load initial profile, learning path and recommendations
  const refreshUserData = async () => {
    try {
      setLoading(true);
      const [prof, path, recs] = await Promise.all([
        api.getProfile(),
        api.getLearningPath(),
        api.getRecommendations("All")
      ]);
      setProfileData(prof);
      setLearningPathData(path);
      setRecommendations(recs.recommendations || []);
      setCurrentRole(prof?.learner?.role_code || "JSO");
    } catch (err) {
      console.warn("API loading fallback:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshUserData();
  }, []);

  const handleRoleChange = async (newRole) => {
    setCurrentRole(newRole);
    try {
      const updated = await api.switchRole(newRole);
      setProfileData(updated);
      const path = await api.getLearningPath();
      setLearningPathData(path);
    } catch (e) {
      console.error(e);
    }
  };

  const handleQuizCompleted = async (result) => {
    // Refresh user state after quiz submission
    await refreshUserData();
  };

  const handlePublishQuiz = (newAssessment) => {
    setActiveQuiz(newAssessment);
  };

  return (
    <div className="min-h-screen bg-statwise-canvas text-statwise-navy flex flex-col font-sans">
      {/* Official MoSPI STATWISE Top Bar */}
      <Header
        currentRole={currentRole}
        onRoleChange={handleRoleChange}
        learner={profileData?.learner}
      />

      <div className="flex flex-1">
        {/* STATWISE Screenbook Sidebar */}
        <Sidebar activeTab={activeTab} onSelectTab={setActiveTab} />

        {/* Main Readable Content Area */}
        <main className="flex-1 p-6 lg:p-8 max-w-7xl mx-auto w-full overflow-x-hidden">
          {activeTab === "overview" && (
            <OverviewView profileData={profileData} onNavigate={setActiveTab} />
          )}
          {activeTab === "competency" && (
            <CompetencyView profileData={profileData} onNavigate={setActiveTab} />
          )}
          {activeTab === "pathway" && (
            <LearningPathView
              learningPathData={learningPathData}
              onNavigate={setActiveTab}
            />
          )}
          {activeTab === "recommendations" && (
            <RecommendationsView
              recommendations={recommendations}
              onSelectCourse={(c) => setActiveTab("pathway")}
            />
          )}
          {activeTab === "assessments" && (
            <AssessmentsView
              onPublishQuiz={handlePublishQuiz}
              onNavigate={setActiveTab}
            />
          )}
          {activeTab === "quiz" && (
            <QuizPlayerView
              activeQuiz={activeQuiz}
              onQuizCompleted={handleQuizCompleted}
              onNavigate={setActiveTab}
            />
          )}
          {activeTab === "tutor" && <TutorView />}
          {activeTab === "analytics" && <AdminAnalyticsView />}
          {activeTab === "virtuallab" && <VirtualLabView />}
          {activeTab === "profile" && (
            <ProfileSettingsView
              learner={profileData?.learner}
              currentRole={currentRole}
              onRoleChange={handleRoleChange}
            />
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
