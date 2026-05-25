import React, { useEffect, useState } from 'react';
import { getAnalysis } from '../api/client';
import { SkeletonGrid } from '../components/SkeletonLoader';
import { FileText, TrendingUp, BarChart3, Target, Zap, ChevronDown } from 'lucide-react';
import '../styles/Reports.css';

function Reports() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(false);
  const [expandedId, setExpandedId] = useState(null);
  const [analysisTypeFilter, setAnalysisTypeFilter] = useState('all');

  useEffect(() => {
    fetchReports();
  }, [analysisTypeFilter]);

  const fetchReports = async () => {
    setLoading(true);
    try {
      const params = {};
      if (analysisTypeFilter !== 'all') {
        params.analysis_type = analysisTypeFilter;
      }
      const response = await getAnalysis(params);
      setReports(response.data || []);
    } catch (error) {
      console.error('Error fetching reports:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleExpand = (id) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const getAnalysisIcon = (type) => {
    switch(type) {
      case 'market_gap': return <Target size={20} />;
      case 'trend_analysis': return <TrendingUp size={20} />;
      case 'competitor_analysis': return <BarChart3 size={20} />;
      case 'niche_discovery': return <Zap size={20} />;
      default: return <FileText size={20} />;
    }
  };

  const getAnalysisTypeLabel = (type) => {
    switch(type) {
      case 'market_gap': return 'Market Gap Analysis';
      case 'trend_analysis': return 'Trend Analysis';
      case 'competitor_analysis': return 'Competitor Analysis';
      case 'niche_discovery': return 'Niche Discovery';
      default: return 'Analysis';
    }
  };

  const getConfidenceColor = (score) => {
    if (score >= 90) return '#10b981';
    if (score >= 80) return '#3b82f6';
    if (score >= 70) return '#f59e0b';
    return '#ef4444';
  };

  return (
    <div className="reports-page">
      <header className="page-header">
        <h1>Reports & Analytics</h1>
        <p>Comprehensive market analysis reports and AI-generated insights</p>
      </header>

      {/* Filters */}
      <section className="filter-section">
        <h4>Report Type</h4>
        <div className="filter-buttons">
          <button 
            className={`filter-btn ${analysisTypeFilter === 'all' ? 'active' : ''}`}
            onClick={() => { setAnalysisTypeFilter('all'); fetchReports(); }}
          >
            All Reports
          </button>
          <button 
            className={`filter-btn ${analysisTypeFilter === 'market_gap' ? 'active' : ''}`}
            onClick={() => { setAnalysisTypeFilter('market_gap'); fetchReports(); }}
          >
            Market Gaps
          </button>
          <button 
            className={`filter-btn ${analysisTypeFilter === 'trend_analysis' ? 'active' : ''}`}
            onClick={() => { setAnalysisTypeFilter('trend_analysis'); fetchReports(); }}
          >
            Trends
          </button>
          <button 
            className={`filter-btn ${analysisTypeFilter === 'competitor_analysis' ? 'active' : ''}`}
            onClick={() => { setAnalysisTypeFilter('competitor_analysis'); fetchReports(); }}
          >
            Competitors
          </button>
          <button 
            className={`filter-btn ${analysisTypeFilter === 'niche_discovery' ? 'active' : ''}`}
            onClick={() => { setAnalysisTypeFilter('niche_discovery'); fetchReports(); }}
          >
            Niches
          </button>
        </div>
      </section>

      {/* Reports List */}
      {loading ? (
        <SkeletonGrid count={4} />
      ) : (
        <div className="reports-container">
          {reports.length > 0 ? (
            <div className="reports-list">
              {reports.map((report) => (
                <div 
                  key={report.id} 
                  className={`report-card ${expandedId === report.id ? 'expanded' : ''}`}
                >
                  <div 
                    className="report-header"
                    onClick={() => toggleExpand(report.id)}
                  >
                    <div className="header-content">
                      <div className="icon-wrapper">
                        {getAnalysisIcon(report.analysis_type)}
                      </div>
                      <div className="header-info">
                        <h3>{report.query}</h3>
                        <p className="report-type">
                          {getAnalysisTypeLabel(report.analysis_type)}
                        </p>
                      </div>
                    </div>
                    <div className="header-meta">
                      <div className="confidence-badge" style={{
                        background: getConfidenceColor(report.confidence_score),
                        color: 'white'
                      }}>
                        {report.confidence_score.toFixed(1)}% confidence
                      </div>
                      <ChevronDown 
                        size={20} 
                        className={`expand-icon ${expandedId === report.id ? 'rotated' : ''}`}
                      />
                    </div>
                  </div>

                  {expandedId === report.id && (
                    <div className="report-body">
                      {/* Overview */}
                      <section className="report-section">
                        <h4>Overview</h4>
                        <p className="insight-text">{report.ai_insights.overview}</p>
                        <div className="insight-grid">
                          {report.ai_insights.market_size && (
                            <div className="insight-item">
                              <span className="label">Market Size</span>
                              <span className="value">{report.ai_insights.market_size}</span>
                            </div>
                          )}
                          {report.ai_insights.growth_trend && (
                            <div className="insight-item">
                              <span className="label">Growth Trend</span>
                              <span className="value" style={{ color: '#10b981' }}>
                                {report.ai_insights.growth_trend}
                              </span>
                            </div>
                          )}
                          {report.ai_insights.key_insight && (
                            <div className="insight-item full-width">
                              <span className="label">Key Insight</span>
                              <span className="value">{report.ai_insights.key_insight}</span>
                            </div>
                          )}
                        </div>
                      </section>

                      {/* Trending Mechanics */}
                      {report.trending_mechanics && report.trending_mechanics.length > 0 && (
                        <section className="report-section">
                          <h4>Trending Mechanics</h4>
                          <ul className="insight-list">
                            {report.trending_mechanics.map((mechanic, idx) => (
                              <li key={idx}>{mechanic}</li>
                            ))}
                          </ul>
                        </section>
                      )}

                      {/* Rising Genres */}
                      {report.rising_genres && report.rising_genres.length > 0 && (
                        <section className="report-section">
                          <h4>Rising Genres</h4>
                          <ul className="insight-list">
                            {report.rising_genres.map((genre, idx) => (
                              <li key={idx}>{genre}</li>
                            ))}
                          </ul>
                        </section>
                      )}

                      {/* Market Gaps */}
                      {report.market_gaps && report.market_gaps.length > 0 && (
                        <section className="report-section">
                          <h4>Market Gaps & Opportunities</h4>
                          <ul className="insight-list opportunity">
                            {report.market_gaps.map((gap, idx) => (
                              <li key={idx}>
                                <span className="opportunity-icon">→</span>
                                {gap}
                              </li>
                            ))}
                          </ul>
                        </section>
                      )}

                      {/* Monetization Opportunities */}
                      {report.monetization_opportunities && report.monetization_opportunities.length > 0 && (
                        <section className="report-section">
                          <h4>Monetization Opportunities</h4>
                          <ul className="insight-list">
                            {report.monetization_opportunities.map((opp, idx) => (
                              <li key={idx}>{opp}</li>
                            ))}
                          </ul>
                        </section>
                      )}

                      {/* Raw Data */}
                      {report.raw_data && Object.keys(report.raw_data).length > 0 && (
                        <section className="report-section">
                          <h4>Data Insights</h4>
                          <div className="raw-data">
                            {Object.entries(report.raw_data).map(([key, value]) => (
                              <div key={key} className="data-item">
                                <span className="data-key">{key.replace(/_/g, ' ')}</span>
                                <span className="data-value">
                                  {Array.isArray(value) ? value.join(', ') : String(value)}
                                </span>
                              </div>
                            ))}
                          </div>
                        </section>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div style={{ 
              textAlign: 'center', 
              padding: '80px 20px', 
              color: 'var(--text-secondary)',
              gridColumn: '1 / -1'
            }}>
              <FileText size={48} style={{ margin: '0 auto 16px', opacity: 0.3 }} />
              <p style={{ fontSize: '16px' }}>No reports available</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Reports;
