// import React, { useState } from "react";
// import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
// import SpeechRecognition, {
//   useSpeechRecognition,
// } from "react-speech-recognition";
// import "./audio.css";
// import Memories from "./Memories";

// function Audio() {
//   const { transcript, resetTranscript } = useSpeechRecognition();
//   const [isListening, setIsListening] = useState(false);
//   const [memories, setMemories] = useState([]);

//   if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
//     return <span>Browser doesn't support speech recognition.</span>;
//   }

//   const handleStartListening = () => {
//     setIsListening(true);
//     SpeechRecognition.startListening({ continuous: true });
//   };

//   const handleStopListening = () => {
//     setIsListening(false);
//     SpeechRecognition.stopListening();
//   };

//   const handleReset = () => {
//     setMemories([...memories, transcript]);
//     resetTranscript();
//   };

//   return (
//     <Router>
//       <div className="App">
//         <nav>
//           <Link to="/">Home</Link>
//           <Link to="/memories">Memories</Link>
//         </nav>
//         <Routes>
//           <Route
//             path="/"
//             element={
//               <>
//                 <h1>Welcome!</h1>
//                 <button
//                   className="microphone-button"
//                   onMouseDown={handleStartListening}
//                   onMouseUp={handleStopListening}
//                   onTouchStart={handleStartListening}
//                   onTouchEnd={handleStopListening}
//                 >
//                   🎤
//                 </button>
//                 {isListening ? (
//                   <p>Listening...</p>
//                 ) : (
//                   <p>Click the microphone and speak</p>
//                 )}
//                 <p>{transcript}</p>
//                 {transcript && <button onClick={handleReset}>Save</button>}
//               </>
//             }
//           />
//           <Route path="/memories" element={<Memories memories={memories} />} />
//         </Routes>
//       </div>
//     </Router>
//   );
// }

// export default Audio;
