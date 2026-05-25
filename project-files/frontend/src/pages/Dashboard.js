import React, { useState, useEffect, useRef } from 'react';
import { Search, Zap, TrendingUp, Users, MessageSquare } from 'lucide-react';
import { getTrends, getScrapedGames, getScrapingJobs } from '../api/client';
import '../styles/Dashboard.css';

function Dashboard() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [trends, setTrends] = useState([]);
  const [games, setGames] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const debounceTimer = useRef(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const [trendsRes, gamesRes, jobsRes] = await Promise.all([
        getTrends({ limit: 5 }).catch(() => ({ data: [] })),
        getScrapedGames({ limit: 50 }).catch(() => ({ data: [] })),
        getScrapingJobs().catch(() => ({ data: [] }))
      ]);

      setTrends(trendsRes.data || []);
      setGames(gamesRes.data || []);
      setJobs(jobsRes.data || []);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Debounced search function
  const handleSearchChange = (e) => {
    const value = e.target.value;
    setQuery(value);

    // Clear existing timer
    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current);
    }

    // Set new timer for debounced search
    debounceTimer.current = setTimeout(() => {
      if (value.trim()) {
        performSearch(value);
      } else {
        setSearchResults([]);
        setIsSearching(false);
      }
    }, 500); // 500ms debounce
  };

  const performSearch = (searchQuery) => {
    setIsSearching(true);
    const lowerQuery = searchQuery.toLowerCase();
    
    // Search across games and trends
    const gameMatches = games.filter(g =>
      g.title.toLowerCase().includes(lowerQuery) ||
      g.developer.toLowerCase().includes(lowerQuery) ||
      (g.description && g.description.toLowerCase().includes(lowerQuery))
    );

    const trendMatches = trends.filter(t =>
      t.title.toLowerCase().includes(lowerQuery) ||
      t.description.toLowerCase().includes(lowerQuery) ||
      t.category.toLowerCase().includes(lowerQuery)
    );

    setSearchResults({
      games: gameMatches.slice(0, 5),
      trends: trendMatches.slice(0, 5)
    });
  };

  const handleAnalyzeMarket = async () => {
    if (!query.trim()) {
      alert('Please enter a market to analyze');
      return;
    }
    
    setLoading(true);
    try {
      // Search for market data
      performSearch(query);
      setIsSearching(true);
      console.log(`Analyzing market: ${query}`);
    } catch (error) {
      console.error('Error analyzing market:', error);
      alert('Error analyzing market. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateStrategy = async () => {
    if (!query.trim()) {
      alert('Please enter a game or market concept for strategy generation');
      return;
    }
    
    alert('Strategy generation will be available in Phase 2 (OpenAI Integration)');
    console.log(`Strategy generation requested for: ${query}`);
  };

  const handleDetectTrends = async () => {
    if (!query.trim()) {
      alert('Please enter keywords to detect trends');
      return;
    }
    
    setLoading(true);
    try {
      performSearch(query);
      setIsSearching(true);
      console.log(`Detecting trends for: ${query}`);
    } catch (error) {
      console.error('Error detecting trends:', error);
      alert('Error detecting trends. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Calculate stats from real data
  const uniqueGenres = new Set();
  games.forEach(game => {
    if (Array.isArray(game.genres)) {
      game.genres.forEach(g => uniqueGenres.add(g));
    }
  });

  const trendingGames = games.filter(g => g.trending_score >= 70).length;
  const avgRating = games.length > 0 ? (games.reduce((sum, g) => sum + (g.rating || 0), 0) / games.length).toFixed(1) : 0;
  const completedJobs = jobs.filter(j => j.status === 'completed').length || 0;

  return (
    <div className="dashboard">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1>Greatest Game Agent</h1>
          <p>AI-Powered Game Market Intelligence Platform</p>
          <p className="subtitle">Discover profitable game niches. Track competitors in real time. Analyze player sentiment. Generate launch strategies.</p>
        </div>
      </section>

      {/* Search Section */}
      <section className="search-section">
        <div className="search-container">
          <div className="search-input-wrapper">
            <Search size={20} className="search-icon" />
            <input
              type="text"
              value={query}
              onChange={handleSearchChange}
              placeholder="Search games, trends, or markets..."
              className="search-input"
            />
          </div>
          <div className="action-buttons">
            <button 
              onClick={handleAnalyzeMarket}
              disabled={loading || !query.trim()}
              className="btn btn-primary"
              title="Analyze market data for the entered query"
            >
              <TrendingUp size={18} /> Analyze Market
            </button>
            <button 
              onClick={handleGenerateStrategy}
              disabled={loading || !query.trim()}
              className="btn btn-secondary"
              title="AI-powered strategy generation (Phase 2)"
            >
              <Zap size={18} /> Generate Strategy
            </button>
            <button 
              onClick={handleDetectTrends}
              disabled={loading || !query.trim()}
              className="btn btn-secondary"
              title="Detect emerging trends"
            >
              <TrendingUp size={18} /> Detect Trends
            </button>
          </div>
        </div>
      </section>

      {/* Search Results */}
      {isSearching && (query.trim() || searchResults.games?.length > 0 || searchResults.trends?.length > 0) && (
        <section className="search-results">
          <h2>Search Results for "{query}"</h2>
          {searchResults.games && searchResults.games.length > 0 && (
            <div className="results-section">
              <h3>Games ({searchResults.games.length})</h3>
              <div className="results-grid">
                {searchResults.games.map((game) => (
                  <div key={game.id} className="result-card">
                    <h4>{game.title}</h4>
                    <p className="developer">{game.developer || 'Unknown'}</p>
                    <p className="rating">Rating: {game.rating || 'N/A'} / 10</p>
                    <span className="platform-badge">{game.platform}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
          {searchResults.trends && searchResults.trends.length > 0 && (
            <div className="results-section">
              <h3>Trends ({searchResults.trends.length})</h3>
              <div className="results-grid">
                {searchResults.trends.map((trend) => (
                  <div key={trend.id} className="result-card">
                    <h4>{trend.title}</h4>
                    <p className="growth">Growth: {trend.growth_rate}%</p>
                    <p className="momentum">Momentum: {trend.momentum_score}%</p>
                    <span className="category-badge">{trend.category}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
          {(!searchResults.games || searchResults.games.length === 0) && (!searchResults.trends || searchResults.trends.length === 0) && (
            <p className="no-results">No results found for "{query}"</p>
          )}
        </section>
      )}

      {/* Quick Stats */}
      <section className="quick-stats">
        <div className="stat-card">
          <div className="stat-icon trending">
            <TrendingUp size={24} />
          </div>
          <div className="stat-content">
            <h3>Games Tracked</h3>
            <p className="stat-number">{games.length}</p>
            <span className="stat-label">Across platforms</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon competitors">
            <Users size={24} />
          </div>
          <div className="stat-content">
            <h3>Trending Games</h3>
            <p className="stat-number">{trendingGames}</p>
            <span className="stat-label">75%+ momentum</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon sentiment">
            <MessageSquare size={24} />
          </div>
          <div className="stat-content">
            <h3>Average Rating</h3>
            <p className="stat-number">{avgRating}</p>
            <span className="stat-label">All games</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon ai">
            <Zap size={24} />
          </div>
          <div className="stat-content">
            <h3>Data Collections</h3>
            <p className="stat-number">{completedJobs}</p>
            <span className="stat-label">Completed</span>
          </div>
        </div>
      </section>

      {/* Live Trend Feed */}
      <section className="live-feed">
        <h2>Live Market Trends</h2>
        <div className="trends-grid">
          {trends.length > 0 ? (
            trends.map((trend) => (
              <div key={trend.id} className="trend-card">
                <h4>{trend.title}</h4>
                <p className="trend-momentum">Growth: {trend.growth_rate}%</p>
                <p className="trend-desc">{trend.description}</p>
                <div className="trend-tags">
                  <span className="tag">{trend.category}</span>
                  <span className="tag" style={{
                    background: trend.momentum_score > 80 ? 'rgba(16, 185, 129, 0.2)' : 'rgba(59, 130, 246, 0.2)',
                    color: trend.momentum_score > 80 ? '#10b981' : 'var(--primary)'
                  }}>
                    {trend.momentum_score}% momentum
                  </span>
                </div>
              </div>
            ))
          ) : (
            <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '40px', color: 'var(--text-secondary)' }}>
              <p>No trends available yet. Data will appear after collection.</p>
            </div>
          )}
        </div>
      </section>

      {/* Top Games Section */}
      {games.length > 0 && (
        <section className="live-feed">
          <h2>Top Trending Games</h2>
          <div className="trends-grid">
            {games.slice(0, 5).map((game) => (
              <div key={game.id} className="trend-card">
                <h4>{game.title}</h4>
                <p className="trend-momentum">Rating: {game.rating || 'N/A'} stars</p>
                <p className="trend-desc">{game.developer || game.platform}</p>
                <div className="trend-tags">
                  <span className="tag">{game.platform}</span>
                  <span className="tag">{game.trending_score}% trending</span>
                  {game.review_count > 0 && (
                    <span className="tag">{game.review_count} reviews</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

export default Dashboard;
