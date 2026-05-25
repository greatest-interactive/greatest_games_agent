import React, { useEffect, useState } from 'react';
import { getSentiment } from '../api/client';
import { SkeletonGrid } from '../components/SkeletonLoader';
import { MessageSquare, TrendingUp, TrendingDown, ThumbsUp, ThumbsDown, Zap, ChevronLeft, ChevronRight } from 'lucide-react';
import '../styles/Sentiment.css';

function Sentiment() {
  const [sentiment, setSentiment] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState('all');
  const [sourceFilter, setSourceFilter] = useState('all');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const pageSize = 50;
  const totalPages = Math.ceil(totalCount / pageSize);

  const fetchSentiment = async (page = 1) => {
    setLoading(true);
    try {
      const params = { page };
      if (filter !== 'all') params.sentiment_type = filter;
      if (sourceFilter !== 'all') params.source = sourceFilter;
      const response = await getSentiment(params);
      setSentiment(response.data || []);
      setTotalCount(response.count || 0);
      setCurrentPage(page);
    } catch (error) {
      console.error('Error fetching sentiment:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSentiment(1);
  }, [filter, sourceFilter]);

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      fetchSentiment(currentPage + 1);
      window.scrollTo(0, 0);
    }
  };

  const handlePrevPage = () => {
    if (currentPage > 1) {
      fetchSentiment(currentPage - 1);
      window.scrollTo(0, 0);
    }
  };

  const handleFilterChange = (type) => {
    setFilter(type);
  };

  const handleSourceChange = (source) => {
    setSourceFilter(source);
  };

  // Calculate sentiment stats
  const positiveCount = sentiment.filter(s => s.sentiment_type === 'positive').length;
  const neutralCount = sentiment.filter(s => s.sentiment_type === 'neutral').length;
  const negativeCount = sentiment.filter(s => s.sentiment_type === 'negative').length;

  const topGames = Array.from(new Set(sentiment.map(s => s.game_title)));
  const topSources = [...new Set(sentiment.map(s => s.source))];

  const getSentimentColor = (sentiment_type) => {
    switch(sentiment_type) {
      case 'positive': return '#10b981';
      case 'negative': return '#ef4444';
      case 'neutral': return '#6b7280';
      default: return 'var(--primary)';
    }
  };

  const getSentimentIcon = (sentiment_type) => {
    switch(sentiment_type) {
      case 'positive': return <ThumbsUp size={16} />;
      case 'negative': return <ThumbsDown size={16} />;
      case 'neutral': return <MessageSquare size={16} />;
      default: return <MessageSquare size={16} />;
    }
  };

  return (
    <div className="sentiment-page">
      <header className="page-header">
        <h1>Player Sentiment Analysis</h1>
        <p>Real-time sentiment tracking across Reddit, YouTube, Steam, TikTok, Twitter, and Discord</p>
      </header>

      {/* Stats Section */}
      <section className="sentiment-stats">
        <div className="stat-card positive">
          <div className="stat-icon">
            <ThumbsUp size={24} />
          </div>
          <div className="stat-content">
            <h3>Positive</h3>
            <p className="stat-number">{positiveCount}</p>
          </div>
        </div>
        <div className="stat-card neutral">
          <div className="stat-icon">
            <MessageSquare size={24} />
          </div>
          <div className="stat-content">
            <h3>Neutral</h3>
            <p className="stat-number">{neutralCount}</p>
          </div>
        </div>
        <div className="stat-card negative">
          <div className="stat-icon">
            <ThumbsDown size={24} />
          </div>
          <div className="stat-content">
            <h3>Negative</h3>
            <p className="stat-number">{negativeCount}</p>
          </div>
        </div>
        <div className="stat-card total">
          <div className="stat-icon">
            <Zap size={24} />
          </div>
          <div className="stat-content">
            <h3>Total Posts</h3>
            <p className="stat-number">{sentiment.length}</p>
          </div>
        </div>
      </section>

      {/* Filters */}
      <section className="filter-section">
        <div className="filter-group">
          <h4>Sentiment Type</h4>
          <div className="filter-buttons">
            <button 
              className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
              onClick={() => handleFilterChange('all')}
            >
              All
            </button>
            <button 
              className={`filter-btn ${filter === 'positive' ? 'active' : ''}`}
              onClick={() => handleFilterChange('positive')}
            >
              Positive
            </button>
            <button 
              className={`filter-btn ${filter === 'neutral' ? 'active' : ''}`}
              onClick={() => handleFilterChange('neutral')}
            >
              Neutral
            </button>
            <button 
              className={`filter-btn ${filter === 'negative' ? 'active' : ''}`}
              onClick={() => handleFilterChange('negative')}
            >
              Negative
            </button>
          </div>
        </div>

        <div className="filter-group">
          <h4>Source</h4>
          <div className="filter-buttons">
            <button 
              className={`filter-btn ${sourceFilter === 'all' ? 'active' : ''}`}
              onClick={() => handleSourceChange('all')}
            >
              All
            </button>
            {['steam', 'reddit', 'youtube', 'tiktok', 'twitter', 'discord'].map(source => (
              <button 
                key={source}
                className={`filter-btn ${sourceFilter === source ? 'active' : ''}`}
                onClick={() => handleSourceChange(source)}
              >
                {source.charAt(0).toUpperCase() + source.slice(1)}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Sentiment Feed */}
      {loading ? (
        <SkeletonGrid count={6} />
      ) : (
        <div className="sentiment-feed">
          {sentiment.length > 0 ? (
            <div className="sentiment-grid">
              {sentiment.map((item) => (
                <div 
                  key={item.id} 
                  className={`sentiment-card sentiment-${item.sentiment_type}`}
                >
                  <div className="card-header">
                    <div className="card-title-section">
                      <h4 className="game-title">{item.game_title}</h4>
                      <span className="sentiment-badge" style={{ color: getSentimentColor(item.sentiment_type) }}>
                        {getSentimentIcon(item.sentiment_type)}
                        {item.sentiment_type.charAt(0).toUpperCase() + item.sentiment_type.slice(1)}
                      </span>
                    </div>
                  </div>

                  <div className="card-meta">
                    <span className="source-badge">{item.source.toUpperCase()}</span>
                    <span className="score-badge">
                      {(item.sentiment_score * 100).toFixed(0)}% confidence
                    </span>
                  </div>

                  <p className="card-comment">{item.comment}</p>

                  <div className="card-footer">
                    <span className="engagement">
                      <Zap size={14} /> {item.engagement_metric.toLocaleString()} engagement
                    </span>
                    {item.key_themes && item.key_themes.length > 0 && (
                      <div className="themes">
                        {item.key_themes.slice(0, 3).map((theme, idx) => (
                          <span key={idx} className="theme-tag">{theme}</span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '60px 20px', color: 'var(--text-secondary)' }}>
              <MessageSquare size={48} style={{ margin: '0 auto 16px', opacity: 0.3 }} />
              <p>No sentiment data available for the selected filters</p>
            </div>
          )}

          {/* Pagination */}
          {totalCount > pageSize && (
            <div className="pagination">
              <button
                className="pagination-btn"
                onClick={handlePrevPage}
                disabled={currentPage === 1}
              >
                <ChevronLeft size={18} />
                Previous
              </button>
              
              <div className="pagination-info">
                Page <span className="page-number">{currentPage}</span> of <span className="page-number">{totalPages}</span>
                <span className="result-count">({totalCount} results)</span>
              </div>
              
              <button
                className="pagination-btn"
                onClick={handleNextPage}
                disabled={currentPage === totalPages}
              >
                Next
                <ChevronRight size={18} />
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Sentiment;
