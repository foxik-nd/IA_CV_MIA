import React from 'react';
import { useLocation } from 'react-router-dom';
import './styles/ResultPage.css';
import Header from './Header';


function ResultPage() {
    const location = useLocation();
    const { score, recommendations } = location.state || {};
  
    return (
      <div className="result-page">
      <Header/>
        <main className="result-page-content">
          {score !== undefined ? (
            <>
              <div className="score-section">
                <div className={`score-box score-${score}`}>
                  <h2>{score}</h2>
                </div>
              </div>
              <div className="recommendations">
                <h3>Recommandations :</h3>
                <ul>
                  {Array.isArray(recommendations) ? (
                    recommendations.map((rec, index) => (
                      <li key={index}>{rec}</li>
                    ))
                  ) : (
                    <p>Aucune recommandation disponible.</p>
                  )}
                </ul>
              </div>
            </>
          ) : (
            <p>No results available. Please try again.</p>
          )}
        </main>
      </div>
    );
  }

  export default ResultPage;
