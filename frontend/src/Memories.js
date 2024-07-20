import React, { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Link } from "react-router-dom";
import "./Memories.css"; // Custom styles for the Memories component

function Memories({ memories }) {
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8080/memory')
    .then(response => response.json())
    .then(data => setData(data))
    .catch(error => console.error('Error fetching data: ', error))
  }, []);

  const nextCard = () => {
    setCurrentCardIndex((prevIndex) => (prevIndex + 1) % memories.length);
  };

  const prevCard = () => {
    setCurrentCardIndex((prevIndex) =>
      prevIndex === 0 ? memories.length - 1 : prevIndex - 1
    );
  };

  return (
    <div className="phone-screen">
      <div className="phone-content">
        <h1 className="text-center">Saved Memories</h1>
        <div className="card custom-card">
          <div className="card-body d-flex flex-column justify-content-between">
            <p className="card-text">
              {memories[currentCardIndex]?.transcript}
            </p>
            {memories[currentCardIndex]?.audioUrl && (
              <audio
                controls
                className="audio-player"
                src={memories[currentCardIndex].audioUrl}
              />
            )}
            <div className="text-center mt-3">
              <button
                className="btn btn-primary me-2"
                onClick={prevCard}
                disabled={memories.length === 1} // Disable if only one memory
              >
                Back
              </button>
              <button
                className="btn btn-primary"
                onClick={nextCard}
                disabled={memories.length === 1} // Disable if only one memory
              >
                Next
              </button>
            </div>
          </div>
        </div>
        <div className="mt-3 text-center">
          <Link className="btn btn-secondary" to="/">
            Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Memories;