import { useState } from "react";
import "./App.css";

import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import TrackGrid from "./components/TrackGrid";
import PlayerBar from "./components/PlayerBar";

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [query, setQuery] = useState("");
  const [tracks, setTracks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [currentTrack, setCurrentTrack] = useState(null); // bottom player ke liye

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError("");
    setTracks([]);

    try {
      const res = await fetch(
        `${API_BASE}/api/search?q=${encodeURIComponent(query)}`
      );

      if (!res.ok) {
        let msg = "Search failed";
        try {
          const errData = await res.json();
          msg = errData.detail || msg;
        } catch (_) {}
        throw new Error(msg);
      }

      const data = await res.json();
      setTracks(data.results || []);
    } catch (e) {
      console.error(e);
      setError(e.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="app-root">
      {/* upar ka pura spotify jaisa shell */}
      <div className="app-shell">
        <Sidebar />

        <div className="app-content">
          <Header />

          <main className="main-view">
            <div className="search-bar">
              <input
                type="text"
                placeholder="Search: lofi, chill, hip hop, romantic..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={handleKeyDown}
              />
              <button onClick={handleSearch} disabled={loading}>
                {loading ? "Searching..." : "Search"}
              </button>
            </div>

            {error && <p className="error-text">{error}</p>}

            {!loading && !error && tracks.length === 0 && (
              <p className="hint-text">
                Upar kuch type karo aur Search dabao 😊
              </p>
            )}

            <TrackGrid
              tracks={tracks}
              loading={loading}
              onPlay={(track) => setCurrentTrack(track)}
            />
          </main>
        </div>
      </div>

      {/* neeche ka permanent player */}
      <PlayerBar track={currentTrack} />
    </div>
  );
}

export default App;
