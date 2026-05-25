import React, { useState, useEffect } from 'react';
import { CardElement, useStripe, useElements } from '@stripe/react-stripe-js';
import { AlertCircle, CheckCircle, Loader } from 'lucide-react';
import '../styles/StripePaymentCheckout.css';

function StripePaymentCheckout({ tier, billingPeriod = 'monthly', onSuccess, onCancel }) {
  const stripe = useStripe();
  const elements = useElements();
  
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [cardComplete, setCardComplete] = useState(false);
  const [clientSecret, setClientSecret] = useState(null);
  const [tierChangeId, setTierChangeId] = useState(null);
  const [proratedCredit, setProratedCredit] = useState(0);
  const [amountDue, setAmountDue] = useState(0);

  useEffect(() => {
    if (!tier) return;
    
    // Initialize tier upgrade and get payment intent
    initiateTierChange();
  }, [tier, billingPeriod]);

  const initiateTierChange = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://localhost:8000/api/tiers/upgrade/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          to_tier_id: tier.id,
          billing_period: billingPeriod
        })
      });

      if (!response.ok) {
        throw new Error('Failed to initiate tier upgrade');
      }

      const data = await response.json();
      
      setTierChangeId(data.tier_change_id);
      setProratedCredit(data.prorated_credit);
      setAmountDue(data.amount_due);
      
      if (data.payment_intent) {
        setClientSecret(data.payment_intent.client_secret);
      } else if (data.amount_due <= 0) {
        // No payment needed - immediate upgrade
        setSuccess(true);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const handleCardChange = (event) => {
    setCardComplete(event.complete);
    if (event.error) {
      setError(event.error.message);
    } else {
      setError(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!stripe || !elements) {
      return;
    }

    if (!cardComplete) {
      setError('Please enter complete card details');
      return;
    }

    setIsProcessing(true);
    setError(null);

    try {
      const cardElement = elements.getElement(CardElement);
      
      // Confirm payment with Stripe
      const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
        payment_method: {
          card: cardElement,
          billing_details: {
            // Add billing details from user profile if needed
          }
        }
      });

      if (error) {
        setError(error.message);
        setIsProcessing(false);
        return;
      }

      if (paymentIntent.status === 'succeeded') {
        // Confirm payment in backend
        const token = localStorage.getItem('access_token');
        const confirmResponse = await fetch('http://localhost:8000/api/payments/confirm/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            payment_intent_id: paymentIntent.id,
            tier_change_id: tierChangeId
          })
        });

        if (!confirmResponse.ok) {
          throw new Error('Failed to confirm payment in backend');
        }

        setSuccess(true);
        if (onSuccess) {
          onSuccess({
            tierChangeId,
            paymentIntentId: paymentIntent.id,
            tier: tier.display_name
          });
        }
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsProcessing(false);
    }
  };

  if (!tier) {
    return <div className="payment-error">No tier selected</div>;
  }

  if (success) {
    return (
      <div className="payment-success">
        <div className="success-icon">
          <CheckCircle size={48} />
        </div>
        <h2>Upgrade Successful!</h2>
        <p>Welcome to {tier.display_name} tier</p>
        {proratedCredit > 0 && (
          <p className="prorated-note">
            Prorated credit applied: ${proratedCredit.toFixed(2)}
          </p>
        )}
        <button 
          className="success-button"
          onClick={() => onCancel && onCancel()}
        >
          Close
        </button>
      </div>
    );
  }

  // If no payment needed
  if (amountDue <= 0 && !clientSecret) {
    return (
      <div className="payment-success">
        <div className="success-icon">
          <CheckCircle size={48} />
        </div>
        <h2>Downgrade Confirmed!</h2>
        <p>You've been downgraded to {tier.display_name} tier</p>
        {proratedCredit > 0 && (
          <p className="credit-note">
            Credit applied to your account: ${proratedCredit.toFixed(2)}
          </p>
        )}
        <button 
          className="success-button"
          onClick={() => onCancel && onCancel()}
        >
          Done
        </button>
      </div>
    );
  }

  return (
    <div className="payment-checkout">
      <div className="checkout-header">
        <h2>Upgrade to {tier.display_name}</h2>
        <p className="billing-period">Billing: {billingPeriod === 'yearly' ? 'Yearly' : 'Monthly'}</p>
      </div>

      {/* Price Summary */}
      <div className="price-summary">
        <div className="summary-row">
          <span>Tier Price</span>
          <span className="amount">
            ${billingPeriod === 'yearly' ? (tier.price_yearly || tier.price_monthly * 12).toFixed(2) : tier.price_monthly.toFixed(2)}
          </span>
        </div>
        
        {proratedCredit > 0 && (
          <div className="summary-row credit">
            <span>Prorated Credit</span>
            <span className="amount">-${proratedCredit.toFixed(2)}</span>
          </div>
        )}

        <div className="summary-divider"></div>

        <div className="summary-row total">
          <span>Amount Due Today</span>
          <span className="amount">
            {amountDue > 0 ? `$${amountDue.toFixed(2)}` : 'Free'}
          </span>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="payment-error">
          <AlertCircle size={20} />
          <p>{error}</p>
        </div>
      )}

      {/* Payment Form */}
      {amountDue > 0 ? (
        <form onSubmit={handleSubmit} className="payment-form">
          <div className="form-group">
            <label htmlFor="card-element">Card Details</label>
            <div className="card-element-wrapper">
              <CardElement
                id="card-element"
                onChange={handleCardChange}
                options={{
                  style: {
                    base: {
                      fontSize: '16px',
                      color: '#424770',
                      '::placeholder': {
                        color: '#aab7c4',
                      },
                    },
                    invalid: {
                      color: '#fa755a',
                      iconColor: '#fa755a',
                    },
                  },
                  hidePostalCode: true,
                }}
              />
            </div>
          </div>

          <div className="form-actions">
            <button
              type="submit"
              disabled={isProcessing || !cardComplete || !clientSecret}
              className="submit-button"
            >
              {isProcessing ? (
                <>
                  <Loader size={18} className="spinner" />
                  Processing...
                </>
              ) : (
                `Pay $${amountDue.toFixed(2)}`
              )}
            </button>
            
            <button
              type="button"
              onClick={onCancel}
              disabled={isProcessing}
              className="cancel-button"
            >
              Cancel
            </button>
          </div>

          <p className="secure-note">
            🔒 Your payment information is secure and encrypted
          </p>
        </form>
      ) : (
        <div className="free-upgrade">
          <p className="upgrade-message">
            Your credit covers this upgrade! No payment needed.
          </p>
          <button 
            onClick={() => setSuccess(true)}
            className="confirm-button"
          >
            Confirm Upgrade
          </button>
        </div>
      )}
    </div>
  );
}

export default StripePaymentCheckout;
