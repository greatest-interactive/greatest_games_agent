import React, { useState, useMemo } from 'react';
import { Elements } from '@stripe/react-stripe-js';
import { loadStripe } from '@stripe/stripe-js';
import StripePaymentCheckout from './StripePaymentCheckout';
import '../styles/PaymentModal.css';

// Initialize Stripe (using test publishable key from settings)
const stripePromise = loadStripe(
  process.env.REACT_APP_STRIPE_PUBLISHABLE_KEY || 'pk_test_51234567890abcdef'
);

function PaymentModal({ isOpen, tier, billingPeriod = 'monthly', onClose, onSuccess }) {
  const [isLoading, setIsLoading] = useState(false);

  const handleSuccess = (data) => {
    setIsLoading(false);
    if (onSuccess) {
      onSuccess(data);
    }
    // Close modal after 2 seconds
    setTimeout(() => {
      onClose();
    }, 2000);
  };

  const handleClose = () => {
    if (!isLoading) {
      onClose();
    }
  };

  const elementOptions = useMemo(
    () => ({
      mode: 'payment',
      currency: 'usd',
      appearance: {
        theme: 'stripe',
        variables: {
          colorPrimary: '#2563eb',
          colorText: '#1f2937',
          borderRadius: '6px',
          fontFamily: 'system-ui, sans-serif',
          fontWeightNormal: 400,
          fontWeightBold: 600,
          spacingUnit: '4px',
        },
      },
    }),
    []
  );

  if (!isOpen) return null;

  return (
    <div className="payment-modal-overlay" onClick={handleClose}>
      <div className="payment-modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close-btn" onClick={handleClose}>
          ✕
        </button>

        <Elements stripe={stripePromise} options={elementOptions}>
          <StripePaymentCheckout
            tier={tier}
            billingPeriod={billingPeriod}
            onSuccess={handleSuccess}
            onCancel={handleClose}
          />
        </Elements>
      </div>
    </div>
  );
}

export default PaymentModal;
