import React, { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Menu, X, TrendingUp, Users, MessageSquare, FileText, Zap, BarChart2, LogOut, User, BarChart3, Settings, Shield } from 'lucide-react';
import { logout } from '../api/client';
import './Navigation.css';

function Navigation() {
  const location = useLocation();
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);
  const [isUserOpen, setIsUserOpen] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Check if user is logged in
    const checkAuth = () => {
      const token = localStorage.getItem('access_token');
      const storedUser = localStorage.getItem('user');
      if (token && storedUser) {
        try {
          setUser(JSON.parse(storedUser));
        } catch (e) {
          setUser(null);
        }
      } else {
        setUser(null);
      }
    };

    checkAuth();

    // Listen for storage changes (logout in other tabs)
    window.addEventListener('storage', checkAuth);
    return () => window.removeEventListener('storage', checkAuth);
  }, []);

  const navItems = [
    { label: 'Dashboard', path: '/', icon: BarChart2 },
    { label: 'Trends', path: '/trends', icon: TrendingUp },
    { label: 'Competitors', path: '/competitors', icon: Users },
    { label: 'Sentiment', path: '/sentiment', icon: MessageSquare },
    { label: 'Reports', path: '/reports', icon: FileText },
    { label: 'AI Agent', path: '/ai-agent', icon: Zap },
  ];

  const secondaryItems = [
    { label: 'Plans', path: '/plans', icon: FileText, requiresAuth: false },
    ...(user ? [
      { label: 'Analytics', path: '/analytics', icon: BarChart3, requiresAuth: true },
      { label: 'Billing', path: '/billing', icon: FileText, requiresAuth: true },
      { label: 'Account', path: '/account', icon: Settings, requiresAuth: true },
    ] : []),
    ...(user && user.profile?.role === 'admin' ? [
      { label: 'Admin', path: '/admin', icon: Shield, requiresAuth: true },
    ] : []),
  ];

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const handleLogout = async () => {
    try {
      await logout();
    } catch (e) {
      console.error('Logout error:', e);
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    setUser(null);
    setIsOpen(false);
    setIsUserOpen(false);
    navigate('/auth');
  };

  return (
    <nav className="navigation">
      <div className="nav-container">
        <Link to="/" className="nav-logo" onClick={() => setIsOpen(false)}>
          <BarChart2 size={24} />
          <span>Game Agent</span>
        </Link>

        {/* Mobile Hamburger */}
        <button className="hamburger" onClick={toggleMenu}>
          {isOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
        
        {/* Desktop/Mobile Navigation Menu */}
        <ul className={`nav-menu ${isOpen ? 'active' : ''}`}>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <li key={item.path} className={`nav-item ${isActive ? 'active' : ''}`}>
                <Link 
                  to={item.path} 
                  className="nav-link"
                  onClick={() => setIsOpen(false)}
                >
                  <Icon size={18} />
                  <span>{item.label}</span>
                </Link>
              </li>
            );
          })}
          
          {/* Secondary menu items (Plans, Billing, etc.) - only show if user is logged in */}
          {secondaryItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <li key={item.path} className={`nav-item secondary-item ${isActive ? 'active' : ''}`}>
                <Link 
                  to={item.path} 
                  className="nav-link"
                  onClick={() => setIsOpen(false)}
                >
                  <Icon size={18} />
                  <span>{item.label}</span>
                </Link>
              </li>
            );
          })}
          
          {/* Auth section - appears at bottom */}
          {user ? (
            <li className="nav-auth-item">
              <div className="user-menu-mobile">
                <button 
                  className="user-button-mobile"
                  onClick={() => setIsUserOpen(!isUserOpen)}
                >
                  <User size={18} />
                  <span>{user.username}</span>
                </button>
                {isUserOpen && (
                  <div className="user-dropdown-mobile">
                    <div className="user-info">
                      <p className="user-email">{user.email}</p>
                      {user.profile?.role === 'admin' && (
                        <p className="user-role">Admin</p>
                      )}
                    </div>
                    <button 
                      className="logout-button"
                      onClick={() => {
                        handleLogout();
                      }}
                    >
                      <LogOut size={16} />
                      <span>Logout</span>
                    </button>
                  </div>
                )}
              </div>
            </li>
          ) : (
            <li className="nav-auth-item">
              <Link 
                to="/auth" 
                className="auth-button-mobile"
                onClick={() => setIsOpen(false)}
              >
                <User size={18} />
                <span>Login / Sign Up</span>
              </Link>
            </li>
          )}
        </ul>
      </div>
    </nav>
  );
}

export default Navigation;
              </li>
            );
          })}
          
          {/* Auth section - appears at bottom */}
          <li className="nav-auth-item">
            {user ? (
              <div className="user-menu-mobile">
                <button 
                  className="user-button-mobile"
                  onClick={() => setIsUserOpen(!isUserOpen)}
                >
                  <User size={18} />
                  <span>{user.username}</span>
                </button>
                {isUserOpen && (
                  <div className="user-dropdown-mobile">
                    <div className="user-info">
                      <p className="user-email">{user.email}</p>
                    </div>
                    <button 
                      className="logout-button"
                      onClick={() => {
                        handleLogout();
                        setIsOpen(false);
                      }}
                    >
                      <LogOut size={16} />
                      <span>Logout</span>
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <Link 
                to="/auth" 
                className="auth-button-mobile"
                onClick={() => setIsOpen(false)}
              >
                <User size={18} />
                <span>Login / Sign Up</span>
              </Link>
            )}
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navigation;
