import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, Users, DollarSign, TrendingUp, AlertCircle } from 'lucide-react';
import { logAnalyticsEvent } from '../api/client';
import '../styles/AdminDashboard.css';

const AdminDashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('overview');
  const [webhookStats, setWebhookStats] = useState(null);
  const [webhookEvents, setWebhookEvents] = useState([]);
  const [webhookLoading, setWebhookLoading] = useState(false);

  useEffect(() => {
    const checkUser = localStorage.getItem('user');
    if (!checkUser) {
      navigate('/auth');
      return;
    }

    const userData = JSON.parse(checkUser);
    setUser(userData);

    // Simple admin check - in production, check user role from backend
    if (!userData.profile || userData.profile.role !== 'admin') {
      setError('Admin access required');
      navigate('/');
      return;
    }

    fetchDashboardData();
    logAnalyticsEvent('page_visited', 'Admin Dashboard', {}, '/admin');
  }, [navigate]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      // Mock data - in production, fetch from admin endpoints
      const mockData = {
        revenue: {
          mrr: 4299.90,
          arr: 51598.80,
          growth: 12.5,
        },
        users: {
          total: 1247,
          active: 892,
          new_this_month: 156,
        },
        subscriptions: {
          free: 342,
          starter: 456,
          pro: 312,
          enterprise: 137,
        },
        churn: {
          rate: 2.3,
          this_month: 23,
        },
      };
      setDashboardData(mockData);
      setError('');
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchWebhookStats = async () => {
    try {
      setWebhookLoading(true);
      const response = await fetch('/api/webhooks/stats/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });
      
      if (response.ok) {
        const stats = await response.json();
        setWebhookStats(stats);
      } else {
        console.error('Failed to fetch webhook stats');
      }
    } catch (err) {
      console.error('Error fetching webhook stats:', err);
    } finally {
      setWebhookLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="admin-container">
        <p className="loading-text">Loading admin dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="admin-container">
        <div className="error-alert">
          <AlertCircle size={24} />
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!dashboardData) {
    return null;
  }

  const { revenue, users, subscriptions, churn } = dashboardData;

  return (
    <div className="admin-container">
      <div className="admin-header">
        <h1>
          <Shield size={28} />
          Admin Dashboard
        </h1>
        <p>Platform statistics and management tools</p>
      </div>

      <div className="admin-tabs">
        <button
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={`tab ${activeTab === 'revenue' ? 'active' : ''}`}
          onClick={() => setActiveTab('revenue')}
        >
          Revenue
        </button>
        <button
          className={`tab ${activeTab === 'users' ? 'active' : ''}`}
          onClick={() => setActiveTab('users')}
        >
          Users
        </button>
        <button
          className={`tab ${activeTab === 'subscriptions' ? 'active' : ''}`}
          onClick={() => setActiveTab('subscriptions')}
        >
          Subscriptions
        </button>
        <button
          className={`tab ${activeTab === 'webhooks' ? 'active' : ''}`}
          onClick={() => {
            setActiveTab('webhooks');
            if (!webhookStats) fetchWebhookStats();
          }}
        >
          Webhooks
        </button>
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && (
        <div className="tab-content">
          <div className="kpi-grid">
            <div className="kpi-card">
              <div className="kpi-icon revenue-icon">
                <DollarSign size={28} />
              </div>
              <div className="kpi-info">
                <p className="kpi-label">Monthly Revenue</p>
                <p className="kpi-value">${revenue.mrr.toFixed(2)}</p>
                <p className="kpi-trend positive">+{revenue.growth}% vs last month</p>
              </div>
            </div>

            <div className="kpi-card">
              <div className="kpi-icon users-icon">
                <Users size={28} />
              </div>
              <div className="kpi-info">
                <p className="kpi-label">Total Users</p>
                <p className="kpi-value">{users.total}</p>
                <p className="kpi-trend">{users.new_this_month} new this month</p>
              </div>
            </div>

            <div className="kpi-card">
              <div className="kpi-icon active-icon">
                <TrendingUp size={28} />
              </div>
              <div className="kpi-info">
                <p className="kpi-label">Active Users</p>
                <p className="kpi-value">{users.active}</p>
                <p className="kpi-trend">{((users.active / users.total) * 100).toFixed(1)}% activity rate</p>
              </div>
            </div>

            <div className="kpi-card">
              <div className="kpi-icon churn-icon">
                <AlertCircle size={28} />
              </div>
              <div className="kpi-info">
                <p className="kpi-label">Churn Rate</p>
                <p className="kpi-value">{churn.rate}%</p>
                <p className="kpi-trend negative">{churn.this_month} cancellations</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Revenue Tab */}
      {activeTab === 'revenue' && (
        <div className="tab-content">
          <div className="revenue-section">
            <h2>Revenue Analytics</h2>
            <div className="revenue-grid">
              <div className="revenue-card">
                <p className="label">Monthly Recurring Revenue (MRR)</p>
                <p className="value">${revenue.mrr.toFixed(2)}</p>
              </div>
              <div className="revenue-card">
                <p className="label">Annual Run Rate (ARR)</p>
                <p className="value">${revenue.arr.toFixed(2)}</p>
              </div>
              <div className="revenue-card">
                <p className="label">Growth Rate</p>
                <p className="value positive">{revenue.growth}%</p>
              </div>
              <div className="revenue-card">
                <p className="label">Average Revenue Per User</p>
                <p className="value">${(revenue.mrr / users.total).toFixed(2)}</p>
              </div>
            </div>

            <div className="revenue-breakdown">
              <h3>Revenue by Tier</h3>
              <div className="tier-breakdown">
                <div className="tier-item">
                  <div className="tier-name">Starter</div>
                  <div className="tier-contribution">
                    <div className="bar" style={{width: '35%'}}></div>
                  </div>
                  <div className="tier-revenue">$1,507.44</div>
                </div>
                <div className="tier-item">
                  <div className="tier-name">Pro</div>
                  <div className="tier-contribution">
                    <div className="bar" style={{width: '45%'}}></div>
                  </div>
                  <div className="tier-revenue">$1,934.87</div>
                </div>
                <div className="tier-item">
                  <div className="tier-name">Enterprise</div>
                  <div className="tier-contribution">
                    <div className="bar" style={{width: '20%'}}></div>
                  </div>
                  <div className="tier-revenue">$857.59</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Users Tab */}
      {activeTab === 'users' && (
        <div className="tab-content">
          <div className="users-section">
            <h2>User Analytics</h2>
            <div className="users-grid">
              <div className="user-stat">
                <p className="stat-label">Total Users</p>
                <p className="stat-value">{users.total}</p>
              </div>
              <div className="user-stat">
                <p className="stat-label">Active Users</p>
                <p className="stat-value">{users.active}</p>
              </div>
              <div className="user-stat">
                <p className="stat-label">New This Month</p>
                <p className="stat-value">{users.new_this_month}</p>
              </div>
              <div className="user-stat">
                <p className="stat-label">User Growth</p>
                <p className="stat-value positive">+12.4%</p>
              </div>
            </div>

            <div className="user-growth-chart">
              <h3>User Growth Trend</h3>
              <div className="chart-placeholder">
                <p>User growth chart visualization would appear here</p>
                <p>(Replace with actual charting library in production)</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Subscriptions Tab */}
      {activeTab === 'subscriptions' && (
        <div className="tab-content">
          <div className="subscriptions-section">
            <h2>Subscription Distribution</h2>
            <div className="subscription-breakdown">
              <div className="subscription-card">
                <h4>Free</h4>
                <p className="subscription-count">{subscriptions.free}</p>
                <p className="subscription-percent">
                  {((subscriptions.free / users.total) * 100).toFixed(1)}% of users
                </p>
                <div className="progress-bar">
                  <div className="progress-fill" style={{width: `${(subscriptions.free / users.total) * 100}%`}}></div>
                </div>
              </div>

              <div className="subscription-card">
                <h4>Starter</h4>
                <p className="subscription-count">{subscriptions.starter}</p>
                <p className="subscription-percent">
                  {((subscriptions.starter / users.total) * 100).toFixed(1)}% of users
                </p>
                <div className="progress-bar">
                  <div className="progress-fill" style={{width: `${(subscriptions.starter / users.total) * 100}%`}}></div>
                </div>
              </div>

              <div className="subscription-card">
                <h4>Pro</h4>
                <p className="subscription-count">{subscriptions.pro}</p>
                <p className="subscription-percent">
                  {((subscriptions.pro / users.total) * 100).toFixed(1)}% of users
                </p>
                <div className="progress-bar">
                  <div className="progress-fill" style={{width: `${(subscriptions.pro / users.total) * 100}%`}}></div>
                </div>
              </div>

              <div className="subscription-card">
                <h4>Enterprise</h4>
                <p className="subscription-count">{subscriptions.enterprise}</p>
                <p className="subscription-percent">
                  {((subscriptions.enterprise / users.total) * 100).toFixed(1)}% of users
                </p>
                <div className="progress-bar">
                  <div className="progress-fill" style={{width: `${(subscriptions.enterprise / users.total) * 100}%`}}></div>
                </div>
              </div>
            </div>

            <div className="churn-section">
              <h3>Churn Analytics</h3>
              <div className="churn-stats">
                <div className="churn-stat">
                  <p className="label">Monthly Churn Rate</p>
                  <p className="value">{churn.rate}%</p>
                </div>
                <div className="churn-stat">
                  <p className="label">Cancellations This Month</p>
                  <p className="value">{churn.this_month}</p>
                </div>
                <div className="churn-stat">
                  <p className="label">Retention Rate</p>
                  <p className="value positive">{(100 - churn.rate).toFixed(1)}%</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Webhooks Tab */}
      {activeTab === 'webhooks' && (
        <div className="tab-content">
          <div className="webhooks-section">
            <h2>Webhook Events</h2>
            
            {webhookLoading ? (
              <p className="loading-text">Loading webhook statistics...</p>
            ) : webhookStats ? (
              <>
                <div className="webhook-stats-grid">
                  <div className="webhook-stat-card">
                    <p className="stat-label">Total Events</p>
                    <p className="stat-value">{webhookStats.total_events}</p>
                  </div>
                  <div className="webhook-stat-card success">
                    <p className="stat-label">Succeeded</p>
                    <p className="stat-value">{webhookStats.succeeded}</p>
                  </div>
                  <div className="webhook-stat-card">
                    <p className="stat-label">Failed</p>
                    <p className="stat-value" style={{color: webhookStats.failed > 0 ? '#ef4444' : '#10b981'}}>
                      {webhookStats.failed}
                    </p>
                  </div>
                  <div className="webhook-stat-card">
                    <p className="stat-label">Processing</p>
                    <p className="stat-value">{webhookStats.processing}</p>
                  </div>
                  <div className="webhook-stat-card">
                    <p className="stat-label">Ignored</p>
                    <p className="stat-value">{webhookStats.ignored}</p>
                  </div>
                  <div className="webhook-stat-card">
                    <p className="stat-label">Success Rate</p>
                    <p className="stat-value">{webhookStats.success_rate}%</p>
                  </div>
                </div>

                {webhookStats.event_type_breakdown && webhookStats.event_type_breakdown.length > 0 && (
                  <div className="webhook-breakdown">
                    <h3>Event Type Breakdown</h3>
                    <div className="event-type-list">
                      {webhookStats.event_type_breakdown.map((item, idx) => (
                        <div key={idx} className="event-type-item">
                          <span className="event-type-name">{item.event_type}</span>
                          <span className="event-type-count">{item.count} events</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {webhookStats.recent_failed_events && webhookStats.recent_failed_events.length > 0 && (
                  <div className="recent-failed">
                    <h3>Recent Failed Events</h3>
                    <div className="failed-events-list">
                      {webhookStats.recent_failed_events.map((event) => (
                        <div key={event.id} className="failed-event-item">
                          <div className="event-header">
                            <span className="event-id">{event.stripe_event_id}</span>
                            <span className="event-type-badge">{event.event_type}</span>
                          </div>
                          <p className="event-error">{event.error_message}</p>
                          <p className="event-time">{new Date(event.received_at).toLocaleString()}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </>
            ) : (
              <p>No webhook data available. Click refresh to load.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;
