import React, { useState } from "react";

function App() {
  const [isRunning, setIsRunning] = useState(false);

  return (
    <div
      style={{
        textAlign: "center",
        background: "linear-gradient(135deg, #0f2027, #203a43, #2c5364)",
        height: "100vh",
        color: "white",
        fontFamily: "Arial",
      }}
    >
      <h1 style={{ paddingTop: "20px", fontSize: "40px" }}>
        Emotion Detection 🎭
      </h1>

      {/* VIDEO BOX */}
      <div style={{ marginTop: "20px" }}>
        {isRunning ? (
          <img
            src="http://127.0.0.1:5000/video"
            alt="video"
            width="800"
            style={{
              border: "6px solid #00ffcc",
              borderRadius: "15px",
              boxShadow: "0px 0px 20px #00ffcc",
            }}
          />
        ) : (
          <div
            style={{
              width: "800px",
              height: "500px",
              margin: "auto",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              background: "#000",
              borderRadius: "15px",
            }}
          >
            <p style={{ fontSize: "20px", color: "#aaa" }}>
              Camera is OFF
            </p>
          </div>
        )}
      </div>

      {/* BUTTONS */}
      <div style={{ marginTop: "30px" }}>
        <button
          onClick={() => setIsRunning(true)}
          style={{
            padding: "15px 40px",
            fontSize: "18px",
            marginRight: "20px",
            borderRadius: "10px",
            border: "none",
            background: "#00c853",
            color: "white",
            cursor: "pointer",
            transition: "0.3s",
          }}
          onMouseOver={(e) => (e.target.style.background = "#00e676")}
          onMouseOut={(e) => (e.target.style.background = "#00c853")}
        >
          ▶ Start
        </button>

        <button
          onClick={() => setIsRunning(false)}
          style={{
            padding: "15px 40px",
            fontSize: "18px",
            borderRadius: "10px",
            border: "none",
            background: "#d50000",
            color: "white",
            cursor: "pointer",
            transition: "0.3s",
          }}
          onMouseOver={(e) => (e.target.style.background = "#ff1744")}
          onMouseOut={(e) => (e.target.style.background = "#d50000")}
        >
          ⏹ Stop
        </button>
      </div>
    </div>
  );
}

export default App;