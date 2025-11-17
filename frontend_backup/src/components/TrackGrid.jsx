import TrackCard from "./TrackCard";

const TrackGrid = ({ tracks, loading, onPlay }) => {
  if (loading) {
    return <p className="hint-text">Searching tracks...</p>;
  }

  if (!tracks || tracks.length === 0) {
    return null;
  }

  return (
    <section className="tracks-section">
      <h2 className="section-title">Search results</h2>
      <div className="tracks-grid">
        {tracks.map((track) => (
          <TrackCard key={track.id} track={track} onPlay={onPlay} />
        ))}
      </div>
    </section>
  );
};

export default TrackGrid;
