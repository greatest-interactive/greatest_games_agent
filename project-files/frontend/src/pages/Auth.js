import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { register, login } from '../api/client';
import { Star, Lock, Zap, Users, Lightbulb, Settings, BarChart3, Shield } from 'lucide-react';
import '../styles/Auth.css';

export default function Auth() {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password2: '',
    first_name: '',
    last_name: '',
    company: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    setError('');
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await login(formData.username, formData.password);
      
      // Store tokens
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      
      // Store user info
      const userInfo = {
        username: formData.username,
        email: formData.email,
      };
      localStorage.setItem('user', JSON.stringify(userInfo));
      
      setSuccess('Login successful! Redirecting...');
      setTimeout(() => {
        window.location.href = '/';
      }, 1000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    if (formData.password !== formData.password2) {
      setError('Passwords do not match!');
      setLoading(false);
      return;
    }

    try {
      const response = await register({
        username: formData.username,
        email: formData.email,
        password: formData.password,
        password2: formData.password2,
        first_name: formData.first_name,
        last_name: formData.last_name,
        company: formData.company,
      });

      // Store tokens
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      
      // Store user info
      const userInfo = {
        username: formData.username,
        email: formData.email,
        first_name: formData.first_name,
        last_name: formData.last_name,
      };
      localStorage.setItem('user', JSON.stringify(userInfo));
      
      setSuccess('Account created! Redirecting...');
      setTimeout(() => {
        window.location.href = '/';
      }, 1000);
    } catch (err) {
      const errorData = err.response?.data;
      if (typeof errorData === 'object') {
        const messages = Object.entries(errorData)
          .map(([key, val]) => `${key}: ${Array.isArray(val) ? val.join(', ') : val}`)
          .join('\n');
        setError(messages);
      } else {
        setError('Registration failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-container">
      <div className="auth-card">
        <h1>{isLogin ? 'Login' : 'Create Account'}</h1>
        <p className="auth-subtitle">
          {isLogin 
            ? 'Access your AI gaming insights' 
            : 'Join Greatest Game Agent'}
        </p>

        {error && (
          <div className="auth-error">
            <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
            {error}
          </div>
        )}

        {success && (
          <div className="auth-success">
            <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <polyline points="20 6 9 17 4 12" />
            </svg>
            {success}
          </div>
        )}

        <form onSubmit={isLogin ? handleLogin : handleRegister} className="auth-form">
          {!isLogin && (
            <>
              <div className="form-row">
                <div className="form-group">
                  <label>First Name</label>
                  <input
                    type="text"
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleChange}
                    placeholder="John"
                  />
                </div>
                <div className="form-group">
                  <label>Last Name</label>
                  <input
                    type="text"
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleChange}
                    placeholder="Doe"
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Company</label>
                <input
                  type="text"
                  name="company"
                  value={formData.company}
                  onChange={handleChange}
                  placeholder="Your Game Studio"
                />
              </div>

              <div className="form-group">
                <label>Email</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="john@example.com"
                  required
                />
              </div>
            </>
          )}

          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder={isLogin ? 'your_username' : 'Choose a username'}
              required
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="••••••••"
              required
            />
          </div>

          {!isLogin && (
            <div className="form-group">
              <label>Confirm Password</label>
              <input
                type="password"
                name="password2"
                value={formData.password2}
                onChange={handleChange}
                placeholder="••••••••"
                required
              />
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="auth-button"
          >
            {loading ? (
              <>
                <span className="spinner" />
                {isLogin ? 'Logging in...' : 'Creating account...'}
              </>
            ) : (
              isLogin ? 'Login' : 'Create Account'
            )}
          </button>
        </form>

        <div className="auth-toggle">
          <p>
            {isLogin ? "Don't have an account? " : 'Already have an account? '}
            <button
              type="button"
              onClick={() => {
                setIsLogin(!isLogin);
                setError('');
                setSuccess('');
                setFormData({
                  username: '',
                  email: '',
                  password: '',
                  password2: '',
                  first_name: '',
                  last_name: '',
                  company: '',
                });
              }}
              className="toggle-link"
            >
              {isLogin ? 'Sign Up' : 'Login'}
            </button>
          </p>
        </div>

        <div className="auth-info">
          <p>
            <Lightbulb size={18} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'middle' }} />
            <strong>Tip:</strong> You can use all features without logging in. 
            Create an account to save preferences and track your insights.
          </p>
        </div>

        <div className="account-benefits">
          <h3>Why Create an Account?</h3>
          <div className="benefits-grid">
            <div className="benefit-item">
              <Star size={20} />
              <span>Save & organize favorite games</span>
            </div>
            <div className="benefit-item">
              <Lock size={20} />
              <span>Personalized insights & data</span>
            </div>
            <div className="benefit-item">
              <Zap size={20} />
              <span>Advanced AI analysis tools</span>
            </div>
            <div className="benefit-item">
              <Users size={20} />
              <span>Priority customer support</span>
            </div>
          </div>

          <Link to="/plans" className="plans-link">
            View all plans & features →
          </Link>
        </div>

        <div className="authenticated-features">
          <h3>Unlock After Login</h3>
          <div className="features-grid">
            <Link to="/account" className="feature-card">
              <Settings size={24} />
              <div>
                <h4>Account Settings</h4>
                <p>Manage your profile, security, and billing</p>
              </div>
              <span className="arrow">→</span>
            </Link>
            <Link to="/analytics" className="feature-card">
              <BarChart3 size={24} />
              <div>
                <h4>Analytics Dashboard</h4>
                <p>Track your usage and engagement metrics</p>
              </div>
              <span className="arrow">→</span>
            </Link>
            <Link to="/admin" className="feature-card admin-only">
              <Shield size={24} />
              <div>
                <h4>Admin Dashboard</h4>
                <p>Platform analytics & user management (Admin only)</p>
              </div>
              <span className="arrow">→</span>
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}
