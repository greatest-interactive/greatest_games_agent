import React, { useState, useEffect } from 'react';
import { Check, X, Zap } from 'lucide-react';
import { getTiers } from '../api/client';
import PaymentModal from '../components/PaymentModal';
import '../styles/Plans.css';

function Plans() {
  const [tiers, setTiers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedBilling, setSelectedBilling] = useState('monthly');
  const [selectedTier, setSelectedTier] = useState(null);
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [upgradeMessage, setUpgradeMessage] = useState(null);

  useEffect(() => {
    fetchTiers();
  }, []);

  const fetchTiers = async () => {
    try {
      const response = await getTiers();
      setTiers(response.data.results || response.data);
    } catch (error) {
      console.error('Failed to fetch tiers:', error);
    } finally {
      setLoading(false);
    }
  };

  const getPrice = (tier) => {
    if (tier.name === 'free') return 'Free';
    if (tier.name === 'enterprise') return 'Custom';
    const priceMonthly = parseFloat(tier.price_monthly);
    if (selectedBilling === 'yearly' && tier.price_yearly) {
      const priceYearly = parseFloat(tier.price_yearly);
      return `$${(priceYearly / 12).toFixed(2)}/mo (billed yearly)`;
    }
    return `$${priceMonthly.toFixed(2)}/mo`;
  };

  const handleUpgradeClick = (tier) => {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    if (!user.id) {
      // User not logged in - redirect to auth
      window.location.href = '/auth';
      return;
    }

    if (tier.name === 'free') {
      // Free tier - no payment needed
      setUpgradeMessage(`Welcome to ${tier.display_name}! You now have access to free features.`);
      setTimeout(() => setUpgradeMessage(null), 3000);
      return;
    }

    if (tier.name === 'enterprise') {
      // Enterprise - contact sales
      window.open('mailto:sales@greatestgame.com?subject=Enterprise Plan Inquiry');
      return;
    }

    // Show payment modal for paid tiers
    setSelectedTier(tier);
    setShowPaymentModal(true);
  };

  const handlePaymentSuccess = (data) => {
    setShowPaymentModal(false);
    setUpgradeMessage(`🎉 Upgrade successful! Welcome to ${data.tier}`);
    setTimeout(() => setUpgradeMessage(null), 5000);
  };

  const handlePaymentCancel = () => {
    setShowPaymentModal(false);
  };

  const allFeatures = [
    { name: 'Basic game tracking', free: true, starter: true, pro: true, enterprise: true },
    { name: 'Trend analysis', free: true, starter: true, pro: true, enterprise: true },
    { name: 'Competitor tracking', free: false, starter: true, pro: true, enterprise: true },
    { name: 'Advanced market analysis', free: false, starter: true, pro: true, enterprise: true },
    { name: 'Saved games/favorites', free: true, starter: true, pro: true, enterprise: true },
    { name: 'Player sentiment analysis', free: false, starter: true, pro: true, enterprise: true },
    { name: 'AI strategy generation', free: false, starter: true, pro: true, enterprise: true },
    { name: 'Real-time data updates', free: false, starter: false, pro: true, enterprise: true },
    { name: 'Advanced AI predictions', free: false, starter: false, pro: true, enterprise: true },
    { name: 'Data export (CSV/JSON)', free: false, starter: false, pro: true, enterprise: true },
    { name: 'Team collaboration', free: false, starter: false, pro: true, enterprise: true },
    { name: 'Custom API endpoints', free: false, starter: false, pro: true, enterprise: true },
    { name: 'Priority email support', free: false, starter: true, pro: true, enterprise: true },
    { name: '24/7 priority support', free: false, starter: false, pro: false, enterprise: true },
    { name: 'Dedicated account manager', free: false, starter: false, pro: false, enterprise: true },
    { name: 'Custom integrations', free: false, starter: false, pro: false, enterprise: true },
  ];

  if (loading) {
    return <div className="plans-container">Loading plans...</div>;
  }

  return (
    <div className="plans-page">
      <div className="plans-header">
        <h1>Simple, Transparent Pricing</h1>
        <p>Choose the perfect plan for your game development journey</p>
        
        <div className="billing-toggle">
          <button 
            className={`toggle-btn ${selectedBilling === 'monthly' ? 'active' : ''}`}
            onClick={() => setSelectedBilling('monthly')}
          >
            Monthly
          </button>
          <button 
            className={`toggle-btn ${selectedBilling === 'yearly' ? 'active' : ''}`}
            onClick={() => setSelectedBilling('yearly')}
          >
            Yearly
            <span className="discount-badge">Save 20%</span>
          </button>
        </div>
      </div>

      {/* Tier Cards */}
      <div className="tiers-grid">
        {tiers.map((tier) => (
          <div key={tier.id} className={`tier-card ${tier.name === 'pro' ? 'featured' : ''}`}>
            {tier.name === 'pro' && <div className="featured-badge">MOST POPULAR</div>}
            
            <div className="tier-header">
              <h2>{tier.display_name}</h2>
              <p className="tier-description">{tier.description}</p>
            </div>

            <div className="price-section">
              <div className="price">{getPrice(tier)}</div>
              {tier.name !== 'free' && tier.name !== 'enterprise' && (
                <p className="price-note">Perfect for individual developers</p>
              )}
            </div>

            <div className="tier-highlights">
              <div className="highlight-item">
                <Zap size={16} />
                <span>{tier.monthly_tokens} tokens/month</span>
              </div>
              <div className="highlight-item">
                <span>Save up to {tier.max_saved_games === 999999 ? '∞' : tier.max_saved_games} games</span>
              </div>
              <div className="highlight-item">
                <span>{tier.max_scraping_jobs} concurrent scraping jobs</span>
              </div>
            </div>

            <button 
              className={`cta-button ${tier.name}`}
              onClick={() => handleUpgradeClick(tier)}
            >
              {tier.name === 'free' ? 'Get Started' : tier.name === 'enterprise' ? 'Contact Sales' : 'Start Free Trial'}
            </button>

            <div className="tier-features">
              <h3>What's included</h3>
              <ul>
                {tier.features.map((feature, idx) => (
                  <li key={idx}>
                    <Check size={16} className="check-icon" />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>

      {/* Detailed Comparison Table */}
      <div className="comparison-section">
        <h2>Detailed Feature Comparison</h2>
        <div className="comparison-table">
          <div className="table-header">
            <div className="feature-col">Feature</div>
            <div className="tier-col">Free</div>
            <div className="tier-col">Starter</div>
            <div className="tier-col">Pro</div>
            <div className="tier-col">Enterprise</div>
          </div>
          
          {allFeatures.map((feature, idx) => (
            <div key={idx} className="table-row">
              <div className="feature-col">{feature.name}</div>
              <div className="tier-col">
                {feature.free ? <Check size={18} className="check-icon" /> : <X size={18} className="x-icon" />}
              </div>
              <div className="tier-col">
                {feature.starter ? <Check size={18} className="check-icon" /> : <X size={18} className="x-icon" />}
              </div>
              <div className="tier-col">
                {feature.pro ? <Check size={18} className="check-icon" /> : <X size={18} className="x-icon" />}
              </div>
              <div className="tier-col">
                {feature.enterprise ? <Check size={18} className="check-icon" /> : <X size={18} className="x-icon" />}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* FAQ Section */}
      <div className="faq-section">
        <h2>Frequently Asked Questions</h2>
        <div className="faq-grid">
          <div className="faq-item">
            <h3>Can I upgrade anytime?</h3>
            <p>Yes! Upgrade or downgrade your plan at any time. Changes take effect on your next billing cycle.</p>
          </div>
          <div className="faq-item">
            <h3>What are tokens?</h3>
            <p>Tokens are credits used for API calls and data scraping. Each action consumes a specific number of tokens based on complexity.</p>
          </div>
          <div className="faq-item">
            <h3>Do I need a credit card for the Free tier?</h3>
            <p>No! The Free tier is completely free with no credit card required. Only paid plans require billing information.</p>
          </div>
          <div className="faq-item">
            <h3>What's included in Enterprise?</h3>
            <p>Enterprise includes unlimited everything, dedicated support, custom integrations, and SLA guarantees. Contact our sales team for details.</p>
          </div>
          <div className="faq-item">
            <h3>Can I cancel anytime?</h3>
            <p>Absolutely! You can cancel your subscription at any time. No long-term contracts or penalties.</p>
          </div>
          <div className="faq-item">
            <h3>Is there a money-back guarantee?</h3>
            <p>Yes! We offer a 14-day money-back guarantee if you're not satisfied with your purchase.</p>
          </div>
        </div>
      </div>
    </div>

    {/* Payment Modal */}
    <PaymentModal
      isOpen={showPaymentModal}
      tier={selectedTier}
      billingPeriod={selectedBilling}
      onClose={handlePaymentCancel}
      onSuccess={handlePaymentSuccess}
    />

    {/* Upgrade Success Message */}
    {upgradeMessage && (
      <div className="upgrade-success-banner">
        {upgradeMessage}
      </div>
    )}
    </div>
  );
}

export default Plans;
