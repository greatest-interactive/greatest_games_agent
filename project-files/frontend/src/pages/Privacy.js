import React from 'react';
import '../styles/Pages.css';

function Privacy() {
  return (
    <div className="page">
      <div className="page-header">
        <h1>Privacy Policy</h1>
        <p>Last updated: May 23, 2026</p>
      </div>

      <div style={{ maxWidth: '800px', margin: '0 auto', lineHeight: 1.8, color: 'var(--text-primary)' }}>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>1. Introduction</h2>
          <p>
            Greatest Game Agent ("we", "us", "our", or "Company") is committed to protecting your privacy. This Privacy Policy explains our practices regarding the collection, use, and disclosure of personal information when you use our Service.
          </p>
        </section>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>2. Information We Collect</h2>
          <p style={{ fontWeight: 600, marginBottom: '12px' }}>We may collect the following types of information:</p>
          <ul style={{ marginLeft: '20px', marginTop: '12px' }}>
            <li><strong>Account Information:</strong> Name, email address, company name, account credentials</li>
            <li><strong>Usage Data:</strong> Pages visited, time spent, features used, searches performed</li>
            <li><strong>Device Information:</strong> IP address, browser type, operating system, device type</li>
            <li><strong>Market Data:</strong> Gaming trends, competitor information, player sentiment analysis (aggregated, not personal)</li>
            <li><strong>Cookies & Tracking:</strong> We use cookies to enhance your experience and analyze usage patterns</li>
          </ul>
        </section>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>3. How We Use Your Information</h2>
          <p>We use the collected information for the following purposes:</p>
          <ul style={{ marginLeft: '20px', marginTop: '12px' }}>
            <li>To provide, maintain, and improve the Service</li>
            <li>To send technical notices and support messages</li>
            <li>To respond to your inquiries and support requests</li>
            <li>To analyze usage patterns and optimize platform performance</li>
            <li>To detect, investigate, and prevent fraudulent transactions and other illegal activities</li>
            <li>To comply with legal obligations</li>
            <li>To send marketing communications (with your consent)</li>
          </ul>
        </section>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>4. Data Security</h2>
          <p>
            We implement appropriate technical and organizational security measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction. However, no method of transmission over the Internet or electronic storage is 100% secure. While we strive to protect your information, we cannot guarantee absolute security.
          </p>
        </section>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>5. Third-Party Services</h2>
          <p>
            Our Service integrates with third-party services including:
          </p>
          <ul style={{ marginLeft: '20px', marginTop: '12px' }}>
            <li><strong>Bright Data:</strong> Web scraping and market data collection. See their <a href="https://brightdata.com/privacy" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--primary)' }}>Privacy Policy</a></li>
            <li><strong>OpenAI:</strong> AI analysis and insights generation. See their <a href="https://openai.com/privacy" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--primary)' }}>Privacy Policy</a></li>
            <li><strong>Analytics Providers:</strong> To understand how you use the Service</li>
          </ul>
          <p style={{ marginTop: '12px' }}>
            We are not responsible for the privacy practices of third-party services. Please review their privacy policies independently.
          </p>
        </section>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>6. Data Retention</h2>
          <p>
            We retain your personal information for as long as necessary to provide the Service and fulfill the purposes outlined in this Privacy Policy. Market data and analytics may be retained for historical analysis. You may request deletion of your account and associated data at any time.
          </p>
        </section>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>7. Your Rights</h2>
          <p>
            Depending on your location, you may have the following rights:
          </p>
          <ul style={{ marginLeft: '20px', marginTop: '12px' }}>
            <li><strong>Right to Access:</strong> Request a copy of your personal information</li>
            <li><strong>Right to Correction:</strong> Request correction of inaccurate data</li>
            <li><strong>Right to Deletion:</strong> Request deletion of your data ("right to be forgotten")</li>
            <li><strong>Right to Portability:</strong> Request your data in a machine-readable format</li>
            <li><strong>Right to Opt-Out:</strong> Opt-out of marketing communications</li>
          </ul>
        </section>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>8. Cookies & Tracking</h2>
          <p>
            We use cookies to:
          </p>
          <ul style={{ marginLeft: '20px', marginTop: '12px' }}>
            <li>Remember your login information</li>
            <li>Understand how you use the Service</li>
            <li>Personalize your experience</li>
            <li>Analyze service performance</li>
          </ul>
          <p style={{ marginTop: '12px' }}>
            You can control cookies through your browser settings. However, disabling cookies may affect your ability to use certain features of the Service.
          </p>
        </section>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>9. Children's Privacy</h2>
          <p>
            Greatest Game Agent is not intended for use by individuals under 13 years of age. We do not knowingly collect personal information from children under 13. If we become aware that a child has provided us with personal information, we will take steps to delete such information and terminate the child's account.
          </p>
        </section>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>10. International Data Transfers</h2>
          <p>
            Your information may be transferred to, stored in, and processed in countries other than your country of residence. By using the Service, you consent to such transfers.
          </p>
        </section>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>11. Changes to This Policy</h2>
          <p>
            We may update this Privacy Policy from time to time to reflect changes in our practices or for other operational, legal, or regulatory reasons. We will notify you of any material changes by posting the updated policy and updating the "Last updated" date. Your continued use of the Service constitutes your acceptance of the updated Privacy Policy.
          </p>
        </section>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>12. Contact Us</h2>
          <p>
            If you have questions about this Privacy Policy or our privacy practices, please contact us at:
            <br />
            <strong>Email:</strong> privacy@greatestinteractive.com
            <br />
            <strong>Website:</strong> www.greatestinteractive.com
            <br />
            <strong>Address:</strong> Greatest Interactive, Gaming Innovation Hub
          </p>
        </section>

      </div>
    </div>
  );
}

export default Privacy;
