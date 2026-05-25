import React from 'react';
import '../styles/Pages.css';

function Terms() {
  return (
    <div className="page">
      <div className="page-header">
        <h1>Terms & Conditions</h1>
        <p>Last updated: May 23, 2026</p>
      </div>

      <div style={{ maxWidth: '800px', margin: '0 auto', lineHeight: 1.8, color: 'var(--text-primary)' }}>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>1. Agreement to Terms</h2>
          <p>
            By accessing and using the Greatest Game Agent platform ("Service"), you accept and agree to be bound by the terms and provision of this agreement. If you do not agree to abide by the above, please do not use this service.
          </p>
        </section>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>2. Use License</h2>
          <p>
            Permission is granted to temporarily download one copy of the materials (information or software) on Greatest Game Agent for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title, and under this license you may not:
          </p>
          <ul style={{ marginLeft: '20px', marginTop: '12px' }}>
            <li>Modifying or copying the materials</li>
            <li>Using the materials for any commercial purpose or for any public display</li>
            <li>Attempting to decompile or reverse engineer any software contained on the Service</li>
            <li>Removing any copyright or other proprietary notations from the materials</li>
            <li>Transferring the materials to another person or "mirroring" the materials on any other server</li>
            <li>Engaging in any data mining, data harvesting, data extracting or similar activity in relation to the Service</li>
          </ul>
        </section>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>3. Disclaimer</h2>
          <p>
            The materials on Greatest Game Agent are provided on an 'as is' basis. Greatest Game Agent makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties including, without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.
          </p>
        </section>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>4. Limitations</h2>
          <p>
            In no event shall Greatest Game Agent or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on the Service, even if Greatest Game Agent or an authorized representative has been notified orally or in writing of the possibility of such damage.
          </p>
        </section>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>5. Accuracy of Materials</h2>
          <p>
            The materials appearing on Greatest Game Agent could include technical, typographical, or photographic errors. Greatest Game Agent does not warrant that any of the materials on the Service are accurate, complete, or current. Greatest Game Agent may make changes to the materials contained on the Service at any time without notice.
          </p>
        </section>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>6. Links</h2>
          <p>
            Greatest Game Agent has not reviewed all of the sites linked to its website and is not responsible for the contents of any such linked site. The inclusion of any link does not imply endorsement by Greatest Game Agent of the site. Use of any such linked website is at the user's own risk.
          </p>
        </section>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>7. Modifications</h2>
          <p>
            Greatest Game Agent may revise these terms of service for the Service at any time without notice. By using the Service, you are agreeing to be bound by the then current version of these terms of service.
          </p>
        </section>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>8. User Accounts</h2>
          <p>
            If the Service requires an account, you are responsible for maintaining the confidentiality of your account and password and for restricting access to your computer. You agree to accept responsibility for all activities that occur under your account or password. You must notify Greatest Game Agent immediately of any unauthorized uses of your account.
          </p>
        </section>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>9. Third-Party Services</h2>
          <p>
            Greatest Game Agent utilizes Bright Data APIs and other third-party services to collect and analyze gaming market data. Your use of the Service may be subject to the terms and policies of these third-party providers. Greatest Game Agent is not responsible for the accuracy or availability of data from third-party sources.
          </p>
        </section>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>10. Governing Law</h2>
          <p>
            These terms and conditions are governed by and construed in accordance with the laws of the jurisdiction in which Greatest Game Agent operates, and you irrevocably submit to the exclusive jurisdiction of the courts in that location.
          </p>
        </section>

        <section style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '16px', color: 'var(--primary)' }}>11. Contact Information</h2>
          <p>
            If you have any questions about these Terms & Conditions, please contact us at:
            <br />
            <strong>Email:</strong> legal@greatestinteractive.com
            <br />
            <strong>Website:</strong> www.greatestinteractive.com
          </p>
        </section>

      </div>
    </div>
  );
}

export default Terms;
