import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { User, LogOut, Download, Eye, EyeOff, Trash2, Plus, AlertCircle, Loader } from 'lucide-react';
import { getInvoices, changePassword, logAnalyticsEvent, generateInvoicePDF, downloadInvoicePDF, exportPayments, exportInvoices, exportUserData } from '../api/client';
import '../styles/AccountSettings.css';

const AccountSettings = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [invoices, setInvoices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [downloadingPDF, setDownloadingPDF] = useState(null);
  const [generatingPDF, setGeneratingPDF] = useState(null);
  const [pdfError, setPDFError] = useState('');
  const [pdfSuccess, setPDFSuccess] = useState('');
  const [exportFormat, setExportFormat] = useState('csv');
  const [exporting, setExporting] = useState(null);
  const [exportError, setExportError] = useState('');
  const [activeTab, setActiveTab] = useState('profile');
  const [showPassword, setShowPassword] = useState(false);
  const [passwordForm, setPasswordForm] = useState({
    oldPassword: '',
    newPassword: '',
    confirmPassword: '',
  });
  const [passwordError, setPasswordError] = useState('');
  const [passwordSuccess, setPasswordSuccess] = useState('');

  useEffect(() => {
    const checkUser = localStorage.getItem('user');
    if (!checkUser) {
      navigate('/auth');
      return;
    }
    
    setUser(JSON.parse(checkUser));
    fetchInvoices();
    logAnalyticsEvent('page_visited', 'Account Settings', {}, '/account');
  }, [navigate]);

  const fetchInvoices = async () => {
    try {
      const response = await getInvoices();
      setInvoices(response.data.invoices || []);
    } catch (error) {
      console.error('Failed to load invoices:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    setPasswordError('');
    setPasswordSuccess('');

    if (passwordForm.newPassword !== passwordForm.confirmPassword) {
      setPasswordError('Passwords do not match');
      return;
    }

    if (passwordForm.newPassword.length < 8) {
      setPasswordError('New password must be at least 8 characters');
      return;
    }

    try {
      await changePassword({
        old_password: passwordForm.oldPassword,
        new_password: passwordForm.newPassword,
      });
      setPasswordSuccess('Password changed successfully');
      setPasswordForm({ oldPassword: '', newPassword: '', confirmPassword: '' });
      logAnalyticsEvent('password_changed', 'Password Updated', {});
    } catch (error) {
      setPasswordError(error.response?.data?.detail || 'Failed to change password');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    navigate('/auth');
  };

  const generateAndDownloadPDF = async (invoice) => {
    try {
      setPDFError('');
      setPDFSuccess('');
      setGeneratingPDF(invoice.id);

      // Generate PDF
      await generateInvoicePDF(invoice.id);
      
      // Small delay to ensure file is written
      setTimeout(() => {
        downloadPDF(invoice);
      }, 500);
    } catch (error) {
      setPDFError('Failed to generate PDF. Please try again.');
      console.error('PDF generation error:', error);
    } finally {
      setGeneratingPDF(null);
    }
  };

  const downloadPDF = async (invoice) => {
    try {
      setPDFError('');
      setDownloadingPDF(invoice.id);

      const response = await downloadInvoicePDF(invoice.id);
      
      // Create blob and download
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Invoice_${invoice.invoice_number}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      setPDFSuccess('Invoice downloaded successfully!');
      logAnalyticsEvent('invoice_downloaded', `Downloaded Invoice ${invoice.invoice_number}`, { invoice_id: invoice.id });
    } catch (error) {
      setPDFError('Failed to download PDF. Please try again.');
      console.error('PDF download error:', error);
    } finally {
      setDownloadingPDF(null);
    }
  };

  const downloadInvoice = (invoice) => {
    // Generate and download the PDF
    generateAndDownloadPDF(invoice);
  };

  const handleExportPayments = async () => {
    try {
      setExporting('payments');
      setExportError('');
      
      const blob = await exportPayments(exportFormat, 30);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `payments-${new Date().toISOString().split('T')[0]}.${exportFormat}`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      logAnalyticsEvent('export', 'Payments Exported', { format: exportFormat });
    } catch (error) {
      setExportError('Failed to export payments');
      console.error('Export error:', error);
    } finally {
      setExporting(null);
    }
  };

  const handleExportInvoices = async () => {
    try {
      setExporting('invoices');
      setExportError('');
      
      const blob = await exportInvoices(exportFormat, 30);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `invoices-${new Date().toISOString().split('T')[0]}.${exportFormat}`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      logAnalyticsEvent('export', 'Invoices Exported', { format: exportFormat });
    } catch (error) {
      setExportError('Failed to export invoices');
      console.error('Export error:', error);
    } finally {
      setExporting(null);
    }
  };

  const handleExportUserData = async () => {
    try {
      setExporting('user-data');
      setExportError('');
      
      const blob = await exportUserData(exportFormat);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `user-data-${new Date().toISOString().split('T')[0]}.${exportFormat}`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      logAnalyticsEvent('export', 'User Data Exported', { format: exportFormat });
    } catch (error) {
      setExportError('Failed to export user data');
      console.error('Export error:', error);
    } finally {
      setExporting(null);
    }
  };

  if (!user) return null;

  return (
    <div className="account-settings-container">
      <div className="account-header">
        <h1>
          <User size={28} />
          Account Settings
        </h1>
        <p>Manage your profile, security, and billing</p>
      </div>

      <div className="settings-layout">
        <div className="settings-sidebar">
          <button
            className={`tab-button ${activeTab === 'profile' ? 'active' : ''}`}
            onClick={() => setActiveTab('profile')}
          >
            <User size={18} />
            Profile
          </button>
          <button
            className={`tab-button ${activeTab === 'security' ? 'active' : ''}`}
            onClick={() => setActiveTab('security')}
          >
            <AlertCircle size={18} />
            Security
          </button>
          <button
            className={`tab-button ${activeTab === 'billing' ? 'active' : ''}`}
            onClick={() => setActiveTab('billing')}
          >
            <Download size={18} />
            Billing
          </button>
          <button
            className="tab-button logout"
            onClick={handleLogout}
          >
            <LogOut size={18} />
            Logout
          </button>
        </div>

        <div className="settings-content">
          {/* Profile Tab */}
          {activeTab === 'profile' && (
            <div className="tab-content">
              <h2>Profile Information</h2>
              <div className="profile-card">
                <div className="profile-field">
                  <label>Username</label>
                  <p className="field-value">{user.username}</p>
                </div>
                <div className="profile-field">
                  <label>Email</label>
                  <p className="field-value">{user.email}</p>
                </div>
                <div className="profile-field">
                  <label>First Name</label>
                  <p className="field-value">{user.first_name || 'Not set'}</p>
                </div>
                <div className="profile-field">
                  <label>Last Name</label>
                  <p className="field-value">{user.last_name || 'Not set'}</p>
                </div>
                {user.profile && (
                  <>
                    <div className="profile-field">
                      <label>Company</label>
                      <p className="field-value">{user.profile.company || 'Not set'}</p>
                    </div>
                    <div className="profile-field">
                      <label>Role</label>
                      <p className="field-value">{user.profile.role || 'Not set'}</p>
                    </div>
                  </>
                )}
                <div className="profile-field">
                  <label>Account Created</label>
                  <p className="field-value">{new Date(user.date_joined).toLocaleDateString()}</p>
                </div>
              </div>

              {/* Data Export Section */}
              <div className="data-export-container">
                <h3>Export Your Data</h3>
                <p>Download a copy of your account data including profile, subscription, and activity information.</p>
                
                {exportError && (
                  <div className="error-message">
                    <AlertCircle size={18} />
                    {exportError}
                  </div>
                )}
                
                <div className="data-export-section">
                  <select 
                    value={exportFormat} 
                    onChange={(e) => setExportFormat(e.target.value)}
                  >
                    <option value="csv">CSV Format</option>
                    <option value="json">JSON Format</option>
                  </select>
                  <button 
                    onClick={handleExportUserData}
                    disabled={exporting === 'user-data'}
                  >
                    <Download size={16} />
                    {exporting === 'user-data' ? 'Exporting...' : 'Export My Data'}
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Security Tab */}
          {activeTab === 'security' && (
            <div className="tab-content">
              <h2>Security & Password</h2>
              <form onSubmit={handlePasswordChange} className="security-form">
                <div className="form-group">
                  <label>Current Password *</label>
                  <div className="password-input">
                    <input
                      type={showPassword ? 'text' : 'password'}
                      value={passwordForm.oldPassword}
                      onChange={(e) => setPasswordForm({...passwordForm, oldPassword: e.target.value})}
                      placeholder="Enter current password"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="toggle-password"
                    >
                      {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                  </div>
                </div>

                <div className="form-group">
                  <label>New Password *</label>
                  <div className="password-input">
                    <input
                      type={showPassword ? 'text' : 'password'}
                      value={passwordForm.newPassword}
                      onChange={(e) => setPasswordForm({...passwordForm, newPassword: e.target.value})}
                      placeholder="Enter new password (min 8 characters)"
                      required
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label>Confirm New Password *</label>
                  <div className="password-input">
                    <input
                      type={showPassword ? 'text' : 'password'}
                      value={passwordForm.confirmPassword}
                      onChange={(e) => setPasswordForm({...passwordForm, confirmPassword: e.target.value})}
                      placeholder="Confirm new password"
                      required
                    />
                  </div>
                </div>

                {passwordError && <div className="error-message">{passwordError}</div>}
                {passwordSuccess && <div className="success-message">{passwordSuccess}</div>}

                <button type="submit" className="btn-primary">
                  Update Password
                </button>
              </form>
            </div>
          )}

          {/* Billing Tab */}
          {activeTab === 'billing' && (
            <div className="tab-content">
              <h2>Billing History</h2>
              
              {/* Export Controls */}
              <div className="export-controls">
                <select 
                  value={exportFormat} 
                  onChange={(e) => setExportFormat(e.target.value)}
                >
                  <option value="csv">CSV Format</option>
                  <option value="json">JSON Format</option>
                </select>
                <button 
                  onClick={handleExportPayments}
                  disabled={exporting === 'payments'}
                >
                  <Download size={16} />
                  {exporting === 'payments' ? 'Exporting...' : 'Export Payments'}
                </button>
                <button 
                  onClick={handleExportInvoices}
                  disabled={exporting === 'invoices'}
                >
                  <Download size={16} />
                  {exporting === 'invoices' ? 'Exporting...' : 'Export Invoices'}
                </button>
              </div>
              
              {exportError && (
                <div className="error-message">
                  <AlertCircle size={18} />
                  {exportError}
                </div>
              )}
              
              {pdfError && (
                <div className="error-message">
                  <AlertCircle size={18} />
                  {pdfError}
                </div>
              )}
              
              {pdfSuccess && (
                <div className="success-message">
                  {pdfSuccess}
                </div>
              )}
              
              {loading ? (
                <p className="loading">Loading invoices...</p>
              ) : invoices.length === 0 ? (
                <div className="empty-state">
                  <p>No invoices yet</p>
                  <button onClick={() => navigate('/billing')} className="btn-primary">
                    View Billing
                  </button>
                </div>
              ) : (
                <div className="invoices-table">
                  <div className="table-header">
                    <div>Invoice #</div>
                    <div>Amount</div>
                    <div>Period</div>
                    <div>Status</div>
                    <div>Date</div>
                    <div>Action</div>
                  </div>
                  {invoices.map((invoice) => (
                    <div key={invoice.id} className="table-row">
                      <div>{invoice.invoice_number}</div>
                      <div>${parseFloat(invoice.amount).toFixed(2)}</div>
                      <div>{new Date(invoice.billing_period_start).toLocaleDateString()}</div>
                      <div>
                        <span className={`status-badge status-${invoice.status.toLowerCase()}`}>
                          {invoice.status}
                        </span>
                      </div>
                      <div>{new Date(invoice.created_at).toLocaleDateString()}</div>
                      <div>
                        <button
                          onClick={() => downloadInvoice(invoice)}
                          disabled={downloadingPDF === invoice.id || generatingPDF === invoice.id}
                          className="btn-icon"
                          title={downloadingPDF === invoice.id ? 'Downloading...' : 'Download Invoice PDF'}
                          style={{
                            opacity: downloadingPDF === invoice.id || generatingPDF === invoice.id ? 0.6 : 1,
                            cursor: downloadingPDF === invoice.id || generatingPDF === invoice.id ? 'not-allowed' : 'pointer'
                          }}
                        >
                          {downloadingPDF === invoice.id || generatingPDF === invoice.id ? (
                            <Loader size={18} className="spinner" />
                          ) : (
                            <Download size={18} />
                          )}
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AccountSettings;
