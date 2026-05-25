import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { BarChart3, TrendingUp, Activity, Zap } from 'lucide-react';
import { getAnalyticsDashboard, logAnalyticsEvent } from '../api/client';
import '../styles/UserAnalytics.css';

const UserAnalytics = () => {
  const navigate = useNavigate();
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [days, setDays] = useState(30);
  const [error, setError] = useState('');

  useEffect(() => {
    const checkUser = localStorage.getItem('user');
    if (!checkUser) {
      navigate('/auth');
      return;
    }
    
    fetchAnalytics();
    logAnalyticsEvent('page_visited', 'Analytics Dashboard', {}, '/analytics');
  }, [navigate, days]);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const response = await getAnalyticsDashboard(days);
      setAnalytics(response.data);
      setError('');
    } catch (err) {
      setError('Failed to load analytics data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="analytics-container">
        <p className="loading-text">Loading analytics...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="analytics-container">
        <p className="error-text">{error}</p>
      </div>
    );
  }

  if (!analytics) {
    return null;
  }

  const { subscription, engagement, event_breakdown, top_pages } = analytics;
  const tokenUsagePercent = subscription.tokens_limit > 0 
    ? Math.round(((subscription.tokens_limit - subscription.tokens_remaining) / subscription.tokens_limit) * 100)
    : 0;

  return (
    <div className="analytics-container">
      <div className="analytics-header">
        <h1>
          <BarChart3 size={28} />
          Analytics Dashboard
        </h1>
        <p>Track your usage and engagement metrics</p>
      </div>

      <div className="date-filter">
        <label>Time Period:</label>
        <select value={days} onChange={(e) => setDays(parseInt(e.target.value))}>
          <option value={7}>Last 7 Days</option>
          <option value={30}>Last 30 Days</option>
          <option value={90}>Last 90 Days</option>
        </select>
      </div>

      {/* Subscription Card */}
      <div className="analytics-section">
        <h2>Subscription Status</h2>
        <div className="subscription-grid">
          <div className="stat-card">
            <div className="stat-icon tier-icon">
              <Zap size={24} />
            </div>
            <div className="stat-info">
              <p className="stat-label">Current Plan</p>
              <p className="stat-value">{subscription.tier}</p>
            </div>
          </div>
          
          <div className="stat-card">
            <div className="stat-icon tokens-icon">
              <Activity size={24} />
            </div>
            <div className="stat-info">
              <p className="stat-label">Tokens Remaining</p>
              <p className="stat-value">{subscription.tokens_remaining} / {subscription.tokens_limit}</p>
              <div className="progress-bar">
                <div 
                  className="progress-fill" 
                  style={{ width: `${100 - tokenUsagePercent}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Engagement Metrics */}
      <div className="analytics-section">
        <h2>Engagement Metrics</h2>
        <div className="metrics-grid">
          <div className="metric-card">
            <div className="metric-icon">
              <TrendingUp size={24} />
            </div>
            <div className="metric-info">
              <p className="metric-label">Total Events</p>
              <p className="metric-value">{engagement.total_events}</p>
            </div>
          </div>

          <div className="metric-card">
            <div className="metric-icon">
              <Activity size={24} />
            </div>
            <div className="metric-info">
              <p className="metric-label">Active Days</p>
              <p className="metric-value">{engagement.active_days}</p>
            </div>
          </div>

          <div className="metric-card">
            <div className="metric-icon">
              <BarChart3 size={24} />
            </div>
            <div className="metric-info">
              <p className="metric-label">Avg Daily Events</p>
              <p className="metric-value">{engagement.avg_daily_events}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Event Breakdown */}
      <div className="analytics-section">
        <h2>Activity Breakdown</h2>
        <div className="events-breakdown">
          {Object.entries(event_breakdown).map(([event, count]) => (
            <div key={event} className="event-item">
              <div className="event-name">
                {event.replace(/_/g, ' ').charAt(0).toUpperCase() + event.replace(/_/g, ' ').slice(1)}
              </div>
              <div className="event-count">
                <div className="count-bar">
                  <div 
                    className="count-fill" 
                    style={{ 
                      width: `${Math.max(10, (count / Math.max(...Object.values(event_breakdown), 1)) * 100)}%` 
                    }}
                  ></div>
                </div>
                <span className="count-number">{count}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Top Pages */}
      {top_pages.length > 0 && (
        <div className="analytics-section">
          <h2>Most Visited Pages</h2>
          <div className="pages-list">
            {top_pages.map((page, idx) => (
              <div key={idx} className="page-item">
                <div className="page-rank">{idx + 1}</div>
                <div className="page-name">{page.page}</div>
                <div className="page-visits">
                  <span className="visits-badge">{page.count}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="analytics-footer">
        <p>Data updated in real-time. This period covers the last {days} days.</p>
      </div>
    </div>
  );
};

export default UserAnalytics;
