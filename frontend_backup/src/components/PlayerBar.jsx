const PlayerBar = ({ track }) => {
  if (!track || !track.audio_url) {
    return (
      <div className="player-bar empty">
        <p>Select a track to start listening</p>
      </div>
    );
  }

  return (
    <div className="player-bar">
      <div className="player-track-info">
        {track.image && (
          <img
            src={track.image}
            alt={track.title}
            className="player-cover"
          />
        )}
        <div>
          <p className="player-title">{track.title}</p>
          <p className="player-artist">{track.artist}</p>
        </div>
      </div>

      <div className="player-controls">
        <audio controls src={track.audio_url} className="player-audio">
          Your browser does not support the audio element.
        </audio>
      </div>

      <div className="player-extra">
        <span className="badge">Jamendo</span>
      </div>
    </div>
  );
};

export default PlayerBar;
