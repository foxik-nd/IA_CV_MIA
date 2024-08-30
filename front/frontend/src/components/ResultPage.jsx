import React from 'react';
import { useLocation } from 'react-router-dom';
import './styles/ResultPage.css';
import Header from './Header';


function ResultPage() {
  const location = useLocation();
  const { score, recommendations } = location.state || {};

  let scoreClass = '';
  if (score >= 80) {
    scoreClass = 'score-80';
  } else if (score >= 60) {
    scoreClass = 'score-60';
  } else if (score >= 45) {
    scoreClass = 'score-45';
  } else {
    scoreClass = 'score-20';
  }

  return (
    <div className="result-page">
      <Header />
      <main className="result-page-content">
        {score !== undefined ? (
          <>
          <div className={`score-section ${scoreClass}`}>
              <div className="score-box">
                <h2>{score}</h2>
              </div>
            </div>
            <div className="recommendations">
              <h3>Recommandations :</h3>
              {recommendations ? (
                <p>{recommendations}</p>
              ) : (
                <p>Aucune recommandation disponible.</p>
              )}
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
