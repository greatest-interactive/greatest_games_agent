import React, { useEffect, useState } from 'react';
import { getScrapedGames } from '../api/client';
import { SkeletonGrid } from '../components/SkeletonLoader';
import { TrendingUp, Trophy, Users, DollarSign, ChevronLeft, ChevronRight } from 'lucide-react';
import '../styles/Competitors.css';

function Competitors() {
  const [competitors, setCompetitors] = useState([]);
  const [loading, setLoading] = useState(false);
  const [platformFilter, setPlatformFilter] = useState('all');
  const [sortBy, setSortBy] = useState('rating');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const pageSize = 50;
  const totalPages = Math.ceil(totalCount / pageSize);

  const fetchCompetitors = async (page = 1) => {
    setLoading(true);
    try {
      const params = { page };
      if (platformFilter !== 'all') params.platform = platformFilter;
      const response = await getScrapedGames(params);
      let data = response.data || [];
      
      // Sort based on selection
      if (sortBy === 'rating') {
        data = [...data].sort((a, b) => (b.rating || 0) - (a.rating || 0));
      } else if (sortBy === 'trending') {
        data = [...data].sort((a, b) => (b.trending_score || 0) - (a.trending_score || 0));
      } else if (sortBy === 'reviews') {
        data = [...data].sort((a, b) => (b.review_count || 0) - (a.review_count || 0));
      } else if (sortBy === 'price') {
        data = [...data].sort((a, b) => (a.price || 0) - (b.price || 0));
      }
      
      setCompetitors(data);
      setTotalCount(response.count || 0);
      setCurrentPage(page);
    } catch (error) {
      console.error('Error fetching competitors:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCompetitors(1);
  }, [platformFilter, sortBy]);

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      fetchCompetitors(currentPage + 1);
      window.scrollTo(0, 0);
    }
  };

  const handlePrevPage = () => {
    if (currentPage > 1) {
      fetchCompetitors(currentPage - 1);
      window.scrollTo(0, 0);
    }
  };

  const getPlatformColor = (platform) => {
    const colors = {
      'steam': '#1b2838',
      'epic': '#313131',
      'mobile': '#34C759',
      'itch': '#fa5c5c',
      'roblox': '#cc2d2d',
      'other': '#666666'
    };
    return colors[platform?.toLowerCase()] || '#3b82f6';
  };

  const getTrendingColor = (score) => {
    if (score >= 80) return '#10b981';
    if (score >= 60) return '#f59e0b';
    return '#ef4444';
  };

  return (
    <div className="competitors-page">
      <header className="page-header">
        <h1>Competitor Intelligence</h1>
        <p>Track competitor releases, pricing, reviews, and engagement</p>
      </header>

      <div className="page-content">
        <div className="filter-controls">
          <div className="filter-group">
            <label>Platform:</label>
            <select 
              value={platformFilter} 
              onChange={(e) => setPlatformFilter(e.target.value)}
              className="filter-select"
            >
              <option value="all">All Platforms</option>
              <option value="steam">Steam</option>
              <option value="epic">Epic Games</option>
              <option value="itch">itch.io</option>
              <option value="mobile">Mobile</option>
              <option value="roblox">Roblox</option>
            </select>
          </div>

          <div className="filter-group">
            <label>Sort By:</label>
            <select 
              value={sortBy} 
              onChange={(e) => setSortBy(e.target.value)}
              className="filter-select"
            >
              <option value="rating">Highest Rating</option>
              <option value="trending">Trending Score</option>
              <option value="reviews">Most Reviews</option>
              <option value="price">Price (Low to High)</option>
            </select>
          </div>
        </div>

        {loading ? (
          <SkeletonGrid count={8} />
        ) : competitors.length > 0 ? (
          <div className="competitors-grid">
            {competitors.map((game) => (
              <div key={game.id} className="competitor-card">
                <div className="card-header">
                  <div className="header-top">
                    <h3 className="game-title">{game.title}</h3>
                    <span 
                      className="platform-badge"
                      style={{ backgroundColor: getPlatformColor(game.platform) }}
                    >
                      {game.platform?.toUpperCase() || 'OTHER'}
                    </span>
                  </div>
                  <p className="developer-name">{game.developer || 'Unknown Studio'}</p>
                </div>

                <div className="metrics-grid">
                  <div className="metric-item">
                    <div className="metric-icon" style={{ color: '#f59e0b' }}>
                      <Trophy size={18} />
                    </div>
                    <div className="metric-content">
                      <div className="metric-label">Rating</div>
                      <div className="metric-value">{game.rating?.toFixed(1) || 'N/A'}</div>
                    </div>
                  </div>

                  <div className="metric-item">
                    <div className="metric-icon" style={{ color: getTrendingColor(game.trending_score || 0) }}>
                      <TrendingUp size={18} />
                    </div>
                    <div className="metric-content">
                      <div className="metric-label">Trending</div>
                      <div className="metric-value">{game.trending_score || 0}%</div>
                    </div>
                  </div>

                  {game.price && (
                    <div className="metric-item">
                      <div className="metric-icon" style={{ color: '#10b981' }}>
                        <DollarSign size={18} />
                      </div>
                      <div className="metric-content">
                        <div className="metric-label">Price</div>
                        <div className="metric-value">${game.price}</div>
                      </div>
                    </div>
                  )}

                  {game.review_count > 0 && (
                    <div className="metric-item">
                      <div className="metric-icon" style={{ color: '#3b82f6' }}>
                        <Users size={18} />
                      </div>
                      <div className="metric-content">
                        <div className="metric-label">Reviews</div>
                        <div className="metric-value">{(game.review_count / 1000).toFixed(1)}K</div>
                      </div>
                    </div>
                  )}
                </div>

                {game.description && (
                  <p className="card-description">
                    {game.description.substring(0, 120)}...
                  </p>
                )}

                {game.genres && game.genres.length > 0 && (
                  <div className="genres-section">
                    <div className="genre-list">
                      {(Array.isArray(game.genres) ? game.genres : JSON.parse(game.genres || '[]')).slice(0, 3).map((genre, i) => (
                        <span key={i} className="genre-tag">
                          {genre}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <div className="card-footer">
                  <div className="last-updated">
                    Updated: {new Date(game.updated_at).toLocaleDateString()}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <p>No competitor data available yet. Scraping data automatically...</p>
          </div>
        )}

        {/* Pagination */}
        {competitors.length > 0 && totalCount > pageSize && (
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
    </div>
  );
}

export default Competitors;
