import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
import { Calendar, Download, TrendingUp, Activity, Zap } from 'lucide-react';
import { getAnalyticsDashboard, exportAnalytics, logAnalyticsEvent } from '../api/client';
import '../styles/AnalyticsDashboard.css';

function AnalyticsDashboard() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [daysPeriod, setDaysPeriod] = useState(30);
  const [exportFormat, setExportFormat] = useState('csv');
  const [dashboardData, setDashboardData] = useState(null);
  const [exporting, setExporting] = useState(false);

  // Chart colors
  const COLORS = ['#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#3b82f6', '#6366f1', '#14b8a6', '#f97316'];

  useEffect(() => {
    const user = localStorage.getItem('user');
    if (!user) {
      navigate('/auth');
      return;
    }

    fetchAnalyticsData();
  }, [navigate, daysPeriod]);

  const fetchAnalyticsData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getAnalyticsDashboard(daysPeriod);
      setDashboardData(response.data || response);
      
      // Log analytics event for dashboard view
      logAnalyticsEvent(
        'page_visited',
        'Analytics Dashboard Viewed',
        { period_days: daysPeriod },
        'analytics'
      ).catch(err => console.error('Failed to log analytics event:', err));
    } catch (err) {
      setError('Failed to load analytics data');
      console.error('Analytics error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    if (!dashboardData) return;
    
    try {
      setExporting(true);
      
      // Call backend export endpoint
      const blob = await exportAnalytics(exportFormat, daysPeriod);
      
      // Create download link
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', `analytics-${new Date().toISOString().split('T')[0]}.${exportFormat}`);
      link.style.visibility = 'hidden';
      
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
      
      // Log export event
      logAnalyticsEvent(
        'export',
        'Analytics Data Exported',
        { format: exportFormat, period_days: daysPeriod },
        'analytics'
      ).catch(err => console.error('Failed to log export event:', err));
      
    } catch (error) {
      console.error('Export error:', error);
      setError('Failed to export data');
    } finally {
      setExporting(false);
    }
  };

  const generateCSV = () => {
    if (!dashboardData) return '';
    
    let csv = 'Analytics Dashboard Export\n';
    csv += `Generated: ${new Date().toLocaleString()}\n`;
    csv += `Period: Last ${daysPeriod} days\n\n`;
    
    // Engagement section
    csv += 'ENGAGEMENT METRICS\n';
    csv += 'Metric,Value\n';
    csv += `Total Events,${dashboardData.engagement.total_events}\n`;
    csv += `Active Days,${dashboardData.engagement.active_days}\n`;
    csv += `Average Daily Events,${dashboardData.engagement.avg_daily_events}\n\n`;
    
    // Event breakdown
    csv += 'EVENT BREAKDOWN\n';
    csv += 'Event Type,Count\n';
    Object.entries(dashboardData.event_breakdown).forEach(([type, count]) => {
      csv += `${type},${count}\n`;
    });
    csv += '\n';
    
    // Top pages
    csv += 'TOP PAGES\n';
    csv += 'Page,Visits\n';
    dashboardData.top_pages.forEach(({ page, count }) => {
      csv += `"${page}",${count}\n`;
    });
    
    return csv;
  };

  if (loading) {
    return (
      <div className="analytics-container">
        <div className="analytics-loader">
          <p>Loading analytics dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="analytics-container">
        <div className="analytics-error">
          <p>{error}</p>
          <button onClick={fetchAnalyticsData} className="retry-button">
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div className="analytics-container">
        <div className="analytics-empty">
          <p>No analytics data available yet</p>
        </div>
      </div>
    );
  }

  // Prepare chart data
  const eventBreakdownData = Object.entries(dashboardData.event_breakdown).map(([type, count]) => ({
    name: type.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()),
    count: count
  }));

  const topPagesData = dashboardData.top_pages.map(({ page, count }) => ({
    name: page.length > 30 ? page.substring(0, 27) + '...' : page,
    visits: count,
    fullName: page
  }));

  return (
    <div className="analytics-container">
      {/* Header */}
      <div className="analytics-header">
        <div className="header-content">
          <h1>Analytics Dashboard</h1>
          <p>Detailed insights into your feature usage and engagement</p>
        </div>
        
        <div className="header-actions">
          {/* Date Period Selector */}
          <div className="period-selector">
            <Calendar size={18} />
            <select 
              value={daysPeriod} 
              onChange={(e) => setDaysPeriod(parseInt(e.target.value))}
              className="period-dropdown"
            >
              <option value={7}>Last 7 days</option>
              <option value={30}>Last 30 days</option>
              <option value={90}>Last 90 days</option>
            </select>
          </div>

          {/* Export Format Selector */}
          <div className="period-selector">
            <Download size={18} />
            <select 
              value={exportFormat} 
              onChange={(e) => setExportFormat(e.target.value)}
              className="period-dropdown"
            >
              <option value="csv">Export as CSV</option>
              <option value="json">Export as JSON</option>
            </select>
          </div>

          {/* Export Button */}
          <button 
            onClick={handleExport} 
            disabled={exporting}
            className="export-button"
          >
            <Download size={18} />
            {exporting ? 'Exporting...' : 'Export'}
          </button>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon activity">
            <Activity size={24} />
          </div>
          <div className="metric-content">
            <p className="metric-label">Total Events</p>
            <h3 className="metric-value">{dashboardData.engagement.total_events.toLocaleString()}</h3>
            <p className="metric-subtitle">in this period</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon trending">
            <TrendingUp size={24} />
          </div>
          <div className="metric-content">
            <p className="metric-label">Active Days</p>
            <h3 className="metric-value">{dashboardData.engagement.active_days}</h3>
            <p className="metric-subtitle">days used</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon zap">
            <Zap size={24} />
          </div>
          <div className="metric-content">
            <p className="metric-label">Avg Daily Events</p>
            <h3 className="metric-value">{dashboardData.engagement.avg_daily_events}</h3>
            <p className="metric-subtitle">per active day</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon subscription">
            <Calendar size={24} />
          </div>
          <div className="metric-content">
            <p className="metric-label">Current Plan</p>
            <h3 className="metric-value">{dashboardData.subscription.tier}</h3>
            <p className="metric-subtitle">
              {dashboardData.subscription.tokens_remaining} / {dashboardData.subscription.tokens_limit} tokens
            </p>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="charts-section">
        {/* Event Breakdown Chart */}
        <div className="chart-card">
          <h2>Event Breakdown</h2>
          <div className="chart-container">
            {eventBreakdownData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={eventBreakdownData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                  <XAxis 
                    dataKey="name" 
                    angle={-45}
                    textAnchor="end"
                    height={100}
                    tick={{ fontSize: 12 }}
                  />
                  <YAxis />
                  <Tooltip 
                    contentStyle={{
                      backgroundColor: 'rgba(0,0,0,0.8)',
                      border: '1px solid rgba(255,255,255,0.2)',
                      borderRadius: '8px'
                    }}
                  />
                  <Bar dataKey="count" fill="#8b5cf6" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="no-data">No event data available</div>
            )}
          </div>
        </div>

        {/* Top Pages Chart */}
        <div className="chart-card">
          <h2>Top Pages Visited</h2>
          <div className="chart-container">
            {topPagesData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart 
                  data={topPagesData}
                  layout="vertical"
                  margin={{ left: 150, right: 30, top: 5, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                  <XAxis type="number" />
                  <YAxis dataKey="name" type="category" width={145} tick={{ fontSize: 11 }} />
                  <Tooltip 
                    contentStyle={{
                      backgroundColor: 'rgba(0,0,0,0.8)',
                      border: '1px solid rgba(255,255,255,0.2)',
                      borderRadius: '8px'
                    }}
                  />
                  <Bar dataKey="visits" fill="#ec4899" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="no-data">No page data available</div>
            )}
          </div>
        </div>
      </div>

      {/* Event Type Details Table */}
      <div className="details-section">
        <h2>Event Details</h2>
        <div className="details-table">
          <div className="table-header">
            <div className="table-cell">Event Type</div>
            <div className="table-cell">Count</div>
            <div className="table-cell">Percentage</div>
          </div>
          {eventBreakdownData.map((event, index) => (
            <div key={index} className="table-row">
              <div className="table-cell">
                <span className="event-type-badge" style={{ backgroundColor: COLORS[index % COLORS.length] }}>
                  {event.name}
                </span>
              </div>
              <div className="table-cell">{event.count}</div>
              <div className="table-cell">
                {dashboardData.engagement.total_events > 0 
                  ? ((event.count / dashboardData.engagement.total_events) * 100).toFixed(1) 
                  : 0}%
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Top Pages Details Table */}
      {topPagesData.length > 0 && (
        <div className="details-section">
          <h2>Page Visit Details</h2>
          <div className="details-table">
            <div className="table-header">
              <div className="table-cell">Page</div>
              <div className="table-cell">Visits</div>
              <div className="table-cell">Percentage</div>
            </div>
            {topPagesData.map((page, index) => (
              <div key={index} className="table-row">
                <div className="table-cell" title={page.fullName}>
                  {page.fullName}
                </div>
                <div className="table-cell">{page.visits}</div>
                <div className="table-cell">
                  {dashboardData.engagement.total_events > 0 
                    ? ((page.visits / dashboardData.engagement.total_events) * 100).toFixed(1) 
                    : 0}%
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default AnalyticsDashboard;
