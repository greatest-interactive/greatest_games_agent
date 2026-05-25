import React from 'react';
import { Link } from 'react-router-dom';
import { Twitter, MessageCircle, Linkedin } from 'lucide-react';
import '../styles/Footer.css';

function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-content">
        {/* Brand Section */}
        <div className="footer-section footer-brand">
          <h3>Greatest Game Agent</h3>
          <p>AI-Powered Game Market Intelligence Platform</p>
          <p className="tagline">Discover profitable game niches. Track competitors. Analyze sentiment. Generate strategies.</p>
        </div>

        {/* Product Links */}
        <div className="footer-section">
          <h4>Product</h4>
          <ul>
            <li><Link to="/trends">Gaming Trends</Link></li>
            <li><Link to="/competitors">Competitor Intelligence</Link></li>
            <li><Link to="/sentiment">Player Sentiment</Link></li>
            <li><Link to="/ai-agent">AI Strategy Generator</Link></li>
          </ul>
        </div>

        {/* Company Links */}
        <div className="footer-section">
          <h4>Company</h4>
          <ul>
            <li><a href="https://greatestinteractive.com" target="_blank" rel="noopener noreferrer">Greatest Interactive</a></li>
            <li><a href="mailto:contact@greatestinteractive.com">Contact Us</a></li>
            <li><a href="https://github.com" target="_blank" rel="noopener noreferrer">GitHub</a></li>
          </ul>
        </div>

        {/* Legal Links */}
        <div className="footer-section">
          <h4>Legal</h4>
          <ul>
            <li><Link to="/terms">Terms & Conditions</Link></li>
            <li><Link to="/privacy">Privacy Policy</Link></li>
            <li><a href="#cookies">Cookie Policy</a></li>
          </ul>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="footer-bottom">
        <div className="footer-bottom-content">
          <p>&copy; {currentYear} Greatest Game Agent. All rights reserved. Powered by Bright Data AI.</p>
          <div className="footer-socials">
            <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" aria-label="Twitter" title="Follow on Twitter">
              <Twitter size={18} />
            </a>
            <a href="https://discord.com" target="_blank" rel="noopener noreferrer" aria-label="Discord" title="Join Discord">
              <MessageCircle size={18} />
            </a>
            <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn" title="Connect on LinkedIn">
              <Linkedin size={18} />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
