import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { CreditCard, ArrowUpRight, Calendar, AlertCircle } from 'lucide-react';
import { getUserSubscription } from '../api/client';
import '../styles/Billing.css';

function Billing() {
  const navigate = useNavigate();
  const [subscription, setSubscription] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const user = localStorage.getItem('user');
    if (!user) {
      navigate('/auth');
      return;
    }

    fetchSubscription();
  }, [navigate]);

  const fetchSubscription = async () => {
    try {
      setLoading(true);
      const data = await getUserSubscription();
      setSubscription(data);
    } catch (err) {
      setError('Failed to load subscription data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="billing-container"><p>Loading billing information...</p></div>;
  if (error) return <div className="billing-container"><p className="error">{error}</p></div>;

  return (
    <div className="billing-container">
      <div className="billing-header">
        <h1>Billing & Subscription</h1>
        <p>Manage your account and view billing history</p>
      </div>

      {subscription && (
        <div className="billing-content">
          {/* Current Plan Section */}
          <section className="billing-section">
            <h2>Current Plan</h2>
            <div className="current-plan-card">
              <div className="plan-info">
                <h3>{subscription.tier.display_name}</h3>
                <p className="plan-description">{subscription.tier.description}</p>
                <div className="plan-details">
                  <div className="detail-item">
                    <span className="detail-label">Monthly Tokens</span>
                    <span className="detail-value">{subscription.tier.monthly_tokens.toLocaleString()}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Tokens Used This Month</span>
                    <span className="detail-value">{subscription.tokens_used_this_month.toLocaleString()}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Tokens Remaining</span>
                    <span className="detail-value remaining">{subscription.tokens_remaining.toLocaleString()}</span>
                  </div>
                </div>
              </div>
              <div className="plan-actions">
                {subscription.tier.name !== 'enterprise' && subscription.tier.name !== 'pro' && (
                  <button className="upgrade-button" onClick={() => navigate('/plans')}>
                    <ArrowUpRight size={18} />
                    Upgrade Plan
                  </button>
                )}
              </div>
            </div>
          </section>

          {/* Token Usage Section */}
          <section className="billing-section">
            <h2>Token Usage This Month</h2>
            <div className="usage-card">
              <div className="usage-bar">
                <div 
                  className="usage-fill" 
                  style={{
                    width: `${Math.min(100, (subscription.tokens_used_this_month / subscription.tier.monthly_tokens) * 100)}%`
                  }}
                ></div>
              </div>
              <div className="usage-text">
                <span>{subscription.tokens_used_this_month.toLocaleString()} of {subscription.tier.monthly_tokens.toLocaleString()} tokens used</span>
                <span className="usage-percentage">
                  {Math.round((subscription.tokens_used_this_month / subscription.tier.monthly_tokens) * 100)}%
                </span>
              </div>
            </div>
          </section>

          {/* Billing History Section */}
          <section className="billing-section">
            <h2>Billing History</h2>
            <div className="billing-history">
              <div className="history-message">
                <AlertCircle size={20} />
                <p>No billing transactions yet. Billing history will appear after your first payment.</p>
              </div>
            </div>
          </section>

          {/* Pricing Info Section */}
          <section className="billing-section">
            <h2>Pricing Information</h2>
            <div className="pricing-info">
              {subscription.tier.name === 'free' ? (
                <p>You're on the Free plan. Upgrade anytime to access premium features.</p>
              ) : subscription.tier.name === 'enterprise' ? (
                <p>You have a custom Enterprise plan. Contact support for billing details.</p>
              ) : (
                <div>
                  <p>Monthly: ${subscription.tier.price_monthly}/month</p>
                  {subscription.tier.price_yearly && (
                    <p>Annual: ${subscription.tier.price_yearly}/year (Save ~{Math.round(((subscription.tier.price_monthly * 12) - subscription.tier.price_yearly) / (subscription.tier.price_monthly * 12) * 100)}%)</p>
                  )}
                </div>
              )}
            </div>
          </section>
        </div>
      )}
    </div>
  );
}

export default Billing;
