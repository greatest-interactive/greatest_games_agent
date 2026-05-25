import React, { useEffect, useState } from 'react';
import { getTrends } from '../api/client';
import { SkeletonTrendList } from '../components/SkeletonLoader';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import '../styles/Trends.css';

function Trends() {
  const [trends, setTrends] = useState([]);
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const pageSize = 50;
  const totalPages = Math.ceil(totalCount / pageSize);

  const fetchTrends = async (page = 1) => {
    setLoading(true);
    try {
      const response = await getTrends({ 
        category: filter === 'all' ? '' : filter,
        page: page 
      });
      setTrends(response.data || []);
      setTotalCount(response.count || 0);
      setCurrentPage(page);
    } catch (error) {
      console.error('Error fetching trends:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTrends(1);
  }, [filter]);

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      fetchTrends(currentPage + 1);
      window.scrollTo(0, 0);
    }
  };

  const handlePrevPage = () => {
    if (currentPage > 1) {
      fetchTrends(currentPage - 1);
      window.scrollTo(0, 0);
    }
  };

  return (
    <div className="trends-page">
      <header className="page-header">
        <h1>Gaming Trends</h1>
        <p>Discover trending mechanics, genres, and opportunities</p>
      </header>

      <div className="page-content">
        <div className="filter-bar">
          <button 
            className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
            onClick={() => setFilter('all')}
          >
            All Trends
          </button>
          <button 
            className={`filter-btn ${filter === 'genre' ? 'active' : ''}`}
            onClick={() => setFilter('genre')}
          >
            Genres
          </button>
          <button 
            className={`filter-btn ${filter === 'mechanic' ? 'active' : ''}`}
            onClick={() => setFilter('mechanic')}
          >
            Mechanics
          </button>
          <button 
            className={`filter-btn ${filter === 'monetization' ? 'active' : ''}`}
            onClick={() => setFilter('monetization')}
          >
            Monetization
          </button>
        </div>

        {loading ? (
          <SkeletonTrendList count={5} />
        ) : (
          <>
            <div className="trends-list">
              {trends.length === 0 ? (
                <div className="empty-state">
                  <p>No trends found. Check back soon!</p>
                </div>
              ) : (
                trends.map((trend) => (
                  <div key={trend.id} className="trend-item">
                    <div className="trend-header">
                      <h3>{trend.title}</h3>
                      <span className="momentum-badge" style={{
                        background: trend.momentum_score > 70 ? 'rgba(16, 185, 129, 0.2)' : 'rgba(59, 130, 246, 0.2)'
                      }}>
                        {trend.momentum_score}% momentum
                      </span>
                    </div>
                    <p className="trend-description">{trend.description}</p>
                    <div className="trend-stats">
                      <div className="stat">
                        <span className="stat-label">Growth Rate</span>
                        <span className="stat-value">+{trend.growth_rate}%</span>
                      </div>
                      <div className="stat">
                        <span className="stat-label">Search Volume</span>
                        <span className="stat-value">{trend.search_volume.toLocaleString()}</span>
                      </div>
                      <div className="stat">
                        <span className="stat-label">Opportunity</span>
                        <span className="stat-value">{trend.opportunity_level}</span>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>

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
          </>
        )}
      </div>
    </div>
  );
}

export default Trends;
