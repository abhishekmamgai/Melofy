const TrackCard = ({ track, onPlay }) => {
  const handlePlayClick = () => {
    if (onPlay) onPlay(track);
  };

  return (
    <div className="track-card">
      <div className="track-image-wrapper" onClick={handlePlayClick}>
        {track.image ? (
          <img
            src={track.image}
            alt={track.title}
            className="track-image"
          />
        ) : (
          <div className="track-placeholder">No cover</div>
        )}
        <div className="track-overlay">
          <button className="play-button" type="button">
            ▶
          </button>
        </div>
      </div>

      <div className="track-info">
        <h3 className="track-title">{track.title || "Untitled track"}</h3>
        <p className="track-artist">{track.artist || "Unknown artist"}</p>
      </div>

      <div className="track-links">
        {track.audio_url && (
          <button
            className="small-link"
            type="button"
            onClick={handlePlayClick}
          >
            Play in player
          </button>
        )}

        {track.jamendo_url && (
          <a
            href={track.jamendo_url}
            target="_blank"
            rel="noreferrer"
            className="small-link"
          >
            Open on Jamendo →
          </a>
        )}
      </div>
    </div>
  );
};

export default TrackCard;
