import React from 'react';
import '../styles/SkeletonLoader.css';

export function SkeletonCard() {
  return (
    <div className="skeleton-card">
      <div className="skeleton skeleton-title"></div>
      <div className="skeleton skeleton-text"></div>
      <div className="skeleton skeleton-text" style={{ width: '80%' }}></div>
      <div className="skeleton skeleton-badge"></div>
    </div>
  );
}

export function SkeletonTrendCard() {
  return (
    <div className="skeleton-trend-item">
      <div className="skeleton skeleton-title" style={{ width: '60%' }}></div>
      <div className="skeleton skeleton-text" style={{ marginTop: '12px' }}></div>
      <div className="skeleton skeleton-text" style={{ width: '85%' }}></div>
      <div style={{ display: 'flex', gap: '8px', marginTop: '12px' }}>
        <div className="skeleton skeleton-tag"></div>
        <div className="skeleton skeleton-tag"></div>
      </div>
    </div>
  );
}

export function SkeletonGrid({ count = 6 }) {
  return (
    <div className="grid-container">
      {Array.from({ length: count }).map((_, i) => (
        <SkeletonCard key={i} />
      ))}
    </div>
  );
}

export function SkeletonTrendList({ count = 5 }) {
  return (
    <div className="trends-list">
      {Array.from({ length: count }).map((_, i) => (
        <SkeletonTrendCard key={i} />
      ))}
    </div>
  );
}
