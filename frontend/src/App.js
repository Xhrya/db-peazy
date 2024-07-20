import React, { useState, useRef } from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import SpeechRecognition, { useSpeechRecognition } from "react-speech-recognition";
import "./App.css";
import Memories from "./Memories";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  const { transcript, resetTranscript } = useSpeechRecognition();
  const [isListening, setIsListening] = useState(false);
  const [memories, setMemories] = useState([]);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const [audioUrl, setAudioUrl] = useState(null);

  if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
    return <span>Browser doesn't support speech recognition.</span>;
  }

  const handleStartListening = () => {
    setIsListening(true);
    SpeechRecognition.startListening({ continuous: true });

    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then((stream) => {
        mediaRecorderRef.current = new MediaRecorder(stream);
        audioChunksRef.current = [];
        mediaRecorderRef.current.ondataavailable = (event) => {
          audioChunksRef.current.push(event.data);
        };
        mediaRecorderRef.current.start();
      })
      .catch((error) => {
        console.error("Error accessing microphone:", error);
        setIsListening(false);
      });
  };

  const handleStopListening = () => {
    setIsListening(false);
    SpeechRecognition.stopListening();

    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, {
          type: "audio/wav",
        });
        const url = URL.createObjectURL(audioBlob);
        setAudioUrl(url);
      };
    }
  };

  const handleReset = () => {
    resetTranscript();
    setAudioUrl(null);
  };

  const handleSubmit = () => {
    if (transcript && audioUrl) {
      setMemories((prevMemories) => [
        ...prevMemories,
        { transcript, audioUrl }
      ]);
      resetTranscript();
      setAudioUrl(null);
    }
  };

  return (
    <Router>
      <div className="App">
        <div className="container mt-4">
          <Routes>
            <Route
              path="/"
              element={
                <div className="phone-screen">
                  <div className="phone-content">
                    <h1>Welcome!</h1>
                    <button
                      className="btn btn-primary microphone-button"
                      onMouseDown={handleStartListening}
                      onMouseUp={handleStopListening}
                      onTouchStart={handleStartListening}
                      onTouchEnd={handleStopListening}
                    >
                      🎤
                    </button>
                    <p className="phone-text">
                      {isListening ? "Listening..." : "Click the microphone and speak"}
                    </p>
                    <p>{transcript}</p>
                    {audioUrl && <audio controls src={audioUrl} />}
                    <div className="phone-buttons">
                      <button className="btn btn-danger" onClick={handleReset}>
                        Reset
                      </button>
                      {transcript && audioUrl && (
                        <button className="btn btn-success" onClick={handleSubmit}>
                          Submit
                        </button>
                      )}
                    </div>
                  </div>
                  <div className="phone-navbar">
                    <Link className="btn btn-primary" to="/memories">
                      Memories
                    </Link>
                  </div>
                </div>
              }
            />
            <Route path="/memories" element={<Memories memories={memories} />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
