import React, { useEffect, useRef, useState } from "react";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

function App() {
  const [isRunning, setIsRunning] = useState(false);
  const [emotion, setEmotion] = useState("Ready to detect");
  const [loading, setLoading] = useState(false);

  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const intervalRef = useRef(null);
  const streamRef = useRef(null);
  const busyRef = useRef(false);
  const runningRef = useRef(false);

  // Sending webcam-sized frames to a remote API is expensive. This resolution is
  // sufficient for a 48x48 emotion model while making each upload much smaller.
  const FRAME_WIDTH = 320;
  const FRAME_HEIGHT = 240;
  const JPEG_QUALITY = 0.7;
  const NEXT_FRAME_DELAY_MS = 250;

  useEffect(() => {
    return () => stopCamera();
  }, []);

  const startCamera = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { width: 640, height: 480 },
      audio: false,
    });

    streamRef.current = stream;
    videoRef.current.srcObject = stream;
    await videoRef.current.play();

    runningRef.current = true;
    setIsRunning(true);
    setEmotion("Detecting...");
    captureFrame();
  };

  const stopCamera = () => {
    runningRef.current = false;
    if (intervalRef.current) clearTimeout(intervalRef.current);
    intervalRef.current = null;

    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
    }

    setIsRunning(false);
    setLoading(false);
    setEmotion("Camera stopped");
  };

  const captureFrame = async () => {
    if (!runningRef.current || busyRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;

    if (!video || !canvas || video.videoWidth === 0) return;

    busyRef.current = true;
    setLoading(true);

    const ctx = canvas.getContext("2d");

    canvas.width = FRAME_WIDTH;
    canvas.height = FRAME_HEIGHT;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
      if (!blob || !runningRef.current) {
        busyRef.current = false;
        return;
      }

      const formData = new FormData();
      formData.append("image", blob, "frame.jpg");

      try {
        const res = await fetch(`${API_URL}/predict`, {
          method: "POST",
          body: formData,
        });

        const data = await res.json();

        if (!runningRef.current) return;

        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        if (data.faces && data.faces.length > 0) {
  data.faces.forEach((face) => {
    const { x, y, w, h } = face.box;

    ctx.strokeStyle = "blue";
    ctx.lineWidth = 4;
    ctx.strokeRect(x, y, w, h);

    ctx.fillStyle = "lime";
    ctx.font = "32px Arial";
    ctx.fillText(face.emotion, x, y - 10);
  });

  const firstFace = data.faces[0];
  setEmotion(
    `${data.faces.length} face(s) detected - ${firstFace.emotion} (${(
      firstFace.confidence * 100
    ).toFixed(1)}%)`
  );
} else {
  setEmotion("No face detected");
}
      } catch (err) {
        if (runningRef.current) setEmotion("Backend error");
      } finally {
        busyRef.current = false;
        if (runningRef.current) {
          intervalRef.current = setTimeout(captureFrame, NEXT_FRAME_DELAY_MS);
        } else {
          setLoading(false);
        }
      }
    }, "image/jpeg", JPEG_QUALITY);
  };

  return (
    <div
      style={{
        textAlign: "center",
        background: "linear-gradient(135deg, #0f2027, #203a43, #2c5364)",
        minHeight: "100vh",
        color: "white",
        fontFamily: "Arial",
        paddingBottom: "40px",
      }}
    >
      <h1 style={{ paddingTop: "20px", fontSize: "40px" }}>
        Emotion Detection 🎭
      </h1>

      <video ref={videoRef} style={{ display: "none" }} muted playsInline />

      <div
        style={{
          maxWidth: "800px",
          margin: "auto",
          border: "6px solid #00ffcc",
          borderRadius: "15px",
          boxShadow: "0 0 20px #00ffcc",
          background: "black",
        }}
      >
        <canvas
          ref={canvasRef}
          style={{
            width: "100%",
            display: "block",
          }}
        />
      </div>

      <div style={{ marginTop: "25px" }}>
        <button
          onClick={startCamera}
          disabled={isRunning}
          style={{
            padding: "15px 40px",
            marginRight: "20px",
            background: "#00c853",
            color: "white",
            border: "none",
            borderRadius: "10px",
            fontSize: "18px",
          }}
        >
          ▶ Start
        </button>

        <button
          onClick={stopCamera}
          disabled={!isRunning}
          style={{
            padding: "15px 40px",
            background: "#d50000",
            color: "white",
            border: "none",
            borderRadius: "10px",
            fontSize: "18px",
          }}
        >
          ■ Stop
        </button>
      </div>

      <div style={{ marginTop: "25px", fontSize: "22px" }}>
        <strong>Result:</strong> {loading ? "Detecting..." : emotion}
      </div>
    </div>
  );
}

export default App;
