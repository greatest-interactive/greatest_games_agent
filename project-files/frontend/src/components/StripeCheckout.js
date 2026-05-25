import React, { useState, useEffect } from 'react';
import { CardElement, useElements, useStripe } from '@stripe/react-stripe-js';
import { AlertCircle, CheckCircle, Loader } from 'lucide-react';
import { upgradeTier } from '../api/client';
import '../styles/StripeCheckout.css';

function StripeCheckout({ tier, billingPeriod, onSuccess, onCancel }) {
  const stripe = useStripe();
  const elements = useElements();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [clientSecret, setClientSecret] = useState(null);

  useEffect(() => {
    // Fetch client secret when component mounts
    initializePayment();
  }, [tier, billingPeriod]);

  const initializePayment = async () => {
    try {
      // Call backend to get payment intent
      const response = await upgradeTier({
        to_tier_id: tier.id,
        billing_period: billingPeriod
      });

      if (response.data.payment_intent?.client_secret) {
        setClientSecret(response.data.payment_intent.client_secret);
      } else if (response.data.status === 'completed') {
        // Free tier or downgrade - no payment needed
        setSuccess(true);
        setTimeout(() => onSuccess?.(response.data), 2000);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to initialize payment');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!stripe || !elements) {
      setError('Stripe is not initialized');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const cardElement = elements.getElement(CardElement);

      // Confirm payment with client secret
      if (clientSecret) {
        const result = await stripe.confirmCardPayment(clientSecret, {
          payment_method: {
            card: cardElement,
            billing_details: {
              name: localStorage.getItem('user') 
                ? JSON.parse(localStorage.getItem('user')).username 
                : 'Customer'
            }
          }
        });

        if (result.error) {
          setError(result.error.message);
        } else if (result.paymentIntent.status === 'succeeded') {
          setSuccess(true);
          setTimeout(() => onSuccess?.({ payment_intent_id: result.paymentIntent.id }), 2000);
        }
      }
    } catch (err) {
      setError(err.message || 'Payment failed');
    } finally {
      setLoading(false);
    }
  };

  const cardElementOptions = {
    style: {
      base: {
        fontSize: '16px',
        color: '#424770',
        '::placeholder': {
          color: '#aab7c4',
        },
      },
      invalid: {
        color: '#9e2146',
      },
    },
  };

  if (success) {
    return (
      <div className="stripe-checkout">
        <div className="success-message">
          <CheckCircle size={48} className="success-icon" />
          <h3>Payment Successful!</h3>
          <p>Your tier upgrade has been completed.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="stripe-checkout">
      <form onSubmit={handleSubmit}>
        <div className="form-section">
          <label className="form-label">Card Details</label>
          <CardElement options={cardElementOptions} className="card-element" />
        </div>

        {error && (
          <div className="error-message">
            <AlertCircle size={20} />
            <span>{error}</span>
          </div>
        )}

        <div className="form-actions">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={onCancel}
            disabled={loading}
          >
            Cancel
          </button>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading || !stripe || !elements}
          >
            {loading ? (
              <>
                <Loader size={18} className="spinner" />
                Processing...
              </>
            ) : (
              `Pay $${(tier.price_monthly || 0).toFixed(2)}`
            )}
          </button>
        </div>
      </form>

      <div className="security-notice">
        <p>🔒 Your payment is secure. All transactions are encrypted.</p>
      </div>
    </div>
  );
}

export default StripeCheckout;
