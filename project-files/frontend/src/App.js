import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import Footer from './components/Footer';
import Dashboard from './pages/Dashboard';
import Trends from './pages/Trends';
import Competitors from './pages/Competitors';
import Sentiment from './pages/Sentiment';
import Reports from './pages/Reports';
import AIAgent from './pages/AIAgent';
import Auth from './pages/Auth';
import Plans from './pages/Plans';
import Billing from './pages/Billing';
import Terms from './pages/Terms';
import Privacy from './pages/Privacy';
import AccountSettings from './pages/AccountSettings';
import AnalyticsDashboard from './pages/AnalyticsDashboard';
import AdminDashboard from './pages/AdminDashboard';
import './App.css';
import './styles/Pages.css';
import './styles/Billing.css';
import './styles/AccountSettings.css';
import './styles/AnalyticsDashboard.css';
import './styles/AdminDashboard.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Navigation />
        <main className="main-content">
          <div className="routes-container">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/trends" element={<Trends />} />
              <Route path="/competitors" element={<Competitors />} />
              <Route path="/sentiment" element={<Sentiment />} />
              <Route path="/reports" element={<Reports />} />
              <Route path="/ai-agent" element={<AIAgent />} />
              <Route path="/auth" element={<Auth />} />
              <Route path="/plans" element={<Plans />} />
              <Route path="/billing" element={<Billing />} />
              <Route path="/account" element={<AccountSettings />} />
              <Route path="/analytics" element={<AnalyticsDashboard />} />
              <Route path="/admin" element={<AdminDashboard />} />
              <Route path="/terms" element={<Terms />} />
              <Route path="/privacy" element={<Privacy />} />
            </Routes>
          </div>
          <Footer />
        </main>
      </div>
    </Router>
  );
}

export default App;
