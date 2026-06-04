import React, { useEffect, useRef, useState } from "react";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:7860";

function App() {
  const [isRunning, setIsRunning] = useState(false);
  const [emotion, setEmotion] = useState("Ready to detect");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const intervalRef = useRef(null);
  const streamRef = useRef(null);

  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

  const startCamera = async () => {
    setError("");
    setEmotion("Starting camera...");

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }

      setIsRunning(true);
      setEmotion("Detecting emotion...");
      intervalRef.current = window.setInterval(captureFrame, 1200);
    } catch (err) {
      setError("Unable to open webcam. Please allow camera access.");
      setEmotion("Camera unavailable");
      setIsRunning(false);
    }
  };

  const stopCamera = () => {
    if (intervalRef.current) {
      window.clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    setIsRunning(false);
    setLoading(false);
    setEmotion("Camera is stopped");
  };

  const captureFrame = async () => {
    if (!videoRef.current || !canvasRef.current) {
      return;
    }

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const width = video.videoWidth || 640;
    const height = video.videoHeight || 480;
    canvas.width = width;
    canvas.height = height;

    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, width, height);

    setLoading(true);
    canvas.toBlob(async (blob) => {
      if (!blob) {
        setLoading(false);
        return;
      }

      const formData = new FormData();
      formData.append("image", blob, "frame.jpg");

      try {
        const response = await fetch(`${API_URL}/predict`, {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          throw new Error("Prediction request failed");
        }

        const data = await response.json();
        setEmotion(`${data.emotion} (${(data.confidence * 100).toFixed(1)}%)`);
      } catch (err) {
        setError("Prediction failed. Check backend connection.");
      } finally {
        setLoading(false);
      }
    }, "image/jpeg", 0.8);
  };

  return (
    <div
      style={{
        textAlign: "center",
        background: "linear-gradient(135deg, #0f2027, #203a43, #2c5364)",
        minHeight: "100vh",
        color: "white",
        fontFamily: "Arial, sans-serif",
        paddingBottom: "40px",
      }}
    >
      <h1 style={{ paddingTop: "20px", fontSize: "40px" }}>
        Emotion Detection 🎭
      </h1>

      <div style={{ maxWidth: "900px", margin: "auto", paddingTop: "20px" }}>
        <div
          style={{
            position: "relative",
            border: "6px solid #00ffcc",
            borderRadius: "15px",
            boxShadow: "0px 0px 20px #00ffcc",
            overflow: "hidden",
            background: "#000",
          }}
        >
          {isRunning ? (
            <video
              ref={videoRef}
              style={{ width: "100%", height: "auto" }}
              muted
              autoPlay
              playsInline
            />
          ) : (
            <div
              style={{
                width: "100%",
                minHeight: "500px",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                color: "#aaa",
                fontSize: "20px",
              }}
            >
              {error || "Camera is OFF"}
            </div>
          )}
        </div>

        <div style={{ marginTop: "24px" }}>
          <button
            onClick={startCamera}
            disabled={isRunning}
            style={{
              padding: "15px 40px",
              fontSize: "18px",
              marginRight: "20px",
              borderRadius: "10px",
              border: "none",
              background: isRunning ? "#6b6b6b" : "#00c853",
              color: "white",
              cursor: isRunning ? "not-allowed" : "pointer",
            }}
          >
            ▶ Start
          </button>

          <button
            onClick={stopCamera}
            disabled={!isRunning}
            style={{
              padding: "15px 40px",
              fontSize: "18px",
              borderRadius: "10px",
              border: "none",
              background: !isRunning ? "#6b6b6b" : "#d50000",
              color: "white",
              cursor: !isRunning ? "not-allowed" : "pointer",
            }}
          >
            ⏹ Stop
          </button>
        </div>

        <div style={{ marginTop: "24px", fontSize: "20px" }}>
          <strong>Result:</strong> {loading ? "Detecting..." : emotion}
        </div>
        {error && (
          <div style={{ marginTop: "12px", color: "#ff8a80" }}>{error}</div>
        )}
      </div>

      <canvas ref={canvasRef} style={{ display: "none" }} />
    </div>
  );
}

export default App;
