// src/components/Sidebar.jsx
import melofyLogo from "../assets/melofy-logo.svg";

const Sidebar = () => {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <img src={melofyLogo} alt="Melofy logo" className="logo-img" />

        <div className="logo-text">
          <span className="logo-main">Melofy</span>
          <span className="logo-sub">Free music from Jamendo</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        <button className="nav-item active">
          <span>🏠</span>
          <span>Home</span>
        </button>
        <button className="nav-item">
          <span>🔍</span>
          <span>Search</span>
        </button>
        <button className="nav-item">
          <span>📚</span>
          <span>Your Library</span>
        </button>
      </nav>

      <div className="sidebar-footer">
        <p>Powered by Jamendo API</p>
      </div>
    </aside>
  );
};

export default Sidebar;
