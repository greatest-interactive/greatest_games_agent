import React, { useState } from 'react';
import { 
  analyzeTrends, 
  analyzeCompetitors, 
  getMarketGaps,
  generateLaunchStrategy,
  predictTrends,
  queryAIAgent 
} from '../api/client';
import { Zap, Send, BarChart3, Users, Lightbulb, Sparkles, TrendingUp } from 'lucide-react';
import '../styles/AIAgent.css';

function AIAgent() {
  const [activeTab, setActiveTab] = useState('query'); // query, trends, competitors, gaps, strategy, predictions
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Query State
  const [query, setQuery] = useState('');

  // Trend Analysis State
  const [gameConcept, setGameConcept] = useState('');

  // Competitor Analysis State
  const [compGenre, setCompGenre] = useState('');

  // Strategy State
  const [strategyGame, setStrategyGame] = useState('');
  const [strategyGenre, setStrategyGenre] = useState('');
  const [targetAudience, setTargetAudience] = useState('');

  // Prediction State
  const [timeframe, setTimeframe] = useState('6 months');

  const resetStates = () => {
    setError(null);
    setResult(null);
  };

  const handleQueryAI = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    resetStates();
    setLoading(true);
    try {
      const response = await queryAIAgent({ 
        query,
        include_context: true 
      });
      setResult(response.data);
    } catch (error) {
      setError(error.response?.data?.error || 'Error querying AI agent');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeTrends = async () => {
    resetStates();
    setLoading(true);
    try {
      const response = await analyzeTrends({ 
        game_concept: gameConcept || undefined
      });
      setResult(response.data);
    } catch (error) {
      setError(error.response?.data?.error || 'Error analyzing trends');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeCompetitors = async () => {
    resetStates();
    setLoading(true);
    try {
      const response = await analyzeCompetitors({ 
        genre: compGenre || undefined
      });
      setResult(response.data);
    } catch (error) {
      setError(error.response?.data?.error || 'Error analyzing competitors');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGetMarketGaps = async () => {
    resetStates();
    setLoading(true);
    try {
      const response = await getMarketGaps();
      setResult(response.data);
    } catch (error) {
      setError(error.response?.data?.error || 'Error identifying market gaps');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateStrategy = async () => {
    if (!strategyGame || !strategyGenre || !targetAudience) {
      setError('All fields are required');
      return;
    }
    
    resetStates();
    setLoading(true);
    try {
      const response = await generateLaunchStrategy({
        game_concept: strategyGame,
        genre: strategyGenre,
        target_audience: targetAudience
      });
      setResult(response.data);
    } catch (error) {
      setError(error.response?.data?.error || 'Error generating strategy');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePredictTrends = async () => {
    resetStates();
    setLoading(true);
    try {
      const response = await predictTrends({ timeframe });
      setResult(response.data);
    } catch (error) {
      setError(error.response?.data?.error || 'Error predicting trends');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page aiagent-page">
      <div className="page-header">
        <h1>AI Gaming Consultant</h1>
        <p>Leverage AI-powered insights for game market analysis and strategy</p>
      </div>

      <div className="aiagent-container">
        {/* Tab Navigation */}
        <div className="ai-tabs">
          <button 
            className={`ai-tab ${activeTab === 'query' ? 'active' : ''}`}
            onClick={() => setActiveTab('query')}
          >
            <Send size={18} /> Ask AI
          </button>
          <button 
            className={`ai-tab ${activeTab === 'trends' ? 'active' : ''}`}
            onClick={() => setActiveTab('trends')}
          >
            <TrendingUp size={18} /> Analyze Trends
          </button>
          <button 
            className={`ai-tab ${activeTab === 'competitors' ? 'active' : ''}`}
            onClick={() => setActiveTab('competitors')}
          >
            <Users size={18} /> Competitors
          </button>
          <button 
            className={`ai-tab ${activeTab === 'gaps' ? 'active' : ''}`}
            onClick={() => setActiveTab('gaps')}
          >
            <Lightbulb size={18} /> Market Gaps
          </button>
          <button 
            className={`ai-tab ${activeTab === 'strategy' ? 'active' : ''}`}
            onClick={() => setActiveTab('strategy')}
          >
            <BarChart3 size={18} /> Launch Strategy
          </button>
          <button 
            className={`ai-tab ${activeTab === 'predictions' ? 'active' : ''}`}
            onClick={() => setActiveTab('predictions')}
          >
            <Sparkles size={18} /> Predictions
          </button>
        </div>

        <div className="ai-content">
          {/* Query Tab */}
          {activeTab === 'query' && (
            <div className="ai-section">
              <h2>Ask the AI Consultant</h2>
              <p>Ask any question about gaming market trends, strategy, or game development.</p>
              
              <form onSubmit={handleQueryAI} className="query-form">
                <div className="form-group">
                  <textarea
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="E.g., What are the best strategies for launching a roguelike game in 2026?"
                    className="form-textarea"
                    rows={4}
                  />
                </div>
                <button 
                  type="submit" 
                  disabled={loading || !query.trim()}
                  className="btn-submit"
                >
                  <Send size={18} />
                  {loading ? 'Analyzing...' : 'Submit Query'}
                </button>
              </form>
            </div>
          )}

          {/* Trends Analysis Tab */}
          {activeTab === 'trends' && (
            <div className="ai-section">
              <h2>Analyze Gaming Trends</h2>
              <p>Get AI insights on current gaming trends and market opportunities.</p>
              
              <div className="form-group">
                <label>Game Concept (Optional)</label>
                <input
                  type="text"
                  value={gameConcept}
                  onChange={(e) => setGameConcept(e.target.value)}
                  placeholder="E.g., Horror platformer with roguelike elements"
                  className="form-input"
                />
              </div>
              <button 
                onClick={handleAnalyzeTrends}
                disabled={loading}
                className="btn-submit"
              >
                <TrendingUp size={18} />
                {loading ? 'Analyzing Trends...' : 'Analyze Trends'}
              </button>
            </div>
          )}

          {/* Competitors Tab */}
          {activeTab === 'competitors' && (
            <div className="ai-section">
              <h2>Analyze Competitors</h2>
              <p>Get competitive intelligence on existing games in your genre.</p>
              
              <div className="form-group">
                <label>Game Genre (Optional)</label>
                <input
                  type="text"
                  value={compGenre}
                  onChange={(e) => setCompGenre(e.target.value)}
                  placeholder="E.g., Action, RPG, Puzzle"
                  className="form-input"
                />
              </div>
              <button 
                onClick={handleAnalyzeCompetitors}
                disabled={loading}
                className="btn-submit"
              >
                <Users size={18} />
                {loading ? 'Analyzing...' : 'Analyze Competitors'}
              </button>
            </div>
          )}

          {/* Market Gaps Tab */}
          {activeTab === 'gaps' && (
            <div className="ai-section">
              <h2>Identify Market Gaps</h2>
              <p>Discover underserved niches and market opportunities.</p>
              
              <button 
                onClick={handleGetMarketGaps}
                disabled={loading}
                className="btn-submit"
              >
                <Lightbulb size={18} />
                {loading ? 'Identifying...' : 'Find Market Gaps'}
              </button>
            </div>
          )}

          {/* Strategy Tab */}
          {activeTab === 'strategy' && (
            <div className="ai-section">
              <h2>Generate Launch Strategy</h2>
              <p>Create a comprehensive launch strategy for your game concept.</p>
              
              <div className="form-group">
                <label>Game Concept *</label>
                <input
                  type="text"
                  value={strategyGame}
                  onChange={(e) => setStrategyGame(e.target.value)}
                  placeholder="E.g., Cyberpunk noir detective game"
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <label>Genre *</label>
                <input
                  type="text"
                  value={strategyGenre}
                  onChange={(e) => setStrategyGenre(e.target.value)}
                  placeholder="E.g., Action RPG"
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <label>Target Audience *</label>
                <input
                  type="text"
                  value={targetAudience}
                  onChange={(e) => setTargetAudience(e.target.value)}
                  placeholder="E.g., Hardcore gamers ages 18-35"
                  className="form-input"
                />
              </div>
              <button 
                onClick={handleGenerateStrategy}
                disabled={loading}
                className="btn-submit"
              >
                <BarChart3 size={18} />
                {loading ? 'Generating Strategy...' : 'Generate Strategy'}
              </button>
            </div>
          )}

          {/* Predictions Tab */}
          {activeTab === 'predictions' && (
            <div className="ai-section">
              <h2>Predict Future Trends</h2>
              <p>Get AI predictions on upcoming gaming trends and market movements.</p>
              
              <div className="form-group">
                <label>Prediction Timeframe</label>
                <select 
                  value={timeframe}
                  onChange={(e) => setTimeframe(e.target.value)}
                  className="form-input"
                >
                  <option value="3 months">3 Months</option>
                  <option value="6 months">6 Months</option>
                  <option value="1 year">1 Year</option>
                  <option value="2 years">2 Years</option>
                </select>
              </div>
              <button 
                onClick={handlePredictTrends}
                disabled={loading}
                className="btn-submit"
              >
                <Sparkles size={18} />
                {loading ? 'Predicting...' : 'Predict Trends'}
              </button>
            </div>
          )}
        </div>

        {/* Results Section */}
        <div className="ai-results">
          {error && (
            <div className="error-box">
              <p>{error}</p>
            </div>
          )}

          {loading && (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>AI is analyzing your request...</p>
            </div>
          )}

          {result && !loading && (
            <div className="result-box">
              <h3>AI Analysis Result</h3>
              
              {result.response && (
                <div className="response-text">
                  <p>{result.response}</p>
                </div>
              )}

              {result.analysis && (
                <div className="response-text">
                  <p>{result.analysis}</p>
                </div>
              )}

              {result.strategy && (
                <div className="response-text">
                  <p>{result.strategy}</p>
                </div>
              )}

              {result.predictions && (
                <div className="response-text">
                  <p>{result.predictions}</p>
                </div>
              )}

              {result.trending_genres && result.trending_genres.length > 0 && (
                <div className="insights-box">
                  <h4>Trending Genres</h4>
                  <ul>
                    {result.trending_genres.map((genre, idx) => (
                      <li key={idx}>{genre}</li>
                    ))}
                  </ul>
                </div>
              )}

              {result.market_gaps && result.market_gaps.length > 0 && (
                <div className="insights-box">
                  <h4>Market Gaps</h4>
                  <ul>
                    {result.market_gaps.map((gap, idx) => (
                      <li key={idx}>{gap}</li>
                    ))}
                  </ul>
                </div>
              )}

              {result.opportunities && result.opportunities.length > 0 && (
                <div className="insights-box">
                  <h4>Opportunities</h4>
                  <ul>
                    {result.opportunities.map((opp, idx) => (
                      <li key={idx}>{opp}</li>
                    ))}
                  </ul>
                </div>
              )}

              {result.predicted_trends && result.predicted_trends.length > 0 && (
                <div className="insights-box">
                  <h4>Predicted Trends</h4>
                  <ul>
                    {result.predicted_trends.map((trend, idx) => (
                      <li key={idx}>{trend}</li>
                    ))}
                  </ul>
                </div>
              )}

              {result.confidence_score && (
                <div className="confidence-meter">
                  <p>Confidence Score: {result.confidence_score}%</p>
                  <div className="meter-bar">
                    <div className="meter-fill" style={{width: `${result.confidence_score}%`}}></div>
                  </div>
                </div>
              )}
            </div>
          )}

          {!result && !loading && !error && (
            <div className="empty-state">
              <Zap size={48} />
              <p>Analysis results will appear here</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default AIAgent;
