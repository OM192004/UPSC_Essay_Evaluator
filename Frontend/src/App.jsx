import { useState, useEffect } from 'react'
import './index.css'

function App() {
  const [theme, setTheme] = useState('dark');
  const [essay, setEssay] = useState('');
  const [question, setQuestion] = useState('');
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  const handleEvaluate = async () => {
    if (essay.trim().length < 50) {
      setError("Essay must be at least 50 characters long.");
      return;
    }

    setIsEvaluating(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/evaluate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question, text: essay }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to evaluate essay');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsEvaluating(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header" style={{ position: 'relative' }}>
        <button
          onClick={toggleTheme}
          style={{ position: 'absolute', top: 0, right: 0, background: 'none', border: 'none', color: 'var(--text-primary)', fontSize: '1.5rem', cursor: 'pointer' }}
          title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
        >
          {theme === 'dark' ? '☀️' : '🌙'}
        </button>
        <h1>UPSC Essay Evaluator</h1>
        <p>Advanced hybrid evaluation using DEEP LEARNING</p>
      </header>

      <main className="main-content">
        {/* Input Section */}
        <div className="glass-panel essay-input-container">
          <h2>Submit Your Essay</h2>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem', fontSize: '0.9rem' }}>
            Paste your UPSC essay below for comprehensive analysis.
          </p>

          <textarea
            value={question}
            onChange={(e) => {
              setQuestion(e.target.value);
              if (error) setError(null);
            }}
            placeholder="Enter the essay topic or question here..."
            className="question-input essay-question-container"
            style={{ marginBottom: '1rem', maxHeight: '100px' }}
          />

          <textarea
            value={essay}
            onChange={(e) => {
              setEssay(e.target.value);
              if (error) setError(null);
            }}
            placeholder="Start typing your essay here... (Minimum 50 characters & Maximum 1200 characters)"
          />

          {error && <p style={{ color: '#ef4444', marginTop: '0.5rem', fontSize: '0.9rem' }}>{error}</p>}

          <button
            className="btn-primary"
            onClick={handleEvaluate}
            disabled={isEvaluating || essay.trim().length === 0}
          >
            {isEvaluating ? (
              <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
                <span className="spinner"></span> Evaluating...
              </span>
            ) : 'Evaluate Essay'}
          </button>
        </div>

        {/* Results Section */}
        <div className="glass-panel results-container">
          <h2>Evaluation Results</h2>

          {!results && !isEvaluating && (
            <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-secondary)' }}>
              <p>Submit an essay to see your score and detailed feedback.</p>
            </div>
          )}

          {isEvaluating && (
            <div style={{ height: '300px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', color: 'var(--text-secondary)', gap: '1rem' }}>
              <span className="spinner" style={{ width: '40px', height: '40px', borderWidth: '4px' }}></span>
              <p>Our Model is analyzing your essay...</p>
            </div>
          )}

          {results && !isEvaluating && (
            <div className="results-content">
              <div className="score-display">
                <div className="score-circle" style={{ '--score': results.final_score }}>
                  <div className="score-value">{results.final_score}</div>
                </div>
                <p>Final Score</p>
                <h3 style={{ marginTop: '0.5rem', color: 'var(--accent-primary)', fontSize: '1.2rem' }}>
                  UPSC Score: {((results.final_score * 85) / 100).toFixed(2)} / 125
                </h3>
              </div>


              <div className="feedback-section">
                <h3>Detailed Feedback</h3>
                <p className="feedback-text">{results.feedback}</p>

                {results.breakdown?.llm_components && Object.keys(results.breakdown.llm_components).length > 0 && (
                  <div className="breakdown-grid" style={{ marginTop: '1rem' }}>
                    {Object.entries(results.breakdown.llm_components).map(([key, value]) => (
                      <div key={key} className="breakdown-item" style={{ padding: '0.5rem' }}>
                        <span className="breakdown-label" style={{ fontSize: '0.7rem' }}>{key}</span>
                        <span className="breakdown-score" style={{ fontSize: '1rem' }}>{value}/25</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default App
